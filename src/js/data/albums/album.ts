import {get} from '@/data/api-client';
import {TopicData} from '@/data/topic';

interface AlbumData {
  id: number;
  user: {username: string};
  title: string;
  public: boolean;
  topic: TopicData | null;
}

export const listOwnAlbums = async (): Promise<AlbumData[]> => {
  const albums = await get<AlbumData[]>('my/albums/');
  return albums!;
};
