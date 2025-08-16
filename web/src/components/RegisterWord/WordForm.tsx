'use client';

import { useToast } from '@/context/ToastContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { clsx } from 'clsx';
import { SubmitHandler, useForm } from 'react-hook-form';
import { handleRegisterWord } from './actions';
import { WordFormInput, wordFormSchema } from './schema';

export const WordForm = () => {
  const { showToast } = useToast();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<WordFormInput>({
    resolver: zodResolver(wordFormSchema),
    mode: 'onChange',
  });

  const isDisabled = !!errors.word || !!errors.meaning || !!errors.example || !!errors.exampleTranslation;

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
