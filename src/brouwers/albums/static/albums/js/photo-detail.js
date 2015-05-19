$(function() {
    'use strict';

    var controls = {};

    var Control = function($node, $target) {
        this.node = $node;
        this.target = $target;
        this.action = $node.data('action');
        this.mutualExclusiveActions = $.map($node.siblings(), function(el) {
            return $(el).data('action');
        });
    };

    Control.prototype.activate = function() {
        this.node.siblings().removeClass('active');
        this.target
            .removeClass(this.mutualExclusiveActions.join(' '))
            .addClass(this.action);
        this.node.addClass('active');
    };

    Control.prototype.deactivate = function() {
        this.node.removeClass('active');
        this.target.removeClass(this.action);
    };

    Control.prototype.toggle = function() {
        if (this.node.hasClass('active')) {
            this.deactivate();
        } else {
            this.activate();
        }
    };


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
