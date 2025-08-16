'use server';

import { registerWord, RegisterWordError, RegisterWordResponse } from "@/lib/api";
import { cookies } from "next/headers";

/**
 * 英単語を登録する
 */
export const handleRegisterWord = async (
  word: string,
  meaning: string,
  example: string,
  exampleTranslation: string
): Promise<{
  success: boolean;
  error?: RegisterWordError;
  data?: RegisterWordResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get('access_token');

  if (!tokenCookie) {
    return { success: false };
  }

  const res = await registerWord({
    body: {
      item: {
        word,
        meaning,
        exampleSentence: example,
        exampleSentenceTranslation: exampleTranslation,
      },
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

