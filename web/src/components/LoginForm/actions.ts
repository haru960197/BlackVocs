'use server'

import { signinUser, SigninUserError, SigninUserResponse } from "@/lib/api";
import { cookies } from "next/headers";

export const handleSignUp = async (userName: string, password: string): Promise<{
  success: boolean;
  error?: SigninUserError;
  data?: SigninUserResponse;
}> => {
  const cookieStore = await cookies();

  const res = await signinUser({
    body: {
      username: userName,
      password: password,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  cookieStore.set("access_token", res.data.access_token, {
    httpOnly: true,
    maxAge: 60 * 60,
    sameSite: "none",
    secure: true,
  });

  return { success: true, data: res.data };
};
 
