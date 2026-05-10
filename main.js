document.querySelectorAll("button[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const text = button.getAttribute("data-copy");

    try {
      await navigator.clipboard.writeText(text);

      const originalText = button.textContent;
      button.textContent = "Skopiowano!";
      button.classList.add("copied");

      setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove("copied");
      }, 1800);
    } catch (error) {
      alert("Nie udało się skopiować. Zaznacz tekst ręcznie i wybierz Kopiuj.");
    }
  });
});