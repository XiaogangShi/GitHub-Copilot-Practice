document.addEventListener('DOMContentLoaded', () => {
    // 1. 获取 DOM 元素
    const track = document.querySelector('.carousel-track');
    const slides = Array.from(track.children);
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');
    const indicatorsContainer = document.getElementById('indicators');
    const container = document.querySelector('.carousel-container');

    // 2. 初始化变量
    const slideWidth = slides[0].getBoundingClientRect().width; // 获取宽度 (800px)
    let currentIndex = 0;
    let autoPlayInterval;
    const totalSlides = slides.length;
    const autoPlayDelay = 3000; // 3秒

    // 3. 动态生成底部圆点指示器
    slides.forEach((_, index) => {
        const indicator = document.createElement('div');
        indicator.classList.add('indicator');
        if (index === 0) indicator.classList.add('active'); // 默认第一个高亮

        // 点击圆点切换
        indicator.addEventListener('click', () => {
            currentIndex = index;
            updateCarousel();
        });

        indicatorsContainer.appendChild(indicator);
    });

    // 获取生成后的所有圆点 DOM
    const indicators = Array.from(document.querySelectorAll('.indicator'));

    // 4. 核心更新函数：移动轨道 & 更新圆点
    const updateCarousel = () => {
        // 移动轨道：通过 translateX 平移
        // 例如：index 为 1 时，向左移动 800px
        const amountToMove = -(slideWidth * currentIndex);
        track.style.transform = `translateX(${amountToMove}px)`;

        // 更新圆点高亮
        indicators.forEach(ind => ind.classList.remove('active'));
        indicators[currentIndex].classList.add('active');
    };

    // 5. 切换逻辑
    const moveToNextSlide = () => {
        if (currentIndex === totalSlides - 1) {
            currentIndex = 0; // 如果是最后一张，回到第一张
        } else {
            currentIndex++;
        }
        updateCarousel();
    };

    const moveToPrevSlide = () => {
        if (currentIndex === 0) {
            currentIndex = totalSlides - 1; // 如果是第一张，跳到最后一张
        } else {
            currentIndex--;
        }
        updateCarousel();
    };

    // 6. 事件监听：左右按钮
    nextBtn.addEventListener('click', () => {
        moveToNextSlide();
        resetTimer(); // 手动点击后重置计时器，避免立即自动切换
    });

    prevBtn.addEventListener('click', () => {
        moveToPrevSlide();
        resetTimer();
    });

    // 7. 自动播放逻辑
    const startAutoPlay = () => {
        autoPlayInterval = setInterval(moveToNextSlide, autoPlayDelay);
    };

    const stopAutoPlay = () => {
        clearInterval(autoPlayInterval);
    };

    // 辅助函数：手动操作时重置计时器
    const resetTimer = () => {
        stopAutoPlay();
        startAutoPlay();
    };

    // 8. 鼠标悬停控制
    // 鼠标移入轮播图 -> 停止自动播放
    container.addEventListener('mouseenter', stopAutoPlay);
    // 鼠标移出轮播图 -> 恢复自动播放
    container.addEventListener('mouseleave', startAutoPlay);

    // 9. 启动程序
    startAutoPlay();
});
