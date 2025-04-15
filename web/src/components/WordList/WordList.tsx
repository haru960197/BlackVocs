import { WordInfo } from '@/types/word';
import { WordListItem } from './WordListItem';

export const WordList = () => {
  const exampleWordInfos: WordInfo[] = [
    {
      id: '9jklfdsjkl',
      word: 'cook',
      meaning: '料理する',
      exampleSentence: 'I usually cook because eating at a restaurant costs a lot.',
      exampleSentenceTranslation: '外食はお金がたくさんかかるので，私は普段料理をします',
    },
    {
      id: 'fdsjklwe',
      word: 'traditional',
      meaning: '伝統的な',
      exampleSentence: 'I usually cook because eating at a restaurant costs a lot.',
      exampleSentenceTranslation: '外食はお金がたくさんかかるので，私は普段料理をします',
    },
  ];

  return (
    <ul className="list bg-base-100 rounded-box shadow-md">
      <li className="p-4 pb-2 text-xs opacity-60 tracking-wide">英単語一覧</li>
      {exampleWordInfos.map((wordInfo) => (
        <WordListItem key={wordInfo.id} wordInfo={wordInfo} />
      ))}
    </ul>
  );
};
