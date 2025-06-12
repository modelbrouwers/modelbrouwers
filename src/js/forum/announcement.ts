import {get} from '@/data/api-client';

interface AnnouncementData {
  html: string | null;
}

export const fetchAndDisplayAnnouncements = async () => {
  const {html} = (await get<AnnouncementData>('forum_tools/announcement/'))!;
  if (!html) return;
  const node = document.getElementById('announcement');
  if (!node) return;
  node.innerHTML = html;
};

document.addEventListener('DOMContentLoaded', () => {
  fetchAndDisplayAnnouncements();
});
