'use server'

import { signedInCheck, SignedInCheckResponse, signin, SigninError, SigninResponse, signout } from "@/lib/api";
import { cookies } from "next/headers";

export const handleLogin = async (userName: string, password: string): Promise<{
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
 
export const handleLogout = async (): Promise<{
  success: boolean;
}> => {
  const res = await signout();

  if (res.error) {
    return { success: false };
  }

  return { success: true };
}

export const loggedInCheck = async (): Promise<{
  success: boolean;
  data?: SignedInCheckResponse;
}> => {
  const cookieStore = await cookies();
  const tokenCookie = cookieStore.get('access_token');

  const res = await signedInCheck({
    headers: {
      Cookie: `${tokenCookie?.name}=${tokenCookie?.value}`,
    },
  });

  if (res.error) {
    return { success: false };
  }

  return { success: true, data: res.response };
}


