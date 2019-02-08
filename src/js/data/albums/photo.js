import { CrudConsumer, CrudConsumerObject } from 'consumerjs';

import { API_ROOT } from '../../constants';


class Photo extends CrudConsumerObject {
    get bbcode() {
        return `[photo data-id="${this.id}"]${this.image.large}[/photo]`;
    }

    rotate(direction) {
        return this.__consumer__.rotate(this.id, direction);
    }
}


class PhotoConsumer extends CrudConsumer {
    constructor(endpoint=`${API_ROOT}api/v1/albums/photo`, objectClass=Photo) {
        super(endpoint, objectClass);
    }

    getForAlbum(albumId, page) {
        return this
            .get('/', {album: albumId, page: page})
            .then(paginatedResponse => {
                return paginatedResponse.results;
            });
    }

    rotate(id, direction) {
        const endpoint = `/${id}/rotate/`;
        return this.patch(endpoint, { direction: direction });
    }
}


class MyPhoto extends Photo {
    setAsCover() {
        this.__consumer__.setAsCover(this.id);
    }
}


class MyPhotoConsumer extends CrudConsumer {
    constructor(endpoint=`${API_ROOT}api/v1/my/photos`, objectClass=Photo) {
        super(endpoint, objectClass);
    }

    setAsCover(id) {
        return this.post(`/${id}/set_cover/`);
    }

    getForAlbum(albumId, extraFilters={}) {
        let filters = Object.assign({ album: albumId }, extraFilters);
        return this.get('/', filters);
    }
}


export { PhotoConsumer, MyPhotoConsumer };