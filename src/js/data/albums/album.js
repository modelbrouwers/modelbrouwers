import {CrudConsumer, CrudConsumerObject} from 'consumerjs';

import {API_ROOT} from '../../constants';
import {MyPhotoConsumer} from './photo';

const myPhotoConsumer = new MyPhotoConsumer();

class Album extends CrudConsumerObject {
  getPhotos(extraFilters = {}) {
    return myPhotoConsumer.getForAlbum(this.id, extraFilters);
  }
}

class AlbumConsumer extends CrudConsumer {
  constructor(endpoint = `${API_ROOT}api/v1/my/albums`, objectClass = Album) {
    super(endpoint, objectClass);
  }

  list() {
    return this.get('/');
  }
}

export {Album, AlbumConsumer};
