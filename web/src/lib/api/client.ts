'use server';

import { paths } from '@/types/api-types';
import { WordInfo } from '@/types/word';

export async function getAllWordInfo(): Promise<WordInfo[]> {
  const response = await fetch(`${process.env.SERVICE_URI}/items/all`, {
    method: 'GET',
  });
  if (!response.ok) {
    throw new Error('Failed to fetch wordInfo list.');
  }
  const wordInfoList: paths['/items/all']['get']['responses']['200']['content']['application/json'] =
    await response.json();

  return wordInfoList.items;
}
