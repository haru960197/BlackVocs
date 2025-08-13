"use server";

import { SignupResponse, signupUser, SignupUserError } from "@/lib/api";

/**
 * ユーザーを新規登録する
 */
export const handleSignupUser = async (userName: string, email: string, password: string): Promise<{
    success: boolean;
    error?: SignupUserError;
    data?: SignupResponse;
}> => {
  const res = await signupUser({
    body: {
      username: userName,
      email: email,
      password: password,
    }
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true, data: res.data };
}
