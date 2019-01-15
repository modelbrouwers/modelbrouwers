import { CrudConsumer, CrudConsumerObject } from 'consumerjs';

import { API_ROOT } from '../../constants';


class Photo extends CrudConsumerObject {
    bbcode() {
        return `[photo data-id="${this.id}"]${this.image.large}[/photo]`;
    }

    rotate(direction) {
        return this.__consumer__.rotate(this.id, direction);
    }
}


class PhotoConsumer extends CrudConsumer {
    constructor(endpoint=`${API_ROOT}albums/photo`, objectClass=Photo) {
        super(endpoint, objectClass);
    }

    getForAlbum(albumId, page) {
        return this.get('/', {album: albumId, page: page});
    }

    rotate(id, direction) {
        const endpoint = `/${id}/rotate/`;
        return this.patch(endpoint, { direction: direction });
    }
}


class MyPhoto extends CrudConsumerObject {
    setAsCover() {
        this.__consumer__.setAsCover(this.id);
    }
}


class MyPhotoConsumer extends CrudConsumer {
    constructor(endpoint=`${API_ROOT}my/photos`, objectClass=Photo) {
        super(endpoint, objectClass);
    }

    setAsCover(id) {
        return this.post(`/${id}/set_cover/`);
    }
}


export { PhotoConsumer, MyPhotoConsumer };
