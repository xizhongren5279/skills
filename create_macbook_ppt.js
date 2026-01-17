const pptxgen = require('pptxgenjs');
const html2pptx = require('./skills/pptx/scripts/html2pptx');
const path = require('path');

async function createPresentation() {
    const pptx = new pptxgen();
    pptx.layout = 'LAYOUT_16x9';
    pptx.author = 'Claude';
    pptx.title = 'Apple MacBook 产品介绍';

    // Slide 1: 封面
    await html2pptx('macbook-slide1.html', pptx);

    // Slide 2: 产品特点
    await html2pptx('macbook-slide2.html', pptx);

    // Slide 3: 系列对比
    await html2pptx('macbook-slide3.html', pptx);

    // Save
    await pptx.writeFile({ fileName: 'MacBook_产品介绍.pptx' });
    console.log('演示文稿创建成功: MacBook_产品介绍.pptx');
}

createPresentation().catch(console.error);
