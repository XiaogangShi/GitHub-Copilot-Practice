document.addEventListener('DOMContentLoaded', () => {
    // 获取 DOM 元素
    const redSlider = document.getElementById('red-slider');
    const greenSlider = document.getElementById('green-slider');
    const blueSlider = document.getElementById('blue-slider');

    const redValDisplay = document.getElementById('red-val');
    const greenValDisplay = document.getElementById('green-val');
    const blueValDisplay = document.getElementById('blue-val');

    const colorDisplay = document.getElementById('color-display');
    const hexLabel = document.getElementById('hex-label');

    // 更新颜色的函数
    function updateColor() {
        // 获取当前滑块的值
        const r = parseInt(redSlider.value);
        const g = parseInt(greenSlider.value);
        const b = parseInt(blueSlider.value);

        // 更新滑块旁边的数字显示
        redValDisplay.textContent = r;
        greenValDisplay.textContent = g;
        blueValDisplay.textContent = b;

        // 生成 RGB 字符串和 Hex 字符串
        const rgbColor = `rgb(${r}, ${g}, ${b})`;
        const hexColor = rgbToHex(r, g, b);

        // 应用背景颜色
        colorDisplay.style.backgroundColor = rgbColor;

        // 更新十六进制标签文本
        hexLabel.textContent = hexColor;

        // 计算对比度颜色（决定文字是黑还是白），以便在深色背景上能看清文字
        const textColor = getContrastingTextColor(r, g, b);
        colorDisplay.style.color = textColor;
    }

    // 辅助函数：RGB 转 Hex
    function rgbToHex(r, g, b) {
        return "#" + [r, g, b].map(x => {
            const hex = x.toString(16);
            return hex.length === 1 ? '0' + hex : hex;
        }).join('');
    }

    // 辅助函数：计算对比色 (简单的亮度公式)
    function getContrastingTextColor(r, g, b) {
        // 相对亮度公式: 0.299*R + 0.587*G + 0.114*B
        const brightness = (r * 299 + g * 587 + b * 114) / 1000;
        return brightness > 128 ? 'black' : 'white';
    }

    // 添加事件监听
    redSlider.addEventListener('input', updateColor);
    greenSlider.addEventListener('input', updateColor);
    blueSlider.addEventListener('input', updateColor);

    // 初始化一次
    updateColor();
});
