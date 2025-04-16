import {API_ROOT} from '@/constants.js';

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

/**
 * Make a GET api call to `url`, with optional query string parameters.
 *
 * The return data is the JSON response body, or `null` if there is no content. Specify
 * the generic type parameter `T` to get typed return data.
 */
export const get = async <T = unknown>(
  relativeUrl: string,
  params: string[][] | Record<string, string> | string | URLSearchParams = {},
): Promise<T | null> => {
  const normalizedUrl = new URL(`${API_ROOT}${relativeUrl}`, window.location.origin);
  const searchParams = new URLSearchParams(params);
  normalizedUrl.search = searchParams.toString();

  const response = await request(normalizedUrl);

  const data: T | null = response.status === 204 ? null : await response.json();
  return data;
};
