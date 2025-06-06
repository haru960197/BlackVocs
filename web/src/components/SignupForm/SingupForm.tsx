'use client';

import Link from 'next/link';
import { useState } from 'react';
import { signupUser } from './action';
import { useRouter } from 'next/navigation';
import { useToast } from '@/context/ToastContext';

export const SignupForm = () => {
  const router = useRouter();

  const { showToast } = useToast();

  const [email, setEmail] = useState<string>('');
  const [userName, setUserName] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const isDisabled = !email || !userName || !password;

  const handleClick = async () => {
    if (isDisabled) {
      return;
    }

    setIsLoading(true);

    const response = await signupUser(userName, email, password);

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

    setIsLoading(false);
  };

  return (
    <div className="flex flex-col border-1 bg-base-200 border-base-300 rounded-lg p-4 gap-2">
      <fieldset className="fieldset">
        <label className="label text-lg">Email</label>
        <input
          type="email"
          className="input text-xl"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

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
          {isLoading ? <span className="loading loading-spinner" /> : '登録'}
        </button>
      </div>

      <p>
        アカウントをお持ちの方：
        <Link href={'/login'} className="link link-primary">
          ログイン
        </Link>
      </p>
    </div>
  );
};
