const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(800);
await p.screenshot({path:process.argv[3],type:'jpeg',quality:88});await b.close();})();
