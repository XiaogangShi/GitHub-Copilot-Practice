// 当扩展安装或更新时执行
chrome.runtime.onInstalled.addListener(() => {
  // 创建一个右键菜单项
  chrome.contextMenus.create({
    id: "openBaiduTranslate", // 菜单项的唯一ID
    title: "翻译",           // 菜单项显示的文本
    // 显示条件：在任何地方都显示，但特别是当有文本选中时，更相关
    contexts: ["selection", "page"] // 在选中文字或页面空白处显示
  });
});

// 监听右键菜单项的点击事件
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "openBaiduTranslate") {
    // 基础的百度翻译 URL
    const baiduTranslateBaseUrl = "https://fanyi.baidu.com/mtpe-individual/transText?ext_channel=DuSearch";
    let targetUrl = baiduTranslateBaseUrl;

    // 检查是否有选中的文本
    if (info.selectionText) {
      // 对选中的文本进行 URL 编码，以确保特殊字符能正确传递
      const encodedSelection = encodeURIComponent(info.selectionText);
      // 拼接 URL，加入查询参数和翻译语言（根据您的示例，默认为英译中）
      targetUrl = `${baiduTranslateBaseUrl}&query=${encodedSelection}&lang=en2zh`;
    }

    // 在新窗口中打开目标 URL
    chrome.windows.create({
      url: targetUrl,
      type: "normal" // 可以是 "normal", "popup", "panel", "detached_panel"
    });
  }
});
