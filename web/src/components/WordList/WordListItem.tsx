'use client';

import { WordInfo } from '@/types/word';
import { BiSolidTrash } from "react-icons/bi";
import { handleDeleteWord } from './action';
import { useToast } from '@/context/ToastContext';

type Props = {
  key: string;
  wordInfo: WordInfo;
};

export const WordListItem = (props: Props) => {
  const { key, wordInfo}  = props;
  const { showToast } = useToast();

  const handleDeleteClick = async () => {
    const res = await handleDeleteWord(wordInfo.id);
    
    if (res.success) {
      showToast('削除に成功しました', 'success');
    } else {
      showToast('削除に失敗しました', 'error');
    }
  };

  return (
    <li key={key} className="list-row flex flex-row items-center gap-4">
      <div className='flex-1 flex flex-col gap-1'>
        <div className="flex gap-4">
          <div className="text-lg">{wordInfo.word}</div>
          <div className="text-lg">{wordInfo.meaning}</div>
        </div>
        <hr className="text-neutral-content border-dashed" />
        <div className="flex flex-col gap-1.5 text-xs mt-1">
          <div>{wordInfo.exampleSentence}</div>
          <div>{wordInfo.exampleSentenceTranslation}</div>
        </div>
      </div>
      <div className="btn btn-ghost text-error" onClick={handleDeleteClick}>
        <BiSolidTrash className='w-6 h-6'/>
      </div>
    </li>
  );
};
