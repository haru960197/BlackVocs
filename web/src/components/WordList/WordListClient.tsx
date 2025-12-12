"use client";

import { useState } from "react";
import { WordOutline } from "@/types/word";
import { WordListItem } from "./WordListItem";
import { WordDetailModal } from "../WordDetailModal/WordDetailModal";

type Props = {
  wordInfoList: WordOutline[];
};

export const WordListClient = ({ wordInfoList }: Props) => {
  const [selectedWordId, setSelectedWordId] = useState<string | null>(null);

  return (
    <div className="flex mx-4 gap-4 w-full flex-wrap">
      {wordInfoList.map((wordOutline) => (
        <WordListItem
          key={wordOutline.id}
          wordOutline={wordOutline}
          onClick={() => setSelectedWordId(wordOutline.id)}
        />
      ))}

      <WordDetailModal
        isOpen={!!selectedWordId}
        wordId={selectedWordId}
        onClose={() => setSelectedWordId(null)}
      />
    </div>
  );
};
