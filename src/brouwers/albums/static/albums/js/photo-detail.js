'use strict';

import $ from 'bootstrap';


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



$(function() {
    var controls = {};

    $('.controls [data-toggle="popover"]').popover();

    $('.controls').on('click', '[data-action]', function(event) {
        event.preventDefault();

        var control,
            action = $(this).data('action'),
            $figure = $(this).closest('figure');

        control = controls[action] || new Control($(this), $figure);
        control.toggle();
        return false;
    });
});
