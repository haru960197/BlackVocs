'use server';

import { addNewWord, AddNewWordError, AddNewWordResponse } from "@/lib/api";

/**
 * 英単語を登録する
 * @param word 登録したい英単語
 */
export const registerNewWord = async (word: string): Promise<{
  success: boolean;
  error?: AddNewWordError;
  data?: AddNewWordResponse;
}> => {
  const res = await addNewWord({
    body: {
      word,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true, data: res.data };
};

