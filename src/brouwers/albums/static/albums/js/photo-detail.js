'use strict';

import $ from 'bootstrap';
import { Photo } from 'albums/js/models/photo';


class Control {
    constructor($node, $target) {
        this.node = $node;
        this.target = $target;
        this.action = $node.data('action');
        this.mutualExclusiveActions = $.map($node.siblings(), function(el) {
            return $(el).data('action');
        });
    }

    activate() {
        this.node.siblings().removeClass('active');
        this.target
            .removeClass(this.mutualExclusiveActions.join(' '))
            .addClass(this.action);
        this.node.addClass('active');
    }

    deactivate() {
        this.node.removeClass('active');
        this.target.removeClass(this.action);
    }

    toggle() {
        if (this.node.hasClass('active')) {
            this.deactivate();
        } else {
            this.activate();
        }
    }
}


class RotateControl extends Control {
    constructor(...args) {
        super(...args);

        let direction_mapping = {
            'rotate-left': 'ccw',
            'rotate-right': 'cw'
        };
        this.direction = direction_mapping[this.action];
    }

    activate() {
        this.node.addClass('active');

        let id = this.target.data('id');

        Photo.objects.get({id: id}).then(photo => {
            return photo.rotate(this.direction);
        }).done(photo => {
            let img = new Image();
            img.src = photo.image.large;
            this.target.find('img').attr('src', img.src);
            this.deactivate();  // removes the highlighting
        });
    }

    deactivate() {
        this.node.removeClass('active');
    };
}

let getControlClass = function(action) {
    let cls;
    switch(action) {
        case 'rotate-left':
        case 'rotate-right':
            cls = RotateControl;
            break;
        default:
            cls = Control;
    }
    return cls;
}



$(function() {
    var controls = {};

    $('.controls').on('click', '[data-action]', function(event) {
        event.preventDefault();

        var control,
            action = $(this).data('action'),
            $figure = $(this).closest('figure');

        let cls = getControlClass(action);
        control = controls[action] || new cls($(this), $figure);
        control.toggle();
        return false;
    });
});
