// 等待DOM加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const historyList = document.getElementById('historyList');
    const searchInput = document.getElementById('searchInput');
    const clearAllBtn = document.getElementById('clearAllBtn');
    const emptyState = document.getElementById('emptyState');

    // 存储当前显示的历史记录
    let currentHistory = [];

    /**
     * 初始化扩展
     */
    function init() {
        loadHistory();
        setupEventListeners();
    }

    /**
     * 从存储中加载历史记录
     */
    function loadHistory() {
        chrome.storage.local.get(['history'], function(result) {
            const history = result.history || [];
            currentHistory = history;
            renderHistory(history);
        });
    }

    /**
     * 渲染历史记录列表
     * @param {Array} history - 历史记录数组
     */
    function renderHistory(history) {
        // 清空当前列表
        historyList.innerHTML = '';

        // 如果没有记录，显示空状态
        if (history.length === 0) {
            emptyState.style.display = 'block';
            historyList.style.display = 'none';
            return;
        }

        // 隐藏空状态，显示列表
        emptyState.style.display = 'none';
        historyList.style.display = 'block';

        // 按时间降序排序（最新的在前面）
        const sortedHistory = [...history].sort((a, b) => b.timestamp - a.timestamp);

        // 创建并添加每个历史记录项
        sortedHistory.forEach(record => {
            const item = createHistoryItem(record);
            historyList.appendChild(item);
        });
    }

    /**
     * 创建单个历史记录项的DOM元素
     * @param {Object} record - 历史记录对象
     * @returns {HTMLElement} 历史记录项元素
     */
    function createHistoryItem(record) {
        const item = document.createElement('div');
        item.className = 'history-item';

        // 创建标题链接
        const titleLink = document.createElement('a');
        titleLink.className = 'history-title';
        titleLink.href = record.url;
        titleLink.textContent = record.title || '无标题';
        titleLink.title = record.title || '无标题';

        // 点击标题在新标签页打开链接
        titleLink.addEventListener('click', function(e) {
            e.preventDefault();
            chrome.tabs.create({ url: record.url, active: false });
        });

        // 创建时间显示
        const timeSpan = document.createElement('span');
        timeSpan.className = 'history-time';
        timeSpan.textContent = formatTimestamp(record.timestamp);

        // 组装元素
        item.appendChild(titleLink);
        item.appendChild(timeSpan);

        return item;
    }

    /**
     * 格式化时间戳为 YYYY-MM-DD HH:MM:SS 格式
     * @param {number} timestamp - 时间戳
     * @returns {string} 格式化后的时间字符串
     */
    function formatTimestamp(timestamp) {
        const date = new Date(timestamp);

        // 补零函数
        const pad = (num) => num.toString().padStart(2, '0');

        const year = date.getFullYear();
        const month = pad(date.getMonth() + 1);
        const day = pad(date.getDate());
        const hours = pad(date.getHours());
        const minutes = pad(date.getMinutes());
        const seconds = pad(date.getSeconds());

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    }

    /**
     * 根据搜索关键词过滤历史记录
     * @param {string} keyword - 搜索关键词
     */
    function filterHistory(keyword) {
        if (!keyword.trim()) {
            // 如果关键词为空，显示所有记录
            renderHistory(currentHistory);
            return;
        }

        const lowerKeyword = keyword.toLowerCase();
        const filtered = currentHistory.filter(record => {
            const title = record.title || '';
            return title.toLowerCase().includes(lowerKeyword);
        });

        renderHistory(filtered);
    }

    /**
     * 设置事件监听器
     */
    function setupEventListeners() {
        // 搜索框输入事件
        searchInput.addEventListener('input', function(e) {
            filterHistory(e.target.value);
        });

        // 清除所有记录按钮点击事件
        clearAllBtn.addEventListener('click', function() {
            if (confirm('确定要清除所有历史记录吗？此操作不可撤销。')) {
                chrome.storage.local.remove('history', function() {
                    currentHistory = [];
                    renderHistory([]);
                    searchInput.value = '';
                });
            }
        });
    }

    // 初始化扩展
    init();
});