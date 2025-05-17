import {CrudConsumer, CrudConsumerObject} from 'consumerjs';

import {get, post} from '@/data/api-client';

import {API_ROOT} from '../../constants';
// TODO: refactor out
import Paginator from '../../scripts/paginator';

interface ListQueryParameters {
  /**
   * ID of the album to retrieve photos for.
   */
  album: number;
  /**
   * Page number, 1-indexed.
   */
  page?: number;
}

interface OwnPhotoData {
  id: number;
  user: number;
  description: string;
  image: {
    large: string;
    thumb: string;
  };
}

interface ListResponseData<T> {
  count: number;
  paginate_by: number;
  previous: string | null;
  next: string | null;
  results: T[];
}

export const listOwnPhotos = async (
  query: ListQueryParameters,
): Promise<ListResponseData<OwnPhotoData>> => {
  const params = Object.entries(query).map((entry: [string, string | number]): [string, string] => {
    const [key, value] = entry;
    return [key, value.toString()];
  });
  const paginatedResponseData = await get<ListResponseData<OwnPhotoData>>('my/photos/', params);
  return paginatedResponseData!;
};

export const getOwnPhoto = async (id: number): Promise<OwnPhotoData> => {
  const photoData = await get<OwnPhotoData>(`my/photos/${id}/`);
  return photoData!;
};

export const setAsCover = async (id: number): Promise<void> => {
  await post(`my/photos/${id}/set_cover/`);
};

interface PhotoData {
  id: number;
  user: {username: string};
  description: string;
  image: {
    large: string;
    thumb: string;
  };
  width: number;
  height: number;
  uploaded: string; // ISO-8601
  order: number;
}

export const listAlbumPhotos = async (query: ListQueryParameters): Promise<PhotoData[]> => {
  const params = Object.entries(query).map((entry: [string, string | number]): [string, string] => {
    const [key, value] = entry;
    return [key, value.toString()];
  });
  const paginatedResponseData = await get<ListResponseData<PhotoData>>('albums/photo/', params);
  return paginatedResponseData!.results;
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
