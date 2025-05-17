import {get} from '@/data/api-client';

interface ParticipantData {
  id: number;
  model_name: string;
  username: string;
  topic: {
    title: string;
    url: string;
  };
  finished: boolean;
}

interface GroupBuildData {
  id: number;
  theme: string;
  url: string;
  description: string;
  start: string | null; // ISO-8601 date
  end: string | null; // ISO-8601 date
  status: string;
  rules: string;
  rules_topic: {
    title: string;
    url: string;
  };
  participants: ParticipantData[];
}

export const getGroupBuild = async (id: number): Promise<GroupBuildData> => {
  const cart = await get<GroupBuildData>(`groupbuilds/groupbuild/${id}/`);
  return cart!;
};
