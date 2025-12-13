"use client";

import { WordOutline } from "@/types/word";

type Props = {
  wordOutline: WordOutline;
  onClick?: () => void;
};

export const WordListItem = (props: Props) => {
  const { wordOutline, onClick } = props;

  return (
    <div
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
