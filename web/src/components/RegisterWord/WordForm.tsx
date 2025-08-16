'use client';

import { useToast } from '@/context/ToastContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { clsx } from 'clsx';
import { useState } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { handleGenerateWordData, handleRegisterWord } from './actions';
import { WordFormInput, wordFormSchema } from './schema';

export const WordForm = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const { showToast } = useToast();

  const {
    register,
    handleSubmit,
    getValues,
    setValue,
    formState: { errors, isSubmitting },
  } = useForm<WordFormInput>({
    resolver: zodResolver(wordFormSchema),
    mode: 'onChange',
  });

  const isDisabled = !!errors.word || !!errors.meaning || !!errors.example || !!errors.exampleTranslation;
  const isGeneratingDisabled = !!errors.word;

  const handleGenerateClick = async () => {
    if (isGeneratingDisabled) {
      return;
    }

    setIsGenerating(true);

    const word = getValues('word');

    const res = await handleGenerateWordData(word)

    if (res.success) {
      const data = res.data;
      if (data?.item) {
        // フォームに生成されたデータをセットする
        setValue("word", data.item.word);
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
  }

  const onSubmit: SubmitHandler<WordFormInput> = async (data) => {
    if (isDisabled) {
      return;
    }

    const res = await handleRegisterWord(data.word, data.meaning, data.example, data.exampleTranslation);

    if (res.success) {  
      showToast('登録に成功しました', 'success');
    } else {
      showToast('登録に失敗しました', 'error');
    }
  };

  return (
    <form
      className="flex flex-col border-1 bg-base-200 border-base-300 rounded-lg p-4 gap-2"
      onSubmit={handleSubmit(onSubmit)}
    >
      <fieldset className="fieldset">
        <legend className="fieldset-legend text-xl">英単語</legend>
        <input
          type="text"
          className={clsx("input text-xl", errors.word && 'input-error')}
          placeholder="Pen"
          {...register('word', { required: true })}
        />
        {errors.word && <p className="text-error text-sm mt-1">{errors.word.message}</p>}

        <legend className="fieldset-legend text-xl">意味</legend>
        <input
          type="text"
          className={clsx("input text-xl", errors.meaning && 'input-error')}
          placeholder="ペン"
          {...register('meaning', { required: true })}
        />
        {errors.meaning && <p className="text-error text-sm mt-1">{errors.meaning.message}</p>}

        <legend className="fieldset-legend text-xl">例文</legend>
        <input
          type="text"
          className={clsx("input text-xl", errors.example && 'input-error')}
          placeholder="This is a pen."
          {...register('example', { required: true })}
        />
        {errors.example && <p className="text-error text-sm mt-1">{errors.example.message}</p>}

        <legend className="fieldset-legend text-xl">例文（日本語訳）</legend>
        <input
          type="text"
          className={clsx("input text-xl", errors.exampleTranslation && 'input-error')}
          placeholder="これはペンです。"
          {...register('exampleTranslation', { required: true })}
        />
        {errors.exampleTranslation && <p className="text-error text-sm mt-1">{errors.exampleTranslation.message}</p>}
      </fieldset>

      <div className="flex justify-end">
        <button
          className='btn btn-secondary btn-sm lg:btn-lg text-lg lg:text-xl mr-2'
          disabled={isGeneratingDisabled || isGenerating}
          onClick={handleGenerateClick}
        >
          {isGenerating ? <span className="loading loading-spinner" /> : 'AIで生成'}
        </button>
        <button
          type="submit"
          className="btn btn-primary btn-sm lg:btn-lg text-lg lg:text-xl"
          disabled={isDisabled || isSubmitting}
        >
          {isSubmitting ? <span className="loading loading-spinner" /> : '登録'}
        </button>
      </div>
    </form>
  );
};
