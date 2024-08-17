console.log('LLM Prompt Artisan script loaded');

/**
 * wait until element is loaded and returns
 * @param {string} selector
 * @param {number} timeout 
 * @param {Element} $rootElement
 * @returns {Promise<HTMLElement>}
 */
function waitQuerySelector(selector, timeout = 5000, $rootElement = gradioApp()) {
    return new Promise((resolve, reject) => {
        const element = $rootElement.querySelector(selector)
        if (element) {
            return resolve(element)
        }

        let timeoutId

        const observer = new MutationObserver(() => {
            const element = $rootElement.querySelector(selector)
            if (!element) {
                return
            }

            if (timeoutId) {
                clearTimeout(timeoutId)
            }

            observer.disconnect()
            resolve(element)
        })

        timeoutId = setTimeout(() => {
            observer.disconnect()
            reject(new Error(`timeout, cannot find element by '${selector}'`))
        }, timeout)

        observer.observe($rootElement, {
            childList: true,
            subtree: true
        })
    })
}

function updateRequestHistory(newHistory, currentPage, totalPages) {
    waitQuerySelector('#request-history-content').then((historyContent) => {
        historyContent.innerHTML = newHistory;
    }).catch((error) => {
        console.error('Error updating request history:', error);
    });

    waitQuerySelector('#page-info').then((pageInfo) => {
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;
    }).catch((error) => {
        console.error('Error updating page info:', error);
    });

    // 非表示の要素も更新
    waitQuerySelector('input[data-testid="Number"]').then((currentPageInput) => {
        currentPageInput.value = currentPage;
    }).catch((error) => {
        console.error('Error updating current page:', error);
    });

    waitQuerySelector('input[data-testid="Number"]', 5000, gradioApp().querySelector('#pagination-row')).then((totalPagesInput) => {
        totalPagesInput.value = totalPages;
    }).catch((error) => {
        console.error('Error updating total pages:', error);
    });
}

function addCopyButton() {
    waitQuerySelector('#generated-prompt label').then((labelElement) => {
        if (!labelElement.querySelector('.copy-button')) {
            const copyButton = document.createElement('button');
            copyButton.textContent = '📋';
            copyButton.className = 'copy-button';

            // ラベルの最初のspan要素（既存のラベルテキスト）を見つける
            const labelSpan = labelElement.querySelector('span[data-testid="block-info"]');
            if (labelSpan) {
                // 既存のwrapperを使用するか、新しく作成する
                let wrapper = labelElement.querySelector('.label-wrapper');
                if (!wrapper) {
                    wrapper = document.createElement('div');
                    wrapper.className = 'label-wrapper';
                    labelSpan.parentNode.insertBefore(wrapper, labelSpan);
                    wrapper.appendChild(labelSpan);
                }
                
                // コピーボタンを追加
                wrapper.appendChild(copyButton);
            }

            copyButton.addEventListener('click', function(e) {
                e.preventDefault(); // デフォルトの動作を防止
                const textArea = labelElement.querySelector('textarea');
                navigator.clipboard.writeText(textArea.value).then(function() {
                    const originalText = copyButton.textContent;
                    copyButton.textContent = "✓";
                    copyButton.disabled = true;
                    setTimeout(function() {
                        copyButton.textContent = originalText;
                        copyButton.disabled = false;
                    }, 2000);
                });
            });
        }
    }).catch((error) => {
        console.error('Error adding copy button:', error);
    });
}

function onUiLoaded() {
    console.log('LLM Prompt Artisan UI loaded');
    addCopyButton();
}

// DOMContentLoadedイベントとGradioのuiUpdateイベントの両方でonUiLoadedを呼び出す
document.addEventListener('DOMContentLoaded', onUiLoaded);

// Gradio の UI 更新後にも実行されるようにする
(function() {
    const originalUpdateInput = updateInput;
    updateInput = function() {
        originalUpdateInput.apply(this, arguments);
        onUiLoaded();
    }
})();

// Gradioのイベントを使用してプロンプト生成時に履歴を更新
document.addEventListener('gradioUpdated', function(event) {
    if (event.detail && event.detail.output) {
        const outputs = event.detail.output;
        if (outputs.length >= 7) {  // generate_prompt_wrapperの出力数に基づいて
            const request_history = outputs[2];
            const current_page = outputs[5];
            const total_pages = outputs[6];
            if (request_history) {
                updateRequestHistory(request_history, current_page, total_pages);
            }
        }
    }
});