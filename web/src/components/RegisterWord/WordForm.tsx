'use client';

import { useState } from 'react';
import { registerNewWord } from './actions';

export const WordForm = () => {
  const [input, setInput] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleClick = async () => {
    setIsLoading(true);

    await registerNewWord(input);

    setIsLoading(false);
  };

  return (
    <div className="flex flex-col border-1 bg-base-200 border-base-300 rounded-lg p-4 gap-2">
      <fieldset className="fieldset">
        <legend className="fieldset-legend text-xl">英単語</legend>
        <input
          type="text"
          className="input text-xl"
          placeholder="Apple"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
      </fieldset>
      <div className="flex justify-end">
        <button
          className="btn btn-primary btn-sm lg:btn-lg text-lg lg:text-xl"
          disabled={!input}
          onClick={handleClick}
        >
          {isLoading ? <span className="loading loading-spinner" /> : '登録'}
        </button>
      </div>
    </div>
  );
};
