const gateButton = document.querySelector(".gate-btn");
const DAMNED_KEY = "damned_usernames";

if (gateButton) {
  gateButton.addEventListener("click", (event) => {
    event.preventDefault();

    const username = window.prompt("Enter your username:");
    if (username === null) {
      window.location.href = gateButton.href;
      return;
    }

    const normalized = username.trim();
    if (!normalized) {
      window.location.href = gateButton.href;
      return;
    }

    const existing = window.localStorage.getItem(DAMNED_KEY) || "";
    const updated = `${existing}${normalized}\n`;
    window.localStorage.setItem(DAMNED_KEY, updated);

    const blob = new Blob([updated], { type: "text/plain;charset=utf-8" });
    const downloadUrl = window.URL.createObjectURL(blob);
    const downloadLink = document.createElement("a");
    downloadLink.href = downloadUrl;
    downloadLink.download = "damned.txt";
    document.body.appendChild(downloadLink);
    downloadLink.click();
    downloadLink.remove();
    window.URL.revokeObjectURL(downloadUrl);

    window.location.href = gateButton.href;
  });
}
