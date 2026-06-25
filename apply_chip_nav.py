#!/usr/bin/env python3
"""
apply_chip_nav.py

Apply the sticky chip nav + back-to-top pattern to every city profile under
cities/*/profile.html. Idempotent: files that already have the nav are skipped.

Usage (run from repo root):
    python3 scripts/apply_chip_nav.py            # write changes in place
    python3 scripts/apply_chip_nav.py --dry-run  # report only, no writes

The script does five things per file:
  1. Insert chip-nav CSS just before </style>
  2. Insert the anchor div + <nav> markup just before <!-- STATS -->
  3. Add id="fit"/"about"/"week"/"where"/"health"/"compare" to the six sections
  4. Insert a "Back to top" button at the end of each of those sections
  5. Insert the controller JS just before </body>

It also performs a preflight check on every file: if any required marker is
missing, the file is skipped untouched and reported.
"""
import glob
import re
import sys

DRY_RUN = '--dry-run' in sys.argv

# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------

CSS_BLOCK = """
/* ===== STICKY CHIP NAV ===== */
html { scroll-padding-top: 64px; }
.section-nav {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(247, 243, 237, 0.94);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(28,26,24,0.08);
  height: 52px;
  display: flex;
  align-items: center;
}
.section-nav-inner {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  scrollbar-width: none;
  padding: 0 16px;
  width: 100%;
  scroll-behavior: smooth;
}
.section-nav-inner::-webkit-scrollbar { display: none; }
.nav-chip {
  background: #E8F4F3;
  border: 1px solid #2A5E5A;
  color: #2A5E5A;
  font-family: 'Libre Franklin', sans-serif;
  font-size: 12.5px;
  font-weight: 700;
  padding: 8px 14px;
  border-radius: 100px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s;
  flex-shrink: 0;
}
.nav-chip:hover { background: #D4E7E5; }
.nav-chip.active {
  background: #2A5E5A;
  color: #FFFFFF;
  border-color: #2A5E5A;
}
@media (min-width: 768px) {
  .section-nav-inner { justify-content: center; }
}
.back-to-top-wrap {
  margin-top: 36px;
  padding-top: 22px;
  border-top: 1px solid rgba(28,26,24,0.08);
  text-align: center;
}
.back-to-top-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: transparent;
  border: 1px solid rgba(28,26,24,0.16);
  color: #5C5852;
  font-family: 'Libre Franklin', sans-serif;
  font-size: 11.5px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 9px 18px;
  border-radius: 100px;
  cursor: pointer;
  transition: all 0.2s;
}
.back-to-top-link:hover {
  background: #1C1A18;
  color: #FFFFFF;
  border-color: #1C1A18;
}
.back-to-top-link .arr { font-size: 13px; line-height: 1; }
/* ===== END STICKY CHIP NAV CSS ===== */

"""

NAV_HTML = """<!-- STICKY CHIP NAV -->
<div id="navAnchor" aria-hidden="true" style="height:1px;"></div>
<nav class="section-nav" id="sectionNav">
  <div class="section-nav-inner">
    <button class="nav-chip" data-target="fit">Is it for you?</button>
    <button class="nav-chip" data-target="about">About the city</button>
    <button class="nav-chip" data-target="week">A week here</button>
    <button class="nav-chip" data-target="where">Where to live</button>
    <button class="nav-chip" data-target="health">Healthcare</button>
    <button class="nav-chip" data-target="compare">Compare cities</button>
  </div>
</nav>

"""

BTT_INNER = ('<div class="back-to-top-wrap">'
             '<button class="back-to-top-link" data-back-to-top>'
             '<span class="arr">\u2191</span> Back to top</button></div>')

