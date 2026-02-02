// create-table.js
// 使用ExcelJS库创建指定格式的Excel表格

const ExcelJS = require('exceljs');
const path = require('path');

/**
 * 创建Excel表格文件
 * 生成一个10行4列带边框的空白表格
 */
async function createExcelTable() {
  try {
    // 1. 创建新工作簿
    const workbook = new ExcelJS.Workbook();

    // 2. 添加工作表并命名为"表格"
    const worksheet = workbook.addWorksheet('表格');

    // 3. 设置表头
    worksheet.columns = [
      { header: 'ID', key: 'id', width: 10 },
      { header: 'Name', key: 'name', width: 20 },
      { header: 'Sex', key: 'sex', width: 10 },
      { header: 'Salary', key: 'salary', width: 15 }
    ];

    // 4. 生成随机数据
    const names = ['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Frank', 'Grace', 'Henry', 'Ivy', 'Jack'];
    const sexes = ['Male', 'Female'];

    for (let i = 1; i <= 10; i++) {
      const randomName = names[Math.floor(Math.random() * names.length)];
      const randomSex = sexes[Math.floor(Math.random() * sexes.length)];
      const randomSalary = Math.floor(Math.random() * 50000) + 50000;

      worksheet.addRow({
        id: i,
        name: randomName,
        sex: randomSex,
        salary: randomSalary
      });
    }

    // 5. 设置边框样式
    worksheet.eachRow((row, rowNumber) => {
      row.eachCell((cell, colNumber) => {
        cell.border = {
          top: { style: 'thin' },
          left: { style: 'thin' },
          bottom: { style: 'thin' },
          right: { style: 'thin' }
        };
      });
    });

    // 6. 保存文件到当前目录
    const filePath = path.join(process.cwd(), 'table.xlsx');
    await workbook.xlsx.writeFile(filePath);

    console.log(`✅ Excel文件创建成功：${filePath}`);
    console.log('📋 工作表名称：表格');
    console.log('� 包含字段：ID, Name, Sex, Salary');
    console.log('� 数据：随机生成 10 条数据');

  } catch (error) {
    console.error('❌ 创建Excel文件时发生错误：', error.message);
    process.exit(1);
  }
}

// 执行主函数
createExcelTable();