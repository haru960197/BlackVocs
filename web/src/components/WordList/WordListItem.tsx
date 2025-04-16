import { WordInfo } from '@/types/word';

type Props = {
  key: string;
  wordInfo: WordInfo;
};

export const WordListItem = (props: Props) => {
  const { key, wordInfo } = props;
  return (
    <li key={key} className="list-row flex flex-col gap-1">
      <div className="flex gap-4">
        <div className="text-lg">{wordInfo.word}</div>
        <div className="text-lg">{wordInfo.meaning}</div>
      </div>
      <hr className="text-neutral-content border-dashed" />
      <div className="flex flex-col gap-1.5 text-xs mt-1">
        <div>{wordInfo.exampleSentence}</div>
        <div>{wordInfo.exampleSentenceTranslation}</div>
      </div>
    </li>
  );
};
