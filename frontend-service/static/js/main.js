const previewButtons = document.querySelectorAll(".preview-btn");
const modal = document.getElementById("previewModal");
const closeBtn = document.getElementById("modalClose");

if (modal && closeBtn) {
    previewButtons.forEach((button) => {
        button.addEventListener("click", () => {
            document.getElementById("modalImage").src = button.dataset.image;
            document.getElementById("modalName").textContent = button.dataset.name;
            document.getElementById("modalPrice").textContent = button.dataset.price;
            document.getElementById("modalColor").textContent = button.dataset.color;
            document.getElementById("modalQuality").textContent = button.dataset.quality;
            document.getElementById("modalDescription").textContent = button.dataset.description;
            modal.classList.add("open");
            modal.setAttribute("aria-hidden", "false");
        });
    });

    closeBtn.addEventListener("click", () => {
        modal.classList.remove("open");
        modal.setAttribute("aria-hidden", "true");
    });

    modal.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.classList.remove("open");
            modal.setAttribute("aria-hidden", "true");
        }
    });
}
