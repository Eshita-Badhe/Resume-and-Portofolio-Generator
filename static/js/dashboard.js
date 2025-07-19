document.addEventListener("DOMContentLoaded", () => {
    console.log("Dashboard loaded");

    const buttons = document.querySelectorAll('.dashboard-button');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', () => {
            btn.classList.add('hovered');
        });
        btn.addEventListener('mouseleave', () => {
            btn.classList.remove('hovered');
        });
    });
});
