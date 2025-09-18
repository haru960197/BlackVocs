'use server';

import { ACCESS_TOKEN_KEY } from '@/constant/auth';
import {
  signedInCheck,
  SignedInCheckResponse,
  signIn,
  SignInError,
  SignInResponse,
  signOut,
} from '@/lib/api';
import { cookies } from 'next/headers';

export const handleLogin = async (
  userName: string,
  password: string
): Promise<{
  success: boolean;
  error?: SignInError;
  data?: SignInResponse;
}> => {
  const cookieStore = await cookies();

  const res = await signIn({
    body: {
      username_or_email: userName,
      password: password,
    },
  });

  if (res.error) {
    return { success: false, error: res.error };
  }

  cookieStore.set(ACCESS_TOKEN_KEY, res.data.access_token, {
    httpOnly: true,
    maxAge: 60 * 60,
    sameSite: 'none',
    secure: true,
  });

  return { success: true, data: res.data };
};

export const handleLogout = async (): Promise<{
  success: boolean;
}> => {
  const cookieStore = await cookies();

  const res = await signOut();

  if (res.error) {
    return { success: false };
  }

  cookieStore.delete(ACCESS_TOKEN_KEY);

  return { success: true };
};

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

  return { success: true, data: res.data };
};
