// 获取显示框元素
const display = document.getElementById('display');

// 允许的字符集合（数字、运算符、小数点）
const allowedChars = new Set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '+', '-', '*', '/']);

/**
 * 向显示框添加字符
 * @param {string} char
 */
function appendChar(char) {
    if (allowedChars.has(char)) {
        display.value += char;
    }
}

/**
 * 计算表达式结果
 */
function calculate() {
    try {
        const expression = display.value;
        if (!expression) return;

        // 使用 Function 来替代 eval，相对安全一点，但仍然要小心
        // 注意：这是一个简单演示，生产环境应使用更安全的解析库
        const result = new Function('return ' + expression)();

        display.value = result;
    } catch (e) {
        alert("错误: 无效的表达式");
        display.value = "";
    }
}

/**
 * 清除显示框
 */
function clearDisplay() {
    display.value = "";
}

/**
 * 处理退格（删除最后一个字符）
 */
function backspace() {
    display.value = display.value.slice(0, -1);
}

// --- 事件监听 ---

// 1. 双击输入框清空内容
display.addEventListener('dblclick', clearDisplay);

// 2. 键盘事件监听
document.addEventListener('keydown', (event) => {
    const key = event.key;

    // 如果按下的是允许的字符，且不是在输入框中直接输入（避免重复）
    // 为了简化逻辑，我们让 readonly 输入框只能通过 JS 修改，
    // 所以这里捕获键盘按键并手动添加
    if (allowedChars.has(key)) {
        appendChar(key);
    }
    // 回车键 -> 计算
    else if (key === 'Enter') {
        event.preventDefault(); // 防止表单提交等默认行为
        calculate();
    }
    // 退格键 -> 删除最后一个字符
    else if (key === 'Backspace') {
        event.preventDefault(); // 防止页面后退
        backspace();
    }
    // 'c' 或 'C' -> 清空
    else if (key.toLowerCase() === 'c') {
        clearDisplay();
    }
});
