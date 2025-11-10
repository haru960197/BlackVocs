"use server";

import { getUserWordList } from "@/lib/api";
import { WordListItem } from "./WordListItem";
import { cookies } from "next/headers";
import { WordInfo } from "@/types/word";

export const WordList = async () => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get("access_token");

  const res = await getUserWordList({
    headers: {
      Cookie: `${tokenCookie?.name}=${tokenCookie?.value}`,
    },
  });

  const wordInfoList: WordInfo[] = res.data
    ? res.data.word_list.map((word) => ({
        id: word.word_id,
        word: word.word,
        meaning: word.meaning ?? undefined,
        exampleSentence: word.example_sentence ?? undefined,
        exampleSentenceTranslation: word.example_sentence_translation ?? undefined,
      }))
    : [];

  return (
    <ul className="list bg-base-100 rounded-box shadow-md w-full mx-4">
      <li className="p-4 pb-2 text-xs opacity-60 tracking-wide">英単語一覧</li>
      {wordInfoList.map((wordInfo) => (
        <WordListItem key={wordInfo.id} wordInfo={wordInfo} />
      ))}
    </ul>
  );
};
