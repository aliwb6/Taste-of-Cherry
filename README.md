# Taste of Cherry — classroom presentation

A nine-slide website about Abbas Kiarostami’s *Taste of Cherry* (1997). The slides and [speaking script](speaker-notes.md) use simple A2 English. The spoken script is about 830 words. Read at 105–115 words a minute, with short pauses, for about 8–9 minutes. Practise with a clock before class.

## Open the presentation

Open `index.html` in Chrome, Firefox, Edge, or Safari. Keep `index.html`, `styles.css`, `script.js`, and the `assets` folder together. The presentation needs no internet connection, package installation, or build step.

You can also use a local server:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Then open `http://localhost:8000`.

## Controls

- Right Arrow, Down Arrow, or Space: next slide.
- Left Arrow or Up Arrow: previous slide.
- Home / End: first / last slide.
- F or the Full screen button: full screen on or off. Escape also leaves full screen.
- On a phone: swipe left or right. The arrow buttons also work.

Slides do not change by themselves. The number and line at the bottom show your place. The first and last slides have a disabled back or next button. The site uses a fixed 1920 × 1080 stage. It fits the screen without changing its 16:9 shape. Use landscape orientation on a phone. A laptop or projector is best for presenting. Reduced-motion settings turn off transitions.

## Real film images and credits

Each slide uses the image manually selected in `index.html`. The sizing fix preserves all nine selections and every image file. The film is directed by Abbas Kiarostami, with cinematography by Homayoun Payvar. The original Janus Films source record is in [assets/README.md](assets/README.md); that record predates the later manual image selections.

Images sit inside proportional, centred frames. `object-fit: contain`, automatic dimensions, and maximum frame bounds preserve the full original aspect ratio without cropping or stretching. Small source files stay at or below their native size within the presentation stage; they are not blown up to fill a large screen. Unused space has a subtle matte background. HTML image dimensions match the actual files. Keep those dimensions accurate if you select a new image later.

The design follows the actual photographs: pale dry hills, muted green daylight, earthy cloth, and dark car interiors. Photos keep their original colours. Text sits outside the image frames so faces and details remain visible. The 16:9 stage fits the available space above a separate control area, including on short phone screens. There is no fake scenery, extra film grain, or automatic animation. Text uses local serif and sans-serif font stacks, so no web font download is needed.

**Public image rights are not confirmed.** The distributor offers the files as promotional stills, but supplies no explicit general licence for public website or repository redistribution. Download access and attribution do not grant those rights. The local copy is prepared for the requested classroom discussion. Confirm permitted use with the institution/rightsholder. Before public hosting or public distribution, obtain the needed permission from Janus using the contact details on its film page. Do not treat these images as freely licensed. No public deployment or push containing the photos is part of this update without that clearance.

## Facts and language

Facts were checked against [Janus Films](https://www.janusfilms.com/films/1037), [Criterion](https://www.criterion.com/films/242-taste-of-cherry), [Cannes’s 1997 awards](https://www.festival-cannes.com/en/retrospective/1997/awards/), and [Encyclopaedia Iranica](https://www.iranicaonline.org/articles/kiarostami-abbas/). Cannes confirms the shared Palme d’Or with Shohei Imamura’s *The Eel*. The notes give simple explanations of necessary film terms and names. The film’s ending is not revealed. Personal readings are identified as personal ideas, not film dialogue.

## Checks

No test package is needed to use the website. For the basic file checks:

```bash
node --check script.js
node tests/static-check.mjs
```

The browser check needs Python Playwright and a local Chromium browser. These are testing tools only; they are not website dependencies.

```bash
python3 -m venv /tmp/taste-tests
/tmp/taste-tests/bin/pip install playwright
TASTE_CHROME=/usr/bin/google-chrome-stable /tmp/taste-tests/bin/python tests/browser-check.py
```

Set `TASTE_CHROME` to your Chrome or Chromium executable. The test works offline using `index.html` directly. It checks all nine slides at 1920 × 1080, 1366 × 768, 1280 × 800, 768 × 1024, 390 × 844, and 844 × 390. It checks image loading, natural aspect ratio, no upscaling, frame bounds, no image/text overlap, no horizontal overflow, keyboard and button controls, rapid navigation, native full screen, swipe events, reduced motion, and JavaScript errors. Screenshots go to `/tmp/taste-image-check`.

## GitHub Pages — after image permission is confirmed

1. Confirm permission to publish the image assets.
2. Push the presentation files and `assets` folder to the existing repository.
3. Open repository Settings → Pages.
4. Select Deploy from a branch, `main`, and `/ (root)`.
5. Save and open the URL GitHub shows. Check the photos there too.

No build command is needed. This update does not publish the copyrighted photographs automatically.
