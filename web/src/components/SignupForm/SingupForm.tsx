'use client';

import Link from 'next/link';
import { useState } from 'react';

export const SignupForm = () => {
  const [email, setEmail] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleClick = async () => {
    setIsLoading(true);

    // TODO: ログインAPIを叩く

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
      </fieldset>

      <div className="flex justify-end">
        <button
          className="btn btn-primary btn-sm lg:btn-lg text-lg lg:text-xl"
          disabled={!email}
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
