import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const css = readFileSync(new URL('../styles.css', import.meta.url), 'utf8');
const js = readFileSync(new URL('../script.js', import.meta.url), 'utf8');
const slides = (html.match(/<section class="slide/g) || []).length;

if (slides !== 9) throw new Error(`Expected 9 slides, found ${slides}.`);
for (const required of ['ArrowRight', "' '", 'touchstart', 'requestFullscreen', 'aria-label', 'prefers-reduced-motion']) {
  if (!(html + css + js).includes(required)) throw new Error(`Missing expected feature: ${required}`);
}
if (css.includes('@import') || /(?:src|href|url)\s*=\s*["']https?:|url\(["']?https?:/i.test(html + css + js)) throw new Error('Presentation must not depend on network assets.');
console.log('Static presentation checks passed: 9 slides, offline assets, navigation, fullscreen, swipe, and reduced motion hooks present.');
