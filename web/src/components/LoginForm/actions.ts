"use server";

import { SigninResponse, signinUserSigninPost, SigninUserSigninPostError } from "@/lib/api";

/**
 * ログインする
 */
export const signinUser = async (userName: string, password: string): Promise<{
    success: boolean;
    error?: SigninUserSigninPostError;
    data?: SigninResponse;
}> => {
  const res = await signinUserSigninPost({
    body: {
      username: userName,
      password: password,
    }
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  return { success: true, data: res.data };
}
