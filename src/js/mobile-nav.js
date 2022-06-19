const init = () => {
    const navs = document.querySelectorAll(".mobile-nav");

    navs.forEach((navNode) => {
        const triggerNode = navNode.querySelector(
            ".mobile-nav__toggle-trigger"
        );
        if (!triggerNode) return;

        triggerNode.addEventListener("click", () => {
            navNode.classList.toggle("mobile-nav--expanded");
            navNode.classList.toggle("mobile-nav--collapsed");
        });
    });
};

if (document.readyState !== "loading") {
    document.addEventListener("DOMContentLoaded", init);
} else {
    init();
}
