'use server';

import {
  generateNewWordEntry,
  GenerateNewWordEntryError,
  GenerateNewWordEntryResponse,
  registerWord,
  RegisterWordError,
  RegisterWordResponse,
  suggestWords,
  SuggestWordsError,
  SuggestWordsResponse,
} from '@/lib/api';
import { cookies } from 'next/headers';

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

/**
 * 生成AIを使って新しい単語情報を生成する
 */
export const handleGenerateWordData = async (
  word: string
): Promise<{
  success: boolean;
  error?: GenerateNewWordEntryError;
  data?: GenerateNewWordEntryResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get('access_token');

  if (!tokenCookie) {
    return { success: false };
  }

  const res = await generateNewWordEntry({
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

export const getSuggestWords = async (
  wordInput: string
): Promise<{
  success: boolean;
  error?: SuggestWordsError;
  data?: SuggestWordsResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get('access_token');

  if (!tokenCookie) {
    return { success: false };
  }

  const res = await suggestWords({
    body: {
      input_word: wordInput,
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
