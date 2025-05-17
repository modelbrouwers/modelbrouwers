import {rotatePhoto} from '@/data/albums/photo';

export class Control {
  constructor($node, $target) {
    this.node = $node;
    this.target = $target;
    this.action = $node.data('action');
    this.mutualExclusiveActions = $.map($node.siblings(), function (el) {
      return $(el).data('action');
    });
  }

  activate() {
    this.node.siblings().removeClass('active');
    this.target.removeClass(this.mutualExclusiveActions.join(' ')).addClass(this.action);
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

export class RotateControl extends Control {
  constructor(...args) {
    super(...args);

    let direction_mapping = {
      'rotate-left': 'ccw',
      'rotate-right': 'cw',
    };
    this.direction = direction_mapping[this.action];
  }

  async activate() {
    this.node.addClass('active');
    $('.modal-backdrop').removeClass('hidden');

    const id = parseInt(this.target.data('id'));

    const photo = await rotatePhoto(id, this.direction);
    const timestamp = new Date().getTime();
    const newImageUrl = `${photo.image.large}?cache_bust=${timestamp}`;

    const img = new Image();
    img.src = newImageUrl;
    this.target.find('img').attr('src', img.src);
    this.deactivate(); // removes the highlighting
  }

  deactivate() {
    this.node.removeClass('active');
    $('.modal-backdrop').addClass('hidden');
  }
}
