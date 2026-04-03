import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { userId, feature } = await request.json();
    
    if (!userId || !feature) {
      return NextResponse.json(
        { error: 'userId and feature are required' },
        { status: 400 }
      );
    }

    // TODO: Replace with actual Supabase query
    // const supabase = createClient(...);
    // const { data: user } = await supabase
    //   .from('users')
    //   .select('role')
    //   .eq('id', userId)
    //   .single();

    // Mock implementation for now
    const userRole = 'free'; // Replace with actual data from Supabase
    const features: Record<string, string> = {
      'dashboard': 'free',
      'agency_it_command': 'free',
      'operational_briefs': 'premium',
      'county_operations': 'premium',
      'poc_command_center': 'premium',
      'vendor_operations': 'premium',
      'advanced_analytics': 'premium',
      'api_access': 'premium',
      'custom_integrations': 'enterprise',
    };

    const requiredTier = features[feature] || 'free';
    const tierHierarchy: Record<string, number> = { free: 0, premium: 1, enterprise: 2, admin: 3 };
    const hasAccess = (tierHierarchy[userRole] || 0) >= (tierHierarchy[requiredTier] || 0);

    return NextResponse.json({
      hasAccess,
      userRole,
      requiredTier,
      feature,
      message: hasAccess ? 'Access granted' : `Upgrade to ${requiredTier} to access this feature`,
      upgradeUrl: `/pricing?tier=${requiredTier}&feature=${feature}`,
    });
  } catch (error) {
    console.error('Access check error:', error);
    return NextResponse.json(
      { error: 'Failed to check access' },
      { status: 500 }
    );
  }
}