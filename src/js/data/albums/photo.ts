import {CrudConsumer, CrudConsumerObject} from 'consumerjs';

import {get, post} from '@/data/api-client';

import {API_ROOT} from '../../constants';

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

export const listAllAlbumPhotos = async (albumId: number): Promise<PhotoData[]> => {
  const query = {album: albumId.toString()};
  // get first page to determine how many pages to retrieve
  const paginatedResponseData = await get<ListResponseData<PhotoData>>('albums/photo/', {
    ...query,
    page: '1',
  });
  const {count, paginate_by, results} = paginatedResponseData!;
  const numPages = Math.ceil(count / paginate_by);

  // figure out all the other pages to load in parallel
  const pageNumbersToRetrieve = [...Array(numPages - 1).keys()].map(index => index + 2);
  const otherPagePromises = pageNumbersToRetrieve.map(page => {
    const params = {...query, page: page.toString()};
    return get<ListResponseData<PhotoData>>('albums/photo/', params);
  });
  const resolvedPromises = await Promise.all(otherPagePromises);
  return resolvedPromises.reduce((acc, response) => acc.concat(response!.results), results);
};

class Photo extends CrudConsumerObject {
  rotate(direction) {
    return this.__consumer__.rotate(this.id, direction);
  }
}

class PhotoConsumer extends CrudConsumer {
  constructor(endpoint = `${API_ROOT}api/v1/albums/photo`, objectClass = Photo) {
    super(endpoint, objectClass);
  }

  rotate(id, direction) {
    const endpoint = `/${id}/rotate/`;
    return this.patch(endpoint, {direction: direction});
  }
}

export {Photo, PhotoConsumer};
