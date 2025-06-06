'use client';

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { signupUser } from './action';

export const SignupForm = () => {
  const [email, setEmail] = useState<string>('');
  const [userName, setUserName] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isDisabled, setIsDisabled] = useState<boolean>(!email || !userName || !password);

  useEffect(() => {
    setIsDisabled(!email || !userName || !password);
  }, [email, userName, password]);

  const handleClick = async () => {
    if (isDisabled) {
      return;
    }

    setIsLoading(true);

    await signupUser(userName, email, password);

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
