'use server';

import { getUserWordList } from '@/lib/api';
import { WordListItem } from './WordListItem';
import { cookies } from 'next/headers';

export const WordList = async () => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get('access_token');

  const res = await getUserWordList({
    headers: {
      Cookie: `${tokenCookie?.name}=${tokenCookie?.value}`,
    },
  });

  const wordInfoList = res.data ? res.data.items : [];

  return (
    <ul className="list bg-base-100 rounded-box shadow-md w-full mx-4">
      <li className="p-4 pb-2 text-xs opacity-60 tracking-wide">英単語一覧</li>
      {wordInfoList.map((wordInfo) => (
        <WordListItem key={wordInfo.id} wordInfo={wordInfo} />
      ))}
    </ul>
  );
};
