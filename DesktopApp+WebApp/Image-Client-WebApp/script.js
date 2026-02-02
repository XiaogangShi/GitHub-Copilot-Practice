document.addEventListener('DOMContentLoaded', () => {
    // 获取 DOM 元素
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const resultList = document.getElementById('result-list');
    const previewImg = document.getElementById('preview-img');
    const previewText = document.getElementById('preview-text');

    // 配置后端地址
    // server 运行在 1234 端口
    const API_BASE_URL = 'http://127.0.0.1:1234/images';

    // 执行搜索
    function performSearch() {
        const query = searchInput.value.trim();
        if (!query) {
            alert('请输入内容');
            return;
        }

        // 清空并显示状态
        resultList.innerHTML = '';
        const statusLi = document.createElement('li');
        statusLi.textContent = `正在搜索: ${query}...`;
        statusLi.style.fontWeight = 'bold';
        resultList.appendChild(statusLi);

        // 发起网络请求
        fetch(`${API_BASE_URL}/search?query=${encodeURIComponent(query)}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.text(); 
            })
            .then(dataText => {
                resultList.innerHTML = ''; // Clear loading

                const parts = dataText.split(',').map(s => s.trim()).filter(s => s);
                if (!dataText || parts.length === 0) {
                    const li = document.createElement('li');
                    li.textContent = `未找到与 '${query}' 匹配的图像`;
                    resultList.appendChild(li);
                    return;
                }

                // 添加结果
                parts.forEach(relPath => {
                    // relPath e.g. "images/cat.jpg"
                    let fileName = relPath;
                    if (fileName.startsWith('images/')) fileName = fileName.substring(7);
                    
                    const fileUrl = `http://127.0.0.1:1234/images/${encodeURIComponent(fileName)}`;
                    const viewUrl = `http://127.0.0.1:1234/images/view/${encodeURIComponent(fileName)}`;

                    const li = document.createElement('li');
                    li.textContent = `📷 ${fileName}`;
                    
                    li.onclick = () => {
                         // Select
                         document.querySelectorAll('#result-list li').forEach(el => el.classList.remove('selected'));
                         li.classList.add('selected');
                         // Show
                         previewText.style.display = 'none';
                         previewImg.src = fileUrl;
                         previewImg.style.display = 'block';
                    };
                    
                    li.ondblclick = () => {
                         window.open(viewUrl, '_blank');
                    };

                    resultList.appendChild(li);
                });
            })
            .catch(error => {
                console.error('搜索失败:', error);
                resultList.innerHTML = '';
                const li = document.createElement('li');
                li.textContent = `连接失败: ${error.message}`;
                li.style.color = 'red';
                resultList.appendChild(li);
            });
    }

    // 绑定事件：点击按钮
    searchBtn.addEventListener('click', performSearch);

    // 绑定事件：回车键
    searchInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            performSearch();
        }
    });
});
