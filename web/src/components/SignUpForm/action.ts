'use server';

import { SignUpResponse, signUp, SignUpError } from '@/lib/api';

/**
 * ユーザーを新規登録する
 */
export const handleSignUpUser = async (
  userName: string,
  email: string,
  password: string
): Promise<{
  success: boolean;
  error?: SignUpError;
  data?: SignUpResponse;
}> => {
  const res = await signUp({
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
