export default class Slider {

    constructor(selector) {
        this.nodes = document.querySelectorAll(selector);
        for (let node of this.nodes) {
            node.addEventListener('change', this.updateOutput.bind(this));
            node.addEventListener('input', this.updateOutput.bind(this));
        }
    }

    updateOutput(event) {
        let output = event.target.nextElementSibling;
        output.value = event.target.value;
    }
}
