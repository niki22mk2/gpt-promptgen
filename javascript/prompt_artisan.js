console.log('LLM Prompt Artisan script loaded');

function waitForElement(selector, timeout = 10000) {
    return new Promise((resolve, reject) => {
        const observer = new MutationObserver(() => {
            const element = document.querySelector(selector);
            if (element) {
                observer.disconnect();
                resolve(element);
            }
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        setTimeout(() => {
            observer.disconnect();
            reject(new Error(`Timeout waiting for element: ${selector}`));
        }, timeout);
    });
}

function addCopyButton() {
    waitForElement('#generated-prompt textarea')
        .then((generatedPromptTextarea) => {
            if (!generatedPromptTextarea.parentNode.querySelector('.copy-prompt-button')) {
                const copyButton = document.createElement('button');
                copyButton.textContent = 'Copy Prompt';
                copyButton.classList.add('gr-button', 'gr-button-secondary', 'copy-prompt-button');
                copyButton.style.marginLeft = '10px';

                generatedPromptTextarea.parentNode.insertBefore(copyButton, generatedPromptTextarea.nextSibling);

                copyButton.addEventListener('click', () => {
                    navigator.clipboard.writeText(generatedPromptTextarea.value).then(() => {
                        copyButton.textContent = 'Copied!';
                        setTimeout(() => {
                            copyButton.textContent = 'Copy Prompt';
                        }, 2000);
                    });
                });
            }
        })
        .catch((error) => {
            console.error('Error adding copy button:', error);
        });
}

function onUiLoaded() {
    addCopyButton();
}

document.addEventListener('DOMContentLoaded', onUiLoaded);

// Gradio の UI 更新後にも実行されるようにする
(function() {
    const originalUpdateInput = updateInput;
    updateInput = function() {
        originalUpdateInput.apply(this, arguments);
        onUiLoaded();
    }
})();