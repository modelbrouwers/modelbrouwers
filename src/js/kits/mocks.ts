import {HttpResponse, http} from 'msw';

import {API_ROOT} from '@/constants';

export const mockGetKitBrands = () =>
  http.get(`${API_ROOT}api/v1/kits/brand/`, () =>
    HttpResponse.json([
      {
        id: 1,
        name: 'Revell',
        is_active: true,
      },
    ]),
  );

export const mockGetKitScales = () =>
  http.get(`${API_ROOT}api/v1/kits/scale/`, () =>
    HttpResponse.json([
      {
        id: 1,
        scale: 48,
        __str__: '1/48',
      },
    ]),
  );
