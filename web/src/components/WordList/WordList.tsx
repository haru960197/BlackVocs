'use server';

import { getUserWordList } from '@/lib/api';
import { WordListItem } from './WordListItem';

export const WordList = async () => {
  const res = await getUserWordList();
  const wordInfoList = res.data ? res.data.wordlist : [];

  return (
    <ul className="list bg-base-100 rounded-box shadow-md w-full mx-4">
      <li className="p-4 pb-2 text-xs opacity-60 tracking-wide">英単語一覧</li>
      {wordInfoList.map((wordInfo) => (
        <WordListItem key={wordInfo.id} wordInfo={wordInfo} />
      ))}
    </ul>
  );
};
