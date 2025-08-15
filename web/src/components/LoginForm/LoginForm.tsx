'use client';

import { useToast } from '@/context/ToastContext';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm, SubmitHandler } from 'react-hook-form';
import { LoginFormInput, loginSchema } from './schema';

export const LoginForm = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { showToast } = useToast();
  const { login } = useAuth();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormInput>({
    resolver: zodResolver(loginSchema),
    mode: 'onChange',
  });

  const isDisabled = !!errors.userName || !!errors.password;

  const onSubmit: SubmitHandler<LoginFormInput> = async (data) => {
    if (isDisabled) {
      return;
    }

    const result = await login(data.userName, data.password);

    if (result) {
      showToast('ログインに成功しました', 'success');

      const redirectUrl = searchParams.get('next') ?? '/register-word';
      router.push(redirectUrl);
    } else {
      // ログインに失敗
      showToast('ログインに失敗しました', 'error');
    }
  };

  return (
    <div className="flex flex-col border-1 bg-base-200 border-base-300 rounded-lg p-4 gap-2">
      <form onSubmit={handleSubmit(onSubmit)}>
        <fieldset className="fieldset">
          <label className="label text-lg">User name</label>
          <input
            type="text"
            className="input text-xl"
            placeholder="User name"
            autoComplete="username"
            {...register('userName')}
          />
          {errors.userName && <p className="text-error text-sm mt-1">{errors.userName.message}</p>}

          <label className="label text-lg">Password</label>
          <input
            type="password"
            className="input text-xl"
            placeholder="Password"
            autoComplete="current-password"
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
            {isSubmitting ? <span className="loading loading-spinner" /> : 'ログイン'}
          </button>
        </div>
      </form>

      <p>
        アカウントをお持ちでない方：
        <Link href={'/signup'} className="link link-primary">
          登録
        </Link>
      </p>
    </div>
  );
};
