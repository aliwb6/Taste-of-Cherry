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

The three photographs come from the **official Janus Films stills download** for this film. They are stored locally at their original resolution (over 3000 pixels wide). They show the soldier in the car, Mr. Bagheri talking, and Mr. Badii at the gates. The film is directed by Abbas Kiarostami, with cinematography by Homayoun Payvar. Stills courtesy of Janus Films; copyright remains with the respective rights holders.

See [assets/README.md](assets/README.md) for the original download URL, original filenames, sizes, slide uses, and permission limits. The package has three high-resolution photos and one very small photo. The small one is not used. Some slides reuse the large photos with different crops. A high-resolution road-only image with clear reuse terms is still missing. No artificial pictures or unrelated stock images replace it.

The design follows the actual photographs: pale dry hills, muted green daylight, earthy cloth, and dark car interiors. Photos keep their original colours. Text has a plain background or dark overlay. There is no fake scenery, extra film grain, or automatic animation. Text uses local serif and sans-serif font stacks, so no web font download is needed.

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

Set `TASTE_CHROME` to your Chrome or Chromium executable. The test works offline using `index.html` directly. It checks all nine slides at 1280 × 720, 1920 × 1080, 1024 × 768, and 390 × 844. It checks image loading, slide and text bounds, keyboard and button controls, rapid navigation, native full screen, swipe events, reduced motion, and JavaScript errors. Screenshots go to `/tmp/taste-check`.

## GitHub Pages — after image permission is confirmed

1. Confirm permission to publish the image assets.
2. Push the presentation files and `assets` folder to the existing repository.
3. Open repository Settings → Pages.
4. Select Deploy from a branch, `main`, and `/ (root)`.
5. Save and open the URL GitHub shows. Check the photos there too.

No build command is needed. This update does not publish the copyrighted photographs automatically.
