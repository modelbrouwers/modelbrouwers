import {get} from '@/data/api-client';

export interface TopicData {
  topic_id: number;
  forum: number;
  topic_title: string;
  last_post_time: number; // UNIX time stamp
  create_time: number; // UNIX time stamp
  author: number;
  is_dead: boolean;
  age: string;
  text_dead: string;
}

export const getTopic = async (id: number): Promise<TopicData> => {
  const cart = await get<TopicData>(`forum_tools/topic/${id}/`);
  return cart!;
};
