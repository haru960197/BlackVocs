"use server";

import { HttpValidationError, SignupResponse, signupUserSignupPost, SignupUserSignupPostError } from "@/lib/api";

/**
 * ユーザーを新規登録する
 */
export const signupUser = async (userName: string, email: string, password: string): Promise<{
    success: boolean;
    error?: SignupUserSignupPostError;
    data?: SignupResponse;
}> => {
  const res = await signupUserSignupPost({
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
