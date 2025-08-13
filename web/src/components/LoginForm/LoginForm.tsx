'use client';

import { useToast } from '@/context/ToastContext';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState } from 'react';
import { signinUser } from '@/lib/api';

export const LoginForm = () => {
  const router = useRouter();
  const { showToast } = useToast();

  const [userName, setUserName] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const isDisabled = !userName || !password;

  const handleClick = async () => {
    if (isDisabled) {
      return;
    }

    setIsLoading(true);

    const res = await signinUser({
      body: {
        username: userName,
        password: password,
      }
    });

    if (!res.error) {
      // ログインに成功したので，単語一覧ページにリダイレクトする
      showToast('ログインに成功しました', 'success');
      router.push('/word-list');
    } else {
      // ログインに失敗
      showToast('ログインに失敗しました', 'error');
    }

    setIsLoading(false);
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
