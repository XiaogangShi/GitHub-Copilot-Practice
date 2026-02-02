// 扩展安装时的初始化
chrome.runtime.onInstalled.addListener(() => {
    console.log('历史记录隐私查看器已安装');
});

/**
 * 检查URL是否需要过滤
 * @param {string} url - 要检查的URL
 * @returns {boolean} true表示需要过滤，false表示需要记录
 */
function shouldFilterUrl(url) {
    // 过滤chrome://和file://开头的URL
    return url.startsWith('chrome://') || url.startsWith('file://');
}

/**
 * 添加新的历史记录
 * @param {Object} tab - 标签页对象
 */
async function addHistoryRecord(tab) {
    try {
        // 检查URL是否需要过滤
        if (!tab.url || shouldFilterUrl(tab.url)) {
            return;
        }

        // 检查标题是否为空（某些页面可能没有标题）
        const title = tab.title || '无标题';

        // 创建新的历史记录对象
        const newRecord = {
            title: title,
            url: tab.url,
            timestamp: Date.now() // 使用当前时间戳
        };

        // 从存储中获取现有历史记录
        const result = await chrome.storage.local.get(['history']);
        let history = result.history || [];

        // 将新记录添加到数组开头（保证最新的在前面）
        history.unshift(newRecord);

        // 限制记录数量为1000条
        if (history.length > 1000) {
            // 移除最旧的一条记录（数组最后一条）
            history = history.slice(0, 1000);
        }

        // 保存回存储
        await chrome.storage.local.set({ history: history });

        console.log('已添加历史记录:', title);
    } catch (error) {
        console.error('添加历史记录时出错:', error);
    }
}

// 监听标签页更新事件
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    // 只有当页面加载完成时才记录
    if (changeInfo.status === 'complete' && tab.url) {
        addHistoryRecord(tab);
    }
});

// 监听标签页激活事件（处理页面刷新等情况）
chrome.tabs.onActivated.addListener(async (activeInfo) => {
    try {
        const tab = await chrome.tabs.get(activeInfo.tabId);
        if (tab.status === 'complete' && tab.url) {
            addHistoryRecord(tab);
        }
    } catch (error) {
        console.error('获取标签页信息时出错:', error);
    }
});