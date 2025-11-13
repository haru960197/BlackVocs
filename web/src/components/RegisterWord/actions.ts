"use server";

import {
  generateNewWordEntry,
  GenerateNewWordEntryError,
  GenerateNewWordEntryResponse,
  registerWord,
  RegisterWordError,
  suggestWords,
  SuggestWordsError,
  SuggestWordsResponse,
} from "@/lib/api";
import { cookies } from "next/headers";

/**
 * 英単語を登録する
 */
export const handleRegisterWord = async (
  spelling: string,
  meaning?: string,
  example?: string,
  exampleTranslation?: string
): Promise<{
  success: boolean;
  error?: RegisterWordError;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get("access_token");

  if (!tokenCookie) {
    return { success: false };
  }

  const res = await registerWord({
    body: {
      spelling,
      meaning,
      example_sentence: example,
      example_sentence_translation: exampleTranslation,
    },
    headers: {
      Cookie: `${tokenCookie.name}=${tokenCookie.value}`,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true };
};

/**
 * 生成AIを使って新しい単語情報を生成する
 */
export const handleGenerateWordData = async (
  spelling: string,
  meaning?: string,
  exampleSentence?: string,
  exampleSentenceTranslation?: string
): Promise<{
  success: boolean;
  error?: GenerateNewWordEntryError;
  data?: GenerateNewWordEntryResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get("access_token");

  if (!tokenCookie) {
    return { success: false };
  }

  const res = await generateNewWordEntry({
    body: {
      spelling,
      meaning,
      example_sentence: exampleSentence,
      example_sentence_translation: exampleSentenceTranslation,
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
  spellingInput: string
): Promise<{
  success: boolean;
  error?: SuggestWordsError;
  data?: SuggestWordsResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get("access_token");

  if (!tokenCookie) {
    return { success: false };
  }

  const res = await suggestWords({
    body: {
      input_str: spellingInput,
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
