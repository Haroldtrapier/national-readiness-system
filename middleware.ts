import { NextRequest, NextResponse } from 'next/server';

// Protected routes that require authentication
const PROTECTED_ROUTES = [
  '/operational-briefs',
  '/county-operations',
  '/poc-command',
  '/vendor-operations',
  '/admin',
];

// Premium-only routes
const PREMIUM_ROUTES = [
  '/operational-briefs',
  '/county-operations',
  '/poc-command',
  '/vendor-operations',
];

export async function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  // Check if route is protected
  const isProtected = PROTECTED_ROUTES.some(route => pathname.startsWith(route));
  if (!isProtected) return NextResponse.next();

  // Get user token from cookie
  const token = request.cookies.get('auth_token')?.value;
  if (!token) {
    const loginUrl = new URL('/login', request.url);
    loginUrl.searchParams.set('next', pathname);
    return NextResponse.redirect(loginUrl);
  }

  // Check if route requires premium
  const isPremium = PREMIUM_ROUTES.some(route => pathname.startswith(route));
  if (isPremium) {
    // Validate subscription (replace with actual Supabase check)
    const userTier = request.cookies.get('user_tier')?.value || 'free';
    if (userTier === 'free') {
      const upgradeUrl = new URL('/upgrade', request.url);
      upgradeUrl.searchParams.set('feature', pathname.split('/')[1]);
      return NextResponse.redirect(upgradeUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!api|_next|.*\\..*).*)'],
};