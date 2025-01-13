'use server';

import { NextRequest, NextResponse } from 'next/server';
import { tokenProvider } from './app/lib/JWTProvider';


const protectedRoutes = ['/profile'];
const publicRoutes = ['/login', '/register', '/'];

export async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname;
  const isProtectedRoute = protectedRoutes.includes(path);
  const isPublicRoute = publicRoutes.includes(path);

  const { isLogged } = await tokenProvider(req);

  // console.log(isLogged, path, isProtectedRoute)

  if (isProtectedRoute && !isLogged) {
    return NextResponse.redirect(new URL('/login', req.nextUrl));
  }

  return NextResponse.next();
}

export const config = {
  matcher: '/profile',
};