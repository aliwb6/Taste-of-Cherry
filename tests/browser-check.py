"""Run with Python Playwright and a locally installed Chromium browser.

TASTE_CHROME can point to a Chromium executable. No server is needed.
Screenshots are written outside the repository, under /tmp/taste-check.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = Path('/tmp/taste-check')
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
    for width, height in [(1280, 720), (1920, 1080), (1024, 768), (390, 844)]:
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
            overflow = page.locator('.slide.active').evaluate('''slide => {
              const box = slide.getBoundingClientRect();
              return [...slide.querySelectorAll('h1,h2,p,.techniques article')].filter(el => {
                if (getComputedStyle(el).display === 'none') return false;
                const b = el.getBoundingClientRect();
                return b.left < box.left-1 || b.right > box.right+1 || b.top < box.top-1 || b.bottom > box.bottom+1;
              }).map(el => el.textContent);
            }''')
            assert not overflow, (width, i+1, overflow)
            if width in (1280, 390):
                page.screenshot(path=str(OUT / f'{width}-slide-{i+1}.png'))
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
print('PASS: offline images, all 9 slides at 4 sizes, text bounds, keyboard, buttons, rapid navigation, native fullscreen, swipe, reduced motion, and JS errors.')
