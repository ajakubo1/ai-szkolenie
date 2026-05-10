function showCopiedState(button, originalText) {
    button.textContent = 'Skopiowano!';
    button.classList.add('copied');

    window.setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('copied');
    }, 1800);
}

async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return;
    }

    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.setAttribute('readonly', '');
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';

    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
}

document.querySelectorAll('.copy-button').forEach((button) => {
    button.addEventListener('click', async () => {
        const card = button.closest('.prompt-card');
        const promptText = card.querySelector('.prompt-text').innerText.trim();
        const originalText = 'Kopiuj prompt';

        try {
            await copyText(promptText);
            showCopiedState(button, originalText);
        } catch (error) {
            alert('Nie udało się skopiować. Zaznacz tekst ręcznie i wybierz Kopiuj.');
        }
    });
});

document.querySelectorAll('.quick-copy').forEach((button) => {
    button.addEventListener('click', async () => {
        const text = button.innerText.trim();
        const originalHtml = button.innerHTML;

        try {
            await copyText(text);
            button.innerHTML = '<span>Skopiowano!</span>';
            button.classList.add('copied');

            window.setTimeout(() => {
                button.innerHTML = originalHtml;
                button.classList.remove('copied');
            }, 1800);
        } catch (error) {
            alert('Nie udało się skopiować. Zaznacz tekst ręcznie i wybierz Kopiuj.');
        }
    });
});