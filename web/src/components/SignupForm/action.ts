'use server';

import { SignupResponse, signup, SignupError } from '@/lib/api';

/**
 * ユーザーを新規登録する
 */
export const handleSignupUser = async (
  userName: string,
  email: string,
  password: string
): Promise<{
  success: boolean;
  error?: SignupError;
  data?: SignupResponse;
}> => {
  const res = await signup({
    body: {
      email: email,
      username: userName,
      password: password,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true, data: res.data };
};
