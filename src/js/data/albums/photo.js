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

    async getForAlbum(albumId, page) {
        const response = await this.get("/", { album: albumId, page: page });
        return response.results;
    }

    async getAllForAlbum(albumId) {
        const paginatedResponse = await this.get("/", {
            album: albumId,
            page: 1,
        });
        // initialize on the first result set
        const paginator = new Paginator();
        paginator.paginate(paginatedResponse);
        const extraPagePromises = paginator.page_range
            .slice(1)
            .map((pageNr) => this.get("/", { album: albumId, page: pageNr }));
        const allResponses = await Promise.all([
            paginatedResponse,
            ...extraPagePromises,
        ]);
        const allResults = allResponses.map((response) => response.results);
        return allResults.flat();
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
