-- Users table with role management
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR UNIQUE NOT NULL,
  role VARCHAR DEFAULT 'free',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Subscriptions table for billing
CREATE TABLE IF NOT EXISTS subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  plan VARCHAR NOT NULL CHECK (plan IN ('free', 'premium', 'enterprise')),
  status VARCHAR DEFAULT 'active',
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  stripe_customer_id VARCHAR,
  stripe_subscription_id VARCHAR,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Feature access log for analytics
CREATE TABLE IF NOT EXISTS feature_access_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  feature VARCHAR NOT NULL,
  allowed BOOLEAN NOT NULL,
  tier_at_access VARCHAR,
  timestamp TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX IF NOT EXISTS idx_subscriptions_status ON subscriptions(status);
CREATE INDEX IF NOT EXISTS idx_access_log_user_id ON feature_access_log(user_id);
CREATE INDEX IF NOT EXISTS idx_access_log_timestamp ON feature_access_log(timestamp);

-- Sample data (optional - remove in production)
INSERT INTO users (email, role) VALUES
  ('demo@example.com', 'free'),
  ('premium@example.com', 'premium'),
  ('enterprise@example.com', 'enterprise')
ON CONFLICT (email) DO NOTHING;