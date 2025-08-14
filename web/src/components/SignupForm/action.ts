"use server";

import { SignupResponse, signin, SignupError } from "@/lib/api";

/**
 * ユーザーを新規登録する
 */
export const handleSignupUser = async (userName: string, email: string, password: string): Promise<{
    success: boolean;
    error?: SignupError;
    data?: SignupResponse;
}> => {
  const res = await signin({
    body: {
      username_or_email: userName,
      password: password,
    }
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true, data: res.data };
}
