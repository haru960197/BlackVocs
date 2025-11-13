"use server";

import { signUp, SignUpError } from "@/lib/api";

/**
 * ユーザーを新規登録する
 */
export const handleSignUpUser = async (
  userName: string,
  password: string
): Promise<{
  success: boolean;
  error?: SignUpError;
}> => {
  const res = await signUp({
    body: {
      username: userName,
      password: password,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true };
};
