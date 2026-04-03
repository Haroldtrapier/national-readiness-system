import { Lock, ExternalLink } from 'lucide-react';

const GOVCON_URL = 'https://govconcommandcenter.com';

export default function SubscriptionBanner() {
  return (
    <div className="flex items-center justify-between gap-4 px-4 py-3 rounded-lg bg-orange-500/10 border border-orange-500/30 text-sm">
      <div className="flex items-center gap-2 text-orange-300">
        <Lock size={14} />
        <span>
          <strong>POC names, contact details, and supplier identities</strong> are unlocked for GovCon Command Center subscribers.
        </span>
      </div>
      <a
        href={GOVCON_URL}
        target="_blank"
        rel="noopener noreferrer"
        className="shrink-0 flex items-center gap-1.5 bg-orange-500 hover:bg-orange-400 text-black font-semibold text-xs px-3 py-1.5 rounded-lg transition-colors"
      >
        Get Access
        <ExternalLink size={12} />
      </a>
    </div>
  );
}
