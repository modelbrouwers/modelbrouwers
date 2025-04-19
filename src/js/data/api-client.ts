import {API_ROOT} from '@/constants.js';

let CSRF_TOKEN: string = '';

export const setCsrfTokenValue = (value: string): void => {
  CSRF_TOKEN = value;
};

const FETCH_DEFAULTS: RequestInit = {
  method: 'GET',
  credentials: 'include',
};

const throwForStatus = async (response: Response): Promise<void> => {
  if (response.ok) return;
  throw {message: `Got error response code ${response.status}`, response};
};

const request = async (url: URL, opts: RequestInit = {}): Promise<Response> => {
  const options: RequestInit = {...FETCH_DEFAULTS, ...opts};

  const response = await window.fetch(url, options);
  await throwForStatus(response);

  return response;
};

type QueryParams = string[][] | Record<string, string> | string | URLSearchParams;

const normalizeUrl = (relativeUrl: string, params?: QueryParams): URL => {
  const normalizedUrl = new URL(`${API_ROOT}api/v1/${relativeUrl}`, window.location.origin);
  if (params) {
    const searchParams = new URLSearchParams(params);
    normalizedUrl.search = searchParams.toString();
  }
  return normalizedUrl;
};

/**
 * Make a GET api call to `url`, with optional query string parameters.
 *
 * The return data is the JSON response body, or `null` if there is no content. Specify
 * the generic type parameter `T` to get typed return data.
 */
export const get = async <T = unknown>(
  relativeUrl: string,
  params: QueryParams = {},
): Promise<T | null> => {
  const normalizedUrl = normalizeUrl(relativeUrl, params);
  const response = await request(normalizedUrl);
  const data: T | null = response.status === 204 ? null : await response.json();
  return data;
};

export const patch = async <T = unknown, U = unknown>(
  relativeUrl: string,
  data: U,
): Promise<T | null> => {
  const normalizedUrl = normalizeUrl(relativeUrl);
  const options: RequestInit = {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': CSRF_TOKEN,
    },
    body: JSON.stringify(data),
  };
  const response = await request(normalizedUrl, options);
  const responseData: T | null = response.status === 204 ? null : await response.json();
  return responseData;
};

export const destroy = async (relativeUrl: string): Promise<null> => {
  const normalizedUrl = normalizeUrl(relativeUrl);
  const options: RequestInit = {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': CSRF_TOKEN,
    },
  };
  await request(normalizedUrl, options);
  return null;
};
