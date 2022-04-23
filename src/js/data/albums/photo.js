import { CrudConsumer, CrudConsumerObject } from "consumerjs";

import { API_ROOT } from "../../constants";

// TODO: refactor out
import Paginator from "../../scripts/paginator";

class Photo extends CrudConsumerObject {
    get bbcode() {
        return `[photo data-id="${this.id}"]${this.image.large}[/photo]`;
    }

    rotate(direction) {
        return this.__consumer__.rotate(this.id, direction);
    }
}

class PhotoConsumer extends CrudConsumer {
    constructor(
        endpoint = `${API_ROOT}api/v1/albums/photo`,
        objectClass = Photo
    ) {
        super(endpoint, objectClass);

        // this.parserDataPath = 'results';
    }

    getForAlbum(albumId, page) {
        return this.get("/", { album: albumId, page: page }).then(
            (paginatedResponse) => paginatedResponse.results
        );
    }

    getAllForAlbum(albumId) {
        const promise = this.get("/", { album: albumId, page: 1 });
        return promise
            .then((paginatedResponse) => {
                // initialize on the first result set
                const paginator = new Paginator();
                paginator.paginate(paginatedResponse);
                const page_range = paginator.page_range;

                let allPromises = [Promise.resolve(paginatedResponse)].concat(
                    // strip off first page, we already just fetched that
                    page_range
                        .slice(1)
                        // fetch all other pages
                        .map((pageNr) => this.getForAlbum(albumId, pageNr))
                );
                return Promise.all(allPromises);
            })
            .then((responses) => {
                const photos = responses.map((response) => response.results);
                // lists of photos for each page, so merge them together
                return photos.flat();
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
    constructor(endpoint = `${API_ROOT}api/v1/my/photos`, objectClass = Photo) {
        super(endpoint, objectClass);
    }

    setAsCover(id) {
        return this.post(`/${id}/set_cover/`);
    }

    getForAlbum(albumId, extraFilters = {}) {
        let filters = Object.assign({ album: albumId }, extraFilters);
        return this.get("/", filters);
    }
}

export { Photo, PhotoConsumer, MyPhotoConsumer };
