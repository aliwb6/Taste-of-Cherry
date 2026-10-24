"""Run with Python Playwright and a locally installed Chromium browser.

TASTE_CHROME can point to a Chromium executable. No server is needed.
Screenshots are written outside the repository, under /tmp/taste-image-check.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('/tmp/taste-image-check')
OUT.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path=os.environ.get('TASTE_CHROME', '/usr/bin/google-chrome-stable'))
    context = browser.new_context(offline=True)
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto((ROOT / 'index.html').as_uri(), wait_until='networkidle')
    assert page.locator('.slide').count() == 9
    assert page.locator('#prev').is_disabled()
    assert page.locator('img').evaluate_all('(images) => images.every(i => i.complete && i.naturalWidth > 0)')
    for width, height in [(1920, 1080), (1366, 768), (1280, 800), (768, 1024), (390, 844), (844, 390)]:
        page.set_viewport_size({'width': width, 'height': height})
        page.keyboard.press('Home')
        for i in range(9):
            if i:
                page.keyboard.press('ArrowRight')
            page.wait_for_timeout(700)
            assert page.locator('.slide.active').count() == 1
            assert page.locator('#current').inner_text() == f'{i+1:02}'
            stage = page.locator('#stage').bounding_box()
            assert stage['x'] >= -1 and stage['y'] >= -1
            assert stage['x'] + stage['width'] <= width + 1
            assert stage['y'] + stage['height'] <= height + 1
            assert abs(stage['width'] / stage['height'] - 16/9) < .001
            # Compare actual image boxes with the natural image ratio, not just
            # the HTML width/height metadata. The image must fill its figure
            # naturally, occupy a substantial slide area and stay clear of text.
            image_issues = page.locator('.slide.active').evaluate('''slide => {
              const img = slide.querySelector('.film-image');
              const frame = img.closest('.film-frame').getBoundingClientRect();
              const b = img.getBoundingClientRect();
              const stage = document.querySelector('#stage').getBoundingClientRect();
              const problems = [];
              if (Math.abs((b.width/b.height) / (img.naturalWidth/img.naturalHeight) - 1) > .005) problems.push('Image distorted');
              if (Math.abs(b.width-frame.width) > 1 || Math.abs(b.height-frame.height) > 1 || Math.abs(b.left-frame.left) > 1 || Math.abs(b.top-frame.top) > 1) problems.push('Empty space in figure');
              const fraction = b.width / stage.width;
              if (fraction < .449 || fraction > .551) problems.push('Image width outside 45–55% of slide');
              if (b.left < stage.left-1 || b.right > stage.right+1 || b.top < stage.top-1 || b.bottom > stage.bottom+1) problems.push('Image cropped by stage');
              for (const el of slide.querySelectorAll('.reveal,.techniques,.director-years,.corner-note,.award-foot,.thanks')) {
                const t = el.getBoundingClientRect();
                if (b.left < t.right && b.right > t.left && b.top < t.bottom && b.bottom > t.top) problems.push('Image overlaps '+el.className);
              }
              return problems;
            }''')
            assert not image_issues, (width, height, i+1, image_issues)
            overflow = page.locator('.slide.active').evaluate('''slide => {
              const box = slide.getBoundingClientRect();
              return [...slide.querySelectorAll('h1,h2,p,.techniques article')].filter(el => {
                if (getComputedStyle(el).display === 'none') return false;
                const b = el.getBoundingClientRect();
                return b.left < box.left-1 || b.right > box.right+1 || b.top < box.top-1 || b.bottom > box.bottom+1;
              }).map(el => el.textContent);
            }''')
            assert not overflow, (width, i+1, overflow)
            page.screenshot(path=str(OUT / f'{width}x{height}-slide-{i+1}.png'))
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
        assert page.locator('#next').is_disabled()
    page.keyboard.press('Home')
    page.keyboard.press('Space')
    assert page.locator('#current').inner_text() == '02'
    page.locator('#next').focus()
    page.keyboard.press('Space')
    assert page.locator('#current').inner_text() == '03'
    page.keyboard.press('ArrowLeft')
    assert page.locator('#current').inner_text() == '02'
    # Rapid reversal must never leave a returning slide invisible.
    for _ in range(10):
        page.keyboard.press('ArrowRight')
        page.keyboard.press('ArrowLeft')
    page.wait_for_timeout(700)
    assert page.locator('.slide.active').evaluate('el => getComputedStyle(el).opacity') == '1'
    # Native fullscreen API, triggered through the actual keyboard handler.
    page.set_viewport_size({'width': 1280, 'height': 720})
    page.keyboard.press('f')
    page.wait_for_function('!!document.fullscreenElement')
    # fullscreenElement changes before the fullscreenchange event updates ARIA.
    page.wait_for_function("document.querySelector('#fullscreen').getAttribute('aria-pressed') === 'true'")
    full_stage = page.locator('#stage').bounding_box()
    full_viewport = page.locator('#presentation').bounding_box()
    assert full_stage['x'] >= -1 and full_stage['y'] >= -1
    assert full_stage['x'] + full_stage['width'] <= full_viewport['width'] + 1
    assert full_stage['y'] + full_stage['height'] <= full_viewport['height'] + 1
    page.keyboard.press('f')
    page.wait_for_function('!document.fullscreenElement')
    page.wait_for_function("document.querySelector('#fullscreen').getAttribute('aria-pressed') === 'false'")
    page.evaluate('''() => {
      const touch = (x,y) => new Touch({identifier:1,target:document.body,screenX:x,screenY:y});
      document.dispatchEvent(new TouchEvent('touchstart',{changedTouches:[touch(300,200)]}));
      document.dispatchEvent(new TouchEvent('touchend',{changedTouches:[touch(100,205)]}));
    }''')
    assert page.locator('#current').inner_text() == '03'
    page.emulate_media(reduced_motion='reduce')
    page.keyboard.press('ArrowRight')
    assert page.locator('.slide.active').evaluate('el => getComputedStyle(el).transitionDuration') == '0s'
    assert not errors, errors
    browser.close()
print('PASS: all 9 slides at 6 sizes, natural image ratios, close-fitting figures, 45–55% image widths, no cropping or image/text overlap, viewport bounds, keyboard, buttons, native fullscreen, swipe, reduced motion, offline loading and JS errors.')
