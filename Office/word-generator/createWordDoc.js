// createWordDoc.js
const officegen = require('officegen');
const fs = require('fs');
const path = require('path');

// 1. 设置工作目录为脚本所在目录
const scriptDir = __dirname;
const outputFilePath = path.join(scriptDir, 'my_ai_doc.docx');

console.log('开始创建文档...');

// 2. 创建Word文档对象
const docx = officegen('docx');

// 3. 创建段落并添加格式化文本
const paragraph = docx.createP();

// 默认格式部分："地到无边 "
paragraph.addText('地到无边 ', { font_face: '宋体' });

// "天作界" - 红色一号字
const redStyle = {
  font_face: '宋体',
  color: 'ff0000',    // 红色
  font_size: 36       // 一号字（36磅）
};
paragraph.addText('天', redStyle);
paragraph.addText('作', redStyle);
paragraph.addText('界', redStyle);

// 默认格式部分：" 山登绝顶 "
paragraph.addText(' 山登绝顶 ', { font_face: '宋体' });

// "我为峰" - 黄字蓝底带下划线
const yellowBlueStyle = {
  font_face: '宋体',
  color: 'ffff00',    // 黄色文字
  back: '0000ff',     // 蓝色背景
  underline: true     // 单下划线
};
paragraph.addText('我', yellowBlueStyle);
paragraph.addText('为', yellowBlueStyle);
paragraph.addText('峰', yellowBlueStyle);

// 4. 创建输出流并生成文档
const outputStream = fs.createWriteStream(outputFilePath);
docx.generate(outputStream);

// 5. 事件处理
outputStream.on('close', function() {
  console.log(`文档创建成功，已保存至：${outputFilePath}`);
});

docx.on('error', function(err) {
  console.error('创建文档时发生错误:', err);
});

// 处理officegen完成事件
docx.on('finalize', function() {
  console.log('文档生成完成');
});