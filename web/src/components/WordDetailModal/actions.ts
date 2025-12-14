"use server";

import {
  deleteWord,
  DeleteWordError,
  DeleteWordResponse,
  getWordContent,
  GetWordContentError,
} from "@/lib/api";
import { cookies } from "next/headers";
import { revalidatePath } from "next/cache";
import { WordInfo } from "@/types/word";

/**
 * 単語の詳細データを取得する
 */
export const handleGetWordInfo = async (
  wordId: string
): Promise<{
  success: boolean;
  error?: GetWordContentError;
  data?: WordInfo;
}> => {
  const res = await getWordContent({
    body: {
      user_word_id: wordId,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return {
    success: true,
    data: {
      id: res.data.user_word_id,
      spelling: res.data.spelling,
      meaning: res.data.meaning ?? undefined,
      exampleSentence: res.data.example_sentence ?? undefined,
      exampleSentenceTranslation: res.data.example_sentence_translation ?? undefined,
    },
  };
};

/**
 * 単語を削除する
 */
export const handleDeleteWord = async (
  wordId: string
): Promise<{
  success: boolean;
  error?: DeleteWordError;
  data?: DeleteWordResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get("access_token");

  if (!tokenCookie) {
    return { success: false };
  }

  const res = await deleteWord({
    body: {
      user_word_id: wordId,
    },
    headers: {
      Cookie: `${tokenCookie.name}=${tokenCookie.value}`,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  revalidatePath("/word-list");

  return { success: true, data: res.data };
};
