"use server";

import { getUserWordList } from "@/lib/api";
import { cookies } from "next/headers";
import { WordOutline } from "@/types/word";
import { WordListClient } from "./WordListClient";

export const WordList = async () => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get("access_token");

  const res = await getUserWordList({
    headers: {
      Cookie: `${tokenCookie?.name}=${tokenCookie?.value}`,
    },
  });

  const wordInfoList: WordOutline[] = res.data
    ? res.data.word_list.map((word) => ({
        id: word.user_word_id,
        spelling: word.spelling,
        meaning: word.meaning ?? undefined,
      }))
    : [];

  return <WordListClient wordInfoList={wordInfoList} />;
};
