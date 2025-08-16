'use server'

import { signin, SigninError, SigninResponse } from "@/lib/api";
import { cookies } from "next/headers";

export const handleSignUp = async (userName: string, password: string): Promise<{
  success: boolean;
  error?: SigninError;
  data?: SigninResponse;
}> => {
  const cookieStore = await cookies();

  const res = await signin({
    body: {
      username_or_email: userName,
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
 
