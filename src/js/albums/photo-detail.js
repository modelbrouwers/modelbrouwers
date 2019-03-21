import { PhotoConsumer } from "../data/albums/photo";

export class Control {
    constructor($node, $target) {
        this.node = $node;
        this.target = $target;
        this.action = $node.data("action");
        this.mutualExclusiveActions = $.map($node.siblings(), function(el) {
            return $(el).data("action");
        });
    }

    activate() {
        this.node.siblings().removeClass("active");
        this.target
            .removeClass(this.mutualExclusiveActions.join(" "))
            .addClass(this.action);
        this.node.addClass("active");
    }

    deactivate() {
        this.node.removeClass("active");
        this.target.removeClass(this.action);
    }

    toggle() {
        if (this.node.hasClass("active")) {
            this.deactivate();
        } else {
            this.activate();
        }
    }
}

export class RotateControl extends Control {
    constructor(...args) {
        super(...args);

        let direction_mapping = {
            "rotate-left": "ccw",
            "rotate-right": "cw"
        };
        this.direction = direction_mapping[this.action];

        this.photoConsumer = new PhotoConsumer();
    }

    activate() {
        this.node.addClass("active");
        $(".modal-backdrop").removeClass("hidden");

        let id = this.target.data("id");

        this.photoConsumer
            .read(id)
            .then(photo => {
                return photo.rotate(this.direction);
            })
            .then(photo => {
                let img = new Image();
                img.src = "{0}?cache_bust={1}".format(
                    photo.image.large,
                    new Date().getTime()
                );
                this.target.find("img").attr("src", img.src);
                this.deactivate(); // removes the highlighting
            })
            .catch(console.error);
    }

    deactivate() {
        this.node.removeClass("active");
        $(".modal-backdrop").addClass("hidden");
    }
}
