// Builds a 2-page vector PDF per shirt colour: page 1 = preview on the shirt colour,
// page 2 = print artwork with a transparent background, at 30 cm wide.
const { chromium } = require('playwright');
const fs = require('fs');
const WIDTH_MM = 300;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  for (const [name, shirt] of [['navy', '#0B2545'], ['white', '#FFFFFF']]) {
    const svg = fs.readFileSync(`back-print-${name}-shirt.svg`, 'utf8');
    const [, w, h] = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).map(Number);
    const hmm = (WIDTH_MM * h / w).toFixed(2);
    const art = svg.replace(/width="[\d.]+" height="[\d.]+"/, 'width="100%" height="100%"');
    await p.setContent(`<!DOCTYPE html><html><head><style>
      @page { size: ${WIDTH_MM}mm ${hmm}mm; margin: 0 }
      html, body { margin: 0 }
      .pg { width: ${WIDTH_MM}mm; height: ${hmm}mm; overflow: hidden; page-break-after: always }
      .pg:last-child { page-break-after: auto }
      svg { display: block }
    </style></head><body>
      <div class="pg" style="background:${shirt}">${art}</div>
      <div class="pg">${art}</div>
    </body></html>`);
    await p.pdf({ path: `alpha-tshirt-back-${name}.pdf`, width: `${WIDTH_MM}mm`, height: `${hmm}mm`,
                  printBackground: true, omitBackground: true, preferCSSPageSize: true });
  }
  await b.close();
})();
