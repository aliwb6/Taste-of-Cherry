# Taste of Cherry — cinematic classroom deck

An offline-ready, full-screen presentation website about Abbas Kiarostami’s *Taste of Cherry* (1997). It has nine fixed-ratio slides and matching speaker notes for a 7–9 minute English-language classroom presentation.

## Run locally

No package installation or build step is required. Open `index.html` directly in a modern browser, or serve the folder:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Controls

- `Right Arrow`, `Down Arrow`, or `Space`: next slide
- `Left Arrow` or `Up Arrow`: previous slide
- `Home` / `End`: first / last slide
- `F`: toggle browser fullscreen
- On mobile: swipe left or right
- On screen: use the circular arrow buttons or Fullscreen control

The deck has no autoplay. It scales one 1920 × 1080 stage to fit any display, keeping the intended 16:9 composition. It also honors the operating system’s reduced-motion preference.

## Content and asset credits

The presentation uses original CSS-composed landscapes and film-grain texture, rather than film stills or unrelated stock photography. This keeps the deck fully functional offline and avoids distributing copyrighted film imagery. The visual language is an original response to the film’s arid landscapes and contemplative pacing; it does not recreate individual shots.

Factual material was checked against [The Criterion Collection](https://www.criterion.com/films/242-taste-of-cherry), [Encyclopaedia Iranica](https://www.iranicaonline.org/articles/kiarostami-abbas/), and [Cinema Iranica](https://cinema.iranicaonline.org/article/ta%CA%BBm-i-gilas-taste-of-cherry-1997/). See `speaker-notes.md` for source notes.

## Deploy to GitHub Pages

1. Push this folder to a GitHub repository.
2. In the repository, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select the branch containing this project (usually `main`) and the `/ (root)` folder, then save.
5. GitHub will publish `index.html` at the URL shown on that page.

Because this is static HTML, CSS, and JavaScript, no special build configuration is needed.
