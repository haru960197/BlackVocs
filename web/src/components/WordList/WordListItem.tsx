"use client";

import { WordOutline } from "@/types/word";

type Props = {
  key: string;
  wordOutline: WordOutline;
};

export const WordListItem = (props: Props) => {
  const { key, wordOutline } = props;

  return (
    <div key={key} className="card min-w-48 bg-base-200 card-sm shadow-sm">
      <div className="card-body">
        <div className="card-title text-2xl">{wordOutline.spelling}</div>
        <p className="text-lg">{wordOutline.meaning}</p>
      </div>
    </div>
  );
};
