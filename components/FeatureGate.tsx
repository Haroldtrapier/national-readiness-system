'use client';

import React, { useState, useEffect } from 'react';

interface FeatureGateProps {
  feature: string;
  requiredTier: string;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export default function FeatureGate({
  feature,
  requiredTier,
  children,
  fallback,
}: FeatureGateProps) {
  const [hasAccess, setHasAccess] = useState(false);
  const [loading, setLoading] = useState(true);
  const [upgradeUrl, setUpgradeUrl] = useState('/pricing');

  useEffect(() => {
    async function checkAccess() {
      try {
        // TODO: Get actual userId from session/context
        const response = await fetch('/api/auth/check-access', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userId: 'current-user', feature }),
        });

        const data = await response.json();
        setHasAccess(data.hasAccess);
        setUpgradeUrl(data.upgradeUrl || '/pricing');
      } catch (error) {
        console.error('Access check failed:', error);
        setHasAccess(false);
      } finally {
        setLoading(false);
      }
    }

    checkAccess();
  }, [feature]);

  if (loading) {
    return <div className="text-center py-10 text-gray-400">Loading...</div>;
  }

  if (!hasAccess) {
    return fallback || (
      <div className="border border-orange-400 bg-orange-50 p-8 rounded-lg text-center">
        <div className="text-6xl mb-4">🔒</div>
        <h3 className="font-bold text-2xl text-orange-900 mb-2">Premium Feature</h3>
        <p className="text-orange-800 mb-6">
          Upgrade to <strong>{requiredTier}</strong> tier to access this feature
        </p>
        <a 
          href={upgradeUrl}
          className="inline-block px-6 py-3 bg-orange-600 text-white rounded-lg hover:bg-orange-700 font-bold transition"
        >
          Upgrade Now →
        </a>
      </div>
    );
  }

  return <>{children}</>;
}