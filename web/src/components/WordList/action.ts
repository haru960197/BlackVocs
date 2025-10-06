'use server';

import { deleteWord, DeleteWordError, DeleteWordResponse } from '@/lib/api';
import { cookies } from 'next/headers';

/**
 * 単語を削除する
 */
export const handleDeleteWord = async (
  wordId: string,
): Promise<{
  success: boolean;
  error?: DeleteWordError;
  data?: DeleteWordResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get('access_token');
  
  if (!tokenCookie) {
    return { success: false };
  }

  const res = await deleteWord({
    body: {
      word_id: wordId,
    },
    headers: {
      Cookie: `${tokenCookie.name}=${tokenCookie.value}`,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true, data: res.data };
}
