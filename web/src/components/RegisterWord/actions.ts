'use server';

import { addNewWord, AddNewWordError, AddNewWordResponse } from "@/lib/api";
import { cookies } from "next/headers";

/**
 * 英単語を登録する
 * @param word 登録したい英単語
 */
export const registerNewWord = async (word: string): Promise<{
  success: boolean;
  error?: AddNewWordError;
  data?: AddNewWordResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get('access_token');

  if (!tokenCookie) {
    return { success: false };
  }

  const res = await addNewWord({
    body: {
      word,
    },
    headers: {
      Cookie: `${tokenCookie.name}=${tokenCookie.value}`,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true, data: res.data };
};

