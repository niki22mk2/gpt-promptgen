document.addEventListener('DOMContentLoaded', (event) => {
    // コピーボタンの追加を遅延させる
    setTimeout(() => {
        const generatedPromptTextarea = document.querySelector('#generated-prompt textarea');
        if (generatedPromptTextarea) {
            const copyButton = document.createElement('button');
            copyButton.textContent = 'Copy Prompt';
            copyButton.classList.add('gr-button', 'gr-button-secondary');
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
        } else {
            console.error('Generated prompt textarea not found');
        }
    }, 1000); // 1秒後に実行
});