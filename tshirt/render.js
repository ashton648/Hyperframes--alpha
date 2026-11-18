const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1200,height:1052}, deviceScaleFactor:2});
  for (const n of ['navy','white']) {
    await p.goto('file://' + process.cwd() + `/_prev_${n}.svg`);
    await p.screenshot({path:`preview-${n}.png`});
  }
  await b.close();
})();
