export default class Page {
    static init() {
        this.initRating();
    }

    static initRating() {
        const nodes = document.querySelectorAll(".rating-input__star");
        const activeClass = "rating-input__option--is-active";

        if (nodes && nodes.length) {
            for (let node of nodes) {
                node.addEventListener("click", function(e) {
                    const id = e.target.dataset.id;
                    const el = document.getElementById(id);
                    const activeNodes = document.querySelectorAll(
                        `.${activeClass}`
                    );

                    for (let activeNode of activeNodes) {
                        activeNode.classList.remove(activeClass);
                    }

                    el.parentNode.classList.add(activeClass);
                    el.checked = true;
                });
            }
        }
    }
}
