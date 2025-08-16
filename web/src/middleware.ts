import { NextRequest, NextResponse } from "next/server";
import { ACCESS_TOKEN_KEY } from "./constant/auth";

export function middleware(request: NextRequest) {
  const tokenCookie = request.cookies.get(ACCESS_TOKEN_KEY);

  if (!tokenCookie) {
    // クッキーがない場合はログインページにリダイレクト
    const loginUrl = new URL('/login', request.url);

    // 現在のアクセス先をログイン後のページに設定
    loginUrl.searchParams.set('next', request.nextUrl.pathname);

    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/word-list/:path*',
    '/register-word/:path*',
  ],
}

