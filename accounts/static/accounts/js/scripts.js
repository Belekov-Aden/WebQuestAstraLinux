document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".transition");

    links.forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            document.body.classList.add("fade-out");
            setTimeout(() => {
                window.location.href = this.href;
            }, 800);
        });
    });
});