JS_BLOCK = """
<script>
/* ===== STICKY CHIP NAV BEHAVIOR ===== */
(function(){
  var nav = document.getElementById('sectionNav');
  if (!nav) return;
  var chips = nav.querySelectorAll('.nav-chip');
  var navInner = nav.querySelector('.section-nav-inner');
  var ids = ['fit','about','week','where','health','compare'];
  var sections = ids.map(function(id){ return document.getElementById(id); }).filter(Boolean);

  chips.forEach(function(chip){
    chip.addEventListener('click', function(){
      var target = document.getElementById(chip.dataset.target);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (entry.isIntersecting) {
          var id = entry.target.id;
          chips.forEach(function(c){ c.classList.toggle('active', c.dataset.target === id); });
          var activeChip = nav.querySelector('.nav-chip.active');
          if (activeChip && navInner) {
            var chipLeft = activeChip.offsetLeft;
            var chipRight = chipLeft + activeChip.offsetWidth;
            var visLeft = navInner.scrollLeft;
            var visRight = visLeft + navInner.offsetWidth;
            if (chipLeft < visLeft + 20) navInner.scrollLeft = chipLeft - 20;
            else if (chipRight > visRight - 20) navInner.scrollLeft = chipRight - navInner.offsetWidth + 20;
          }
        }
      });
    }, { rootMargin: '-60px 0px -60% 0px', threshold: 0 });
    sections.forEach(function(s){ observer.observe(s); });
  }

  var anchor = document.getElementById('navAnchor');
  document.querySelectorAll('[data-back-to-top]').forEach(function(btn){
    btn.addEventListener('click', function(e){
      e.preventDefault();
      if (anchor) {
        anchor.scrollIntoView({ behavior: 'smooth', block: 'start' });
      } else {
        nav.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
})();
/* ===== END STICKY CHIP NAV BEHAVIOR ===== */
</script>

"""

# Section markers used for back-to-top insertion. The marker text appears
# inside the comment immediately AFTER the section whose end we want to mark.
# Strings here are unique substrings, not full comment text -- this lets us
# handle minor wording variations across profiles ("LIFESTYLE PHOTO BANNER"
# vs "LIFESTYLE BANNER", em-dash vs double-hyphen in "PLAN YOUR MOVE", etc).
BTT_TARGETS = [
    'EMAIL CAPTURE',
    'DETAIL PHOTO BREAK',
    'LIFESTYLE',
    'HEALTHCARE -->',
    'PLAN YOUR MOVE',
    'QUIZ CTA',
]

# Required anchors -- preflight check before any mutation
REQUIRED = [
    '</style>',
    '<!-- STATS -->',
    'class="section fit-section"',
    'class="section character-section"',
    'class="section week-section"',
    'class="section related-section"',
    '<!-- NEIGHBORHOODS -->',
    '<!-- HEALTHCARE -->',
    '<!-- EMAIL CAPTURE -->',
    '<!-- DETAIL PHOTO BREAK -->',
    '<!-- PLAN YOUR MOVE',
    '<!-- QUIZ CTA -->',
    '</body>',
]


def add_id_to_section_after(html, comment, id_value):
    """Add id="id_value" to the first <section> that follows `comment`."""
    pattern = re.compile(
        re.escape(comment) + r'\s*\n\s*<section\b([^>]*)>'
    )
    def repl(m):
        attrs = m.group(1)
        if 'id=' in attrs:
            return m.group(0)
        return m.group(0).replace(
            '<section' + attrs + '>',
            '<section' + attrs + ' id="' + id_value + '">'
        )
    return pattern.sub(repl, html, count=1)


def insert_btt_before_marker(html, marker):
    """
    Insert the back-to-top wrap inside the .wrap div that closes immediately
    before `marker`. The expected structure is:

        \\n<indent></div>\\n</section>\\n\\n<!-- ... marker ... -->

    The back-to-top wrap is inserted with two extra spaces of indent so it
    sits as the last child inside the wrap.
    """
    pattern = re.compile(
        r'(\n)([ \t]+)(</div>\n)(</section>[ \t]*\n[ \t]*\n)'
        r'(<!--(?:(?!-->)[\s\S])*?'
        + re.escape(marker)
        + r'(?:(?!-->)[\s\S])*?-->)'
    )
    m = pattern.search(html)
    if not m:
        return html, False
    newline, indent, wrap_close, section_close, comment = m.groups()
    insertion = (newline + indent + '  ' + BTT_INNER
                 + newline + indent + wrap_close
                 + section_close + comment)
    return html[:m.start()] + insertion + html[m.end():], True


