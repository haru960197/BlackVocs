'use client';

import { useState } from 'react';

export const LoginForm = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
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
          disabled={!email || !password}
          onClick={handleClick}
        >
          {isLoading ? <span className="loading loading-spinner" /> : 'ログイン'}
        </button>
      </div>
    </div>
  );
};
