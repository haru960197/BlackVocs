"use server";

import { getUserWordList } from "@/lib/api";
import { WordListItem } from "./WordListItem";
import { cookies } from "next/headers";
import { WordOutline } from "@/types/word";

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

  return (
    <div className="flex mx-4 gap-4 w-full">
      {wordInfoList.map((wordOutline) => (
        <WordListItem key={wordOutline.id} wordOutline={wordOutline} />
      ))}
    </div>
  );
};
