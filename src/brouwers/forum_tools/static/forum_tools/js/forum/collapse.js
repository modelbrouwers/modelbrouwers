
/**
 * Initializes toggle behaviour for any element with data-toggle="collapse"
 */
export default class Collapse {
    constructor() {
        let nodes = document.querySelectorAll('[data-toggle="collapse"]');
        for (let i=0; i<nodes.length; i++) {
            nodes[i].addEventListener('click', event => this.toggle(event));
        }
    }

    toggle(event) {
        let trigger = event.currentTarget,
            targets = document.querySelectorAll(trigger.dataset.target);
        let handler = trigger.classList.contains('in') ? this.hide : this.show;
        handler(trigger, targets);
    }

    show(trigger, targets) {
        trigger.classList.add('in');
        for (let i=0; i<targets.length; i++) {
            targets[i].classList.add('in');
        }
    }

    hide(trigger, targets) {
        trigger.classList.remove('in');
        for (let i=0; i<targets.length; i++) {
            targets[i].classList.remove('in');
        }
    }
}
