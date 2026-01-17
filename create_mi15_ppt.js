const pptxgen = require('pptxgenjs');
const html2pptx = require('./skills/pptx/scripts/html2pptx.js');

async function createPresentation() {
  const pptx = new pptxgen();
  pptx.layout = 'LAYOUT_16x9';
  pptx.author = 'Xiaomi';
  pptx.title = '小米手机15介绍';

  // Slide 1: 封面
  await html2pptx('mi15-slide1.html', pptx);

  // Slide 2: 产品概览
  await html2pptx('mi15-slide2.html', pptx);

  // Slide 3: 核心参数（含表格）
  const { slide: slide3, placeholders } = await html2pptx('mi15-slide3.html', pptx);

  const specsTable = [
    [
      { text: '参数类别', options: { fill: { color: '1A1A1A' }, color: 'FFFFFF', bold: true, fontSize: 16 } },
      { text: '规格', options: { fill: { color: '1A1A1A' }, color: 'FFFFFF', bold: true, fontSize: 16 } }
    ],
    ['处理器', '骁龙8 Gen 3'],
    ['屏幕', '6.73英寸 AMOLED 2K 120Hz'],
    ['主摄', '5000万像素 徕卡专业镜头'],
    ['长焦', '75mm 徕卡长焦镜头'],
    ['电池', '5100mAh'],
    ['充电', '120W有线秒充 + 50W无线充电'],
    ['防护', 'IP68防尘防水'],
    ['系统', 'MIUI 15（基于Android 14）']
  ];

  slide3.addTable(specsTable, {
    ...placeholders[0],
    colW: [2.5, 5.5],
    border: { pt: 1, color: 'CCCCCC' },
    fill: { color: 'FFFFFF' },
    fontSize: 14,
    valign: 'middle'
  });

  // Slide 4: 特色功能
  await html2pptx('mi15-slide4.html', pptx);

  // Save
  await pptx.writeFile({ fileName: '小米手机15介绍.pptx' });
  console.log('PPT已生成：小米手机15介绍.pptx');
}

createPresentation().catch(console.error);
