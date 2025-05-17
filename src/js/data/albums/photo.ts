import {CrudConsumer, CrudConsumerObject} from 'consumerjs';

import {get, post} from '@/data/api-client';

import {API_ROOT} from '../../constants';
// TODO: refactor out
import Paginator from '../../scripts/paginator';

interface ListQueryParameters {
  /**
   * ID of the album to retrieve photos for.
   */
  albumId: number;
  /**
   * Page number, 1-indexed.
   */
  page?: number;
}

interface PhotoData {
  id: number;
  user: number;
  description: string;
  image: {
    large: string;
    thumb: string;
  };
}

interface ListResponseData {
  count: number;
  paginate_by: number;
  previous: string | null;
  next: string | null;
  results: PhotoData[];
}

export const listOwnPhotos = async (query: ListQueryParameters): Promise<ListResponseData> => {
  const params = Object.entries(query).map((entry: [string, string | number]): [string, string] => {
    const [key, value] = entry;
    return [key, value.toString()];
  });
  const paginatedResponseData = await get<ListResponseData>('my/photos/', params);
  return paginatedResponseData!;
};

export const getOwnPhoto = async (id: number): Promise<PhotoData> => {
  const photoData = await get<PhotoData>(`my/photos/${id}/`);
  return photoData!;
};

export const setAsCover = async (id: number): Promise<void> => {
  await post(`my/photos/${id}/set_cover/`);
};

class Photo extends CrudConsumerObject {
  rotate(direction) {
    return this.__consumer__.rotate(this.id, direction);
  }
}

class PhotoConsumer extends CrudConsumer {
  constructor(endpoint = `${API_ROOT}api/v1/albums/photo`, objectClass = Photo) {
    super(endpoint, objectClass);

    // this.parserDataPath = 'results';
  }

  async getForAlbum(albumId, page) {
    const response = await this.get('/', {album: albumId, page: page});
    return response.results;
  }

  async getAllForAlbum(albumId) {
    const paginatedResponse = await this.get('/', {
      album: albumId,
      page: 1,
    });
    // initialize on the first result set
    const paginator = new Paginator();
    paginator.paginate(paginatedResponse);
    const extraPagePromises = paginator.page_range
      .slice(1)
      .map(pageNr => this.get('/', {album: albumId, page: pageNr}));
    const allResponses = await Promise.all([paginatedResponse, ...extraPagePromises]);
    const allResults = allResponses.map(response => response.results);
    return allResults.flat();
  }

  rotate(id, direction) {
    const endpoint = `/${id}/rotate/`;
    return this.patch(endpoint, {direction: direction});
  }
}

export {Photo, PhotoConsumer};
