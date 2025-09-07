import {get, patch, post} from '@/data/api-client';

/**
 * Own photos interactions
 */

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

/**
 * Generic albums/photos interaction
 */

export interface PhotoData {
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

interface RotateBody {
  direction: 'cw' | 'ccw';
}

export const rotatePhoto = async (
  id: number,
  direction: RotateBody['direction'],
): Promise<PhotoData> => {
  const photoData = await patch<PhotoData, RotateBody>(`albums/photo/${id}/rotate/`, {direction});
  return photoData!;
};
