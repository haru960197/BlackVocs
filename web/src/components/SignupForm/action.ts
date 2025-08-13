"use server";

import { signupUser } from "@/lib/api";

/**
 * ユーザーを新規登録する
 */
export const handleSignupUser = async (userName: string, email: string, password: string): Promise<{
    success: boolean;
    error?: string;
}> => {
  const res = await signupUser({
    body: {
      username: userName,
      email: email,
      password: password,
    }
  });

  if (res.error) {
    console.log(res.error);
    return { success: false, error: typeof(res.error) === "string" ? res.error : res.error[0].msg };
  }

  return { success: true };
}
