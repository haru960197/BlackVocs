'use client';

import { useToast } from '@/context/ToastContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { clsx } from 'clsx';
import { useEffect, useState } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { getSuggestWords, handleGenerateWordData, handleRegisterWord } from './actions';
import { WordFormInput, wordFormSchema } from './schema';
import { WordInfo } from '@/types/word';

export const RegisterWordForm = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const { showToast } = useToast();

  const [suggestions, setSuggestions] = useState<WordInfo[]>([]);
  const [isLoadingSuggestions, setIsLoadingSuggestions] = useState(false);
  const [isWordInputFocused, setIsWordInputFocused] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    getValues,
    setValue,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<WordFormInput>({
    resolver: zodResolver(wordFormSchema),
    mode: 'onChange',
  });

  const isDisabled =
    !getValues('word') ||
    !!errors.word ||
    !!errors.meaning ||
    !!errors.example ||
    !!errors.exampleTranslation;
  const isGeneratingDisabled = !getValues('word') || !!errors.word;

  // 'word'フィールドの値を監視
  const watchedWord = watch("word");

  const { onBlur: rhfOnBlur, ...wordRegisterRest } = register('word', { required: true });

  const handleWordInputBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    // まず、react-hook-formのonBlurを実行してバリデーションをトリガー
    rhfOnBlur(e);
    
    // 次に、候補リストを非表示にするためのロジックを実行
    setTimeout(() => {
      setIsWordInputFocused(false);
    }, 150);
  };

  useEffect(() => {
    // 入力が開始されたらローディング状態にする
    if (watchedWord !== "") {
      setIsLoadingSuggestions(true);
    }

    const timerId = setTimeout(() => {
      if (watchedWord !== undefined && watchedWord.trim() === "") {
        setSuggestions([]);
        // 入力が空になったらローディングは停止
        setIsLoadingSuggestions(false);
        return;
      }

      const fetchSuggestions = async () => {

        const response = await getSuggestWords(watchedWord);

        if (!response.success || !response.data) {
          setSuggestions([]);
          setIsLoadingSuggestions(false);
          return;
        }

        setSuggestions(response.data.items.map((item) => ({
          id: item.word,
          ...item
        })));
        setIsLoadingSuggestions(false);
      }

      fetchSuggestions();
    }, 1000);

    return () => {
      clearTimeout(timerId);
    }
  }, [watchedWord]);

  const handleSuggestionClick = (suggestion: WordInfo) => {
    setValue('word', suggestion.word, { shouldValidate: true });
    setValue('meaning', suggestion.meaning, { shouldValidate: true });
    setValue('example', suggestion.exampleSentence ?? "", { shouldValidate: true });
    setValue('exampleTranslation', suggestion.exampleSentenceTranslation ?? "", { shouldValidate: true });

    setSuggestions([]);
  };


  const handleGenerateClick = async () => {
    if (isGeneratingDisabled) {
      return;
    }

    setIsGenerating(true);

    const word = getValues('word');

    const res = await handleGenerateWordData(word);

    if (res.success) {
      const data = res.data;
      if (data?.item) {
        // フォームに生成されたデータをセットする
        setValue('word', data.item.word);
        setValue('meaning', data.item.meaning);
        setValue('example', data.item.exampleSentence);
        setValue('exampleTranslation', data.item.exampleSentenceTranslation);

        showToast('単語情報を生成しました', 'success');
      } else {
        showToast('単語情報の生成に失敗しました', 'error');
      }
    } else {
      showToast('単語情報の生成に失敗しました', 'error');
    }

    setIsGenerating(false);
  };

  const onSubmit: SubmitHandler<WordFormInput> = async (data) => {
    if (isDisabled) {
      return;
    }

    const res = await handleRegisterWord(
      data.word,
      data.meaning,
      data.example,
      data.exampleTranslation
    );

    if (res.success) {
      showToast('登録に成功しました', 'success');
    } else {
      showToast('登録に失敗しました', 'error');
    }
  };

  return (
    <form
      className="flex flex-col border-1 bg-base-200 border-base-300 rounded-lg w-full max-w-[450px] mx-4 p-4 gap-2"
      onSubmit={handleSubmit(onSubmit)}
    >
      <fieldset className="fieldset">
        <legend className="fieldset-legend text-xl">英単語</legend>
        <input
          type="text"
          className={clsx('input text-xl', errors.word && 'input-error')}
          onFocus={() => setIsWordInputFocused(true)}
          placeholder="Pen"
          onBlur={handleWordInputBlur}
          {...wordRegisterRest}
        />
        {errors.word && <p className="text-error text-sm mt-1">{errors.word.message}</p>}

        <div>
        {/* ローディング表示と候補リスト */}
          {isWordInputFocused && (isLoadingSuggestions || suggestions.length > 0) &&
          <ul className="list absolute z-10 mt-1 bg-base-300 border rounded-lg shadow-lg max-h-60 overflow-auto">
            {isLoadingSuggestions &&
              <li className="list-row flex justify-center px-3 py-2 text-lg">
                <span className="loading loading-spinner" /> 
              </li>
            }

            {!isLoadingSuggestions && suggestions.length > 0
              && suggestions.map((suggestion, index) => (
                <li
                  key={index}
                  className="list-row px-3 py-2 text-lg cursor-pointer hover:bg-accent"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  {`${suggestion.word} | ${suggestion.meaning}`}
                </li>
              ))}
            </ul>
            }
        </div>

        <legend className="fieldset-legend text-xl">意味</legend>
        <input
          type="text"
          className={clsx('input text-xl', errors.meaning && 'input-error')}
          placeholder="ペン"
          {...register('meaning', { required: true })}
        />
        {errors.meaning && <p className="text-error text-sm mt-1">{errors.meaning.message}</p>}

        <legend className="fieldset-legend text-xl">例文</legend>
        <textarea
          className={clsx('textarea text-lg w-full', errors.example && 'textarea-error')}
          placeholder="This is a pen."
          {...register('example', { required: true })}
        />
        {errors.example && <p className="text-error text-sm mt-1">{errors.example.message}</p>}

        <legend className="fieldset-legend text-xl">例文（日本語訳）</legend>
        <textarea
          className={clsx('textarea text-lg w-full', errors.exampleTranslation && 'textarea-error')}
          placeholder="これはペンです。"
          {...register('exampleTranslation', { required: true })}
        />
        {errors.exampleTranslation && (
          <p className="text-error text-sm mt-1">{errors.exampleTranslation.message}</p>
        )}
      </fieldset>

      <div className="flex flex-col items-end gap-2">
        <div className="flex justify-end gap-2">
          <button
            type="button"
            className="btn btn-accent btn-sm lg:btn-lg text-lg lg:text-xl"
            onClick={() => reset()}
          >
            リセット
          </button>
          <button
            className="btn btn-secondary btn-sm lg:btn-lg text-lg lg:text-xl"
            disabled={isGeneratingDisabled || isGenerating}
            onClick={handleGenerateClick}
          >
            {isGenerating ? <span className="loading loading-spinner" /> : 'AIで生成'}
          </button>
        </div>
        <div className="flex justify-end">
          <button
            type="submit"
            className="btn btn-primary btn-sm lg:btn-lg text-lg lg:text-xl w-[94px]"
            disabled={isDisabled || isSubmitting}
          >
            {isSubmitting ? <span className="loading loading-spinner" /> : '登録'}
          </button>
        </div>
      </div>
    </form>
  );
};
