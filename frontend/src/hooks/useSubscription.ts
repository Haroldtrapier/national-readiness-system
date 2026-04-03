import { useState, useEffect } from 'react';

const GOVCON_VERIFY_URL = 'https://govconcommandcenter.com/api/verify-nrs-access';
const GOVCON_URL = 'https://govconcommandcenter.com'; // eslint-disable-line @typescript-eslint/no-unused-vars
const STORAGE_KEY = 'nrs_access_token';

/**
 * useSubscription
 *
 * Tied to GovCon Command Center. Subscription status is verified by calling
 * the GovCon platform API with the stored access token.
 *
 * Flow:
 *  1. After subscribing on GovCon, users are redirected here with ?nrs_token=<token>
 *  2. The token is stored in localStorage and verified against GovCon's API.
 *  3. If valid, subscribed = true and POC/supplier details are unlocked.
 *
 * To grant access manually (dev/testing):
 *   localStorage.setItem('nrs_access_token', '<token>')
 */
export function useSubscription(): { subscribed: boolean; loading: boolean } {
  const [subscribed, setSubscribed] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function verify() {
      // 1. Check URL for a token passed from GovCon after signup
      const params = new URLSearchParams(window.location.search);
      const urlToken = params.get('nrs_token');
      if (urlToken) {
        localStorage.setItem(STORAGE_KEY, urlToken);
        // Clean token from URL without reload
        const url = new URL(window.location.href);
        url.searchParams.delete('nrs_token');
        window.history.replaceState({}, '', url.toString());
      }

      const token = localStorage.getItem(STORAGE_KEY);
      if (!token) {
        setSubscribed(false);
        setLoading(false);
        return;
      }

      // 2. Verify token against GovCon platform
      try {
        const res = await fetch(GOVCON_VERIFY_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ token }),
        });
        if (res.ok) {
          const data = await res.json();
          setSubscribed(data.valid === true);
          if (!data.valid) localStorage.removeItem(STORAGE_KEY);
        } else {
          setSubscribed(false);
          localStorage.removeItem(STORAGE_KEY);
        }
      } catch {
        // If GovCon API is unreachable, fall back to trusting the stored token
        // so subscribers aren't locked out by a network blip
        setSubscribed(true);
      } finally {
        setLoading(false);
      }
    }

    verify();
  }, []);

  return { subscribed, loading };
}
