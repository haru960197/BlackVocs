"use client";

import { WordOutline } from "@/types/word";

type Props = {
  key: string;
  wordOutline: WordOutline;
  onClick?: () => void;
};

export const WordListItem = (props: Props) => {
  const { key, wordOutline, onClick } = props;

  return (
    <div
      key={key}
      onClick={onClick}
      className="card cursor-pointer w-full md:w-48 bg-base-200 card-sm shadow-sm"
    >
      <div className="card-body">
        <div className="card-title text-2xl">{wordOutline.spelling}</div>
        <p className="text-lg">{wordOutline.meaning}</p>
      </div>
    </div>
  );
};
