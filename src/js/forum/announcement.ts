import {API_ROOT} from '@/constants.js';

interface AnnouncementData {
  html: string | null;
}

export const fetchAndDisplayAnnouncements = async () => {
  // TODO: move endpoint into /api/v1 and then we can use the api-client `get` function.
  const response = await window.fetch(`${API_ROOT}utils/get-announcement/`, {
    credentials: 'include',
  });
  const {html}: AnnouncementData = await response.json();
  if (!html) return;
  const node = document.getElementById('announcement');
  if (!node) return;
  node.innerHTML = html;
};

document.addEventListener('DOMContentLoaded', () => {
  fetchAndDisplayAnnouncements();
});
