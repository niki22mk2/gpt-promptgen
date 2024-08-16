document.addEventListener('DOMContentLoaded', (event) => {
    // プロンプト履歴の折りたたみ機能
    const historyAccordion = document.querySelector('#request-history-accordion');
    if (historyAccordion) {
        historyAccordion.addEventListener('click', () => {
            const content = historyAccordion.nextElementSibling;
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
        });
    }

    // プロンプトのコピー機能
    const copyButton = document.createElement('button');
    copyButton.textContent = 'Copy Prompt';
    copyButton.classList.add('gr-button', 'gr-button-secondary');
    copyButton.style.marginLeft = '10px';

    const generatedPromptTextarea = document.querySelector('#generated-prompt textarea');
    if (generatedPromptTextarea) {
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
});