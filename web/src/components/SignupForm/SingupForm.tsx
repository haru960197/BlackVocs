'use client';

import Link from 'next/link';
import { handleSignupUser } from './action';
import { useRouter } from 'next/navigation';
import { useToast } from '@/context/ToastContext';
import { useForm, SubmitHandler } from 'react-hook-form';
import { SignupFormInput, signupSchema } from './schema';
import { zodResolver } from '@hookform/resolvers/zod';
import clsx from 'clsx';

export const SignupForm = () => {
  const router = useRouter();

  const { showToast } = useToast();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<SignupFormInput>({
    resolver: zodResolver(signupSchema),
    mode: 'onChange',
  });

  const isDisabled = !!errors.email || !!errors.userName || !!errors.password;

  const onSubmit: SubmitHandler<SignupFormInput> = async (data) => {
    if (isDisabled) {
      return;
    }

    const response = await handleSignupUser(data.userName, data.email, data.password);

    if (response.success) {
      // 登録に成功したので，ログインページにリダイレクトする
      showToast('登録に成功しました', 'success');
      router.push('/login');
    } else {
      if (typeof response.error?.detail === 'string') {
        showToast(response.error?.detail, 'error');
      } else {
        showToast('予期せぬエラーが発生しました', 'error');
      }
    }
  };

  return (
    <div className="flex flex-col border-1 bg-base-200 border-base-300 rounded-lg p-4 gap-2">
      <form onSubmit={handleSubmit(onSubmit)}>
        <fieldset className="fieldset">
          <label className="label text-lg">Email</label>
          <input
            type="email"
            className={clsx('input text-xl', errors.email && 'input-error')}
            placeholder="Email"
            autoComplete="email"
            {...register('email')}
          />
          {errors.email && <p className="text-error text-sm mt-1">{errors.email.message}</p>}

          <label className="label text-lg">User name</label>
          <input
            type="text"
            className={clsx('input text-xl', errors.userName && 'input-error')}
            placeholder="User name"
            autoComplete="username"
            {...register('userName')}
          />
          {errors.userName && <p className="text-error text-sm mt-1">{errors.userName.message}</p>}

          <label className="label text-lg">Password</label>
          <input
            type="password"
            className={clsx('input text-xl', errors.password && 'input-error')}
            placeholder="Password"
            autoComplete="new-password"
            {...register('password')}
          />
          {errors.password && <p className="text-error text-sm mt-1">{errors.password.message}</p>}
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

      <p>
        アカウントをお持ちの方：
        <Link href={'/login'} className="link link-primary">
          ログイン
        </Link>
      </p>
    </div>
  );
};
