'use client';

import { useToast } from '@/context/ToastContext';
import Link from 'next/link';
import { useRouter, useSearchParams } from 'next/navigation';
import { useState } from 'react';
import { useAuth } from '@/context/AuthContext';

export const LoginForm = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { showToast } = useToast();
  const { isLoading, login } = useAuth();

  const [userName, setUserName] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const isDisabled = !userName || !password;

  const handleClick = async () => {
    if (isDisabled) {
      return;
    }

    const result = await login(userName, password);

    if (result) {
      // ログインに成功したので，単語一覧ページにリダイレクトする
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
      <fieldset className="fieldset">
        <label className="label text-lg">User name</label>
        <input
          type="text"
          className="input text-xl"
          placeholder="User name"
          value={userName}
          onChange={(e) => setUserName(e.target.value)}
        />

        <label className="label text-lg">Password</label>
        <input
          type="password"
          className="input text-xl"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </fieldset>

      <div className="flex justify-end">
        <button
          className="btn btn-primary btn-sm lg:btn-lg text-lg lg:text-xl"
          disabled={isDisabled}
          onClick={handleClick}
        >
          {isLoading ? <span className="loading loading-spinner" /> : 'ログイン'}
        </button>
      </div>

      <p>
        アカウントをお持ちでない方：
        <Link href={'/signup'} className="link link-primary">
          登録
        </Link>
      </p>
    </div>
  );
};
