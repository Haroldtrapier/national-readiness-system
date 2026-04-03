// Role-Based Access Control Utilities
export type UserRole = 'free' | 'premium' | 'enterprise' | 'admin';
export type FeatureTier = 'free' | 'premium' | 'enterprise';

export const FEATURE_ACCESS = {
  'dashboard': 'free',
  'agency_it_command': 'free',
  'operational_briefs': 'premium',
  'county_operations': 'premium',
  'poc_command_center': 'premium',
  'vendor_operations': 'premium',
  'advanced_analytics': 'premium',
  'api_access': 'premium',
  'custom_integrations': 'enterprise',
  'dedicated_support': 'enterprise',
  'admin_panel': 'admin',
} as Record<string, FeatureTier>;

export const TIER_HIERARCHY = {
  'free': 0,
  'premium': 1,
  'enterprise': 2,
  'admin': 3,
};

export function checkAccess(userTier: UserRole, requiredTier: FeatureTier): boolean {
  return (TIER_HIERARCHY[userTier] || 0) >= (TIER_HIERARCHY[requiredTier] || 0);
}

export function getAccessMessage(userTier: UserRole, feature: string): string {
  const requiredTier = FEATURE_ACCESS[feature] || 'free';
  const hasAccess = checkAccess(userTier, requiredTier);
  
  if (hasAccess) return 'Access granted';
  return `Upgrade to ${requiredTier} to access ${feature}`;
}

export function getUpgradeUrl(feature: string): string {
  const requiredTier = FEATURE_ACCESS[feature] || 'premium';
  return `/pricing?tier=${requiredTier}&feature=${feature}`;
}