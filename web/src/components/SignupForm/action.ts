"use server";

import { signupUserSignupPost } from "@/lib/api";

/**
 * ユーザーを新規登録する
 * @param userName 
 * @param email 
 * @param password 
 */
export const signupUser = async (userName: string, email: string, password: string) => {
  await signupUserSignupPost({
    body: {
      username: userName,
      email: email,
      password: password,
    }
  });
}
