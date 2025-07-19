
document.addEventListener('DOMContentLoaded', () => {
  const downloadBtn = document.querySelector('form button[type="submit"]');
  downloadBtn.addEventListener('click', () => {
    downloadBtn.innerText = "Preparing PDF...";
    downloadBtn.disabled = true;
  });
});