def patch_file(path):
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if 'id="sectionNav"' in html:
        return 'SKIP', 'already patched'

    missing = [m for m in REQUIRED if m not in html]
    if missing:
        return 'SKIP', 'missing markers: ' + ', '.join(missing[:3]) + ('...' if len(missing) > 3 else '')

    # 1. CSS before </style>
    if html.count('</style>') < 1:
        return 'SKIP', 'no </style>'
    html = html.replace('</style>', CSS_BLOCK + '</style>', 1)

    # 2. NAV HTML before <!-- STATS -->
    html = html.replace('<!-- STATS -->', NAV_HTML + '<!-- STATS -->', 1)

    # 3. Add IDs to six sections
    html = html.replace(
        'class="section fit-section"',
        'class="section fit-section" id="fit"', 1)
    html = html.replace(
        'class="section character-section"',
        'class="section character-section" id="about"', 1)
    html = html.replace(
        'class="section week-section"',
        'class="section week-section" id="week"', 1)
    html = html.replace(
        'class="section related-section"',
        'class="section related-section" id="compare"', 1)
    html = add_id_to_section_after(html, '<!-- NEIGHBORHOODS -->', 'where')
    html = add_id_to_section_after(html, '<!-- HEALTHCARE -->', 'health')

    # Verify all six IDs are now present
    for needle in ['id="fit"', 'id="about"', 'id="week"',
                   'id="where"', 'id="health"', 'id="compare"']:
        if needle not in html:
            return 'SKIP', 'failed to insert ' + needle

    # 4. Back-to-top buttons before each section's closing
    inserted = 0
    for marker in BTT_TARGETS:
        html, ok = insert_btt_before_marker(html, marker)
        if ok:
            inserted += 1
    if inserted < 6:
        return 'SKIP', 'only inserted ' + str(inserted) + '/6 back-to-top buttons'

    # 5. JS before </body>
    html = html.replace('</body>', JS_BLOCK + '</body>', 1)

    # Sanity: exactly six buttons should be present (selector in JS uses brackets)
    if html.count('data-back-to-top>') != 6:
        return 'SKIP', 'wrong back-to-top count: ' + str(html.count('data-back-to-top>'))

    if not DRY_RUN:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
    return 'PATCH', 'ok'


def main():
    profiles = sorted(glob.glob('cities/*/profile.html'))
    if not profiles:
        print('No profiles found at cities/*/profile.html. Run from repo root.',
              file=sys.stderr)
        sys.exit(1)

    mode = 'DRY-RUN' if DRY_RUN else 'WRITE'
    print('Found ' + str(len(profiles)) + ' profiles. Mode: ' + mode)
    print('-' * 72)
    counts = {'PATCH': 0, 'SKIP': 0}
    skips = []
    for path in profiles:
        action, reason = patch_file(path)
        counts[action] = counts.get(action, 0) + 1
        marker = '[PATCH]' if action == 'PATCH' else '[SKIP] '
        print(marker + ' ' + path + ('  -- ' + reason if action == 'SKIP' else ''))
        if action == 'SKIP' and reason != 'already patched':
            skips.append((path, reason))
    print('-' * 72)
    print('Summary: ' + str(counts['PATCH']) + ' patched, ' + str(counts['SKIP']) + ' skipped')
    if skips:
        print('\nNon-trivial skips (need manual review):')
        for path, reason in skips:
            print('  ' + path + ' -- ' + reason)


if __name__ == '__main__':
    main()
