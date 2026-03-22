import { Check, X, Clock, Truck } from 'lucide-react';
import type { VendorMatch } from '../../types';

interface VendorMatchCardProps {
  vendor: VendorMatch;
}

export default function VendorMatchCard({ vendor }: VendorMatchCardProps) {
  const fitColor =
    vendor.fit_score >= 0.8 ? 'text-green-400' :
    vendor.fit_score >= 0.6 ? 'text-yellow-400' :
    vendor.fit_score >= 0.4 ? 'text-orange-400' : 'text-red-400';

  return (
    <div className="p-3 rounded-lg bg-gray-800/50 border border-gray-700/50 hover:border-gray-600/50 transition-colors">
      <div className="flex items-start justify-between">
        <div>
          <span className="text-sm font-medium">{vendor.vendor_name}</span>
          <p className="text-xs text-gray-500 mt-0.5">{vendor.vendor_type}</p>
        </div>
        <span className={`text-sm font-bold ${fitColor}`}>{(vendor.fit_score * 100).toFixed(0)}%</span>
      </div>
      <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
        <span className="flex items-center gap-1">
          {vendor.contract_ready ? <Check size={12} className="text-green-400" /> : <X size={12} className="text-red-400" />}
          Contract
        </span>
        <span className="flex items-center gap-1">
          {vendor.emergency_surge_capable ? <Check size={12} className="text-green-400" /> : <X size={12} className="text-red-400" />}
          Surge
        </span>
        {vendor.response_sla_hours && (
          <span className="flex items-center gap-1">
            <Clock size={12} />
            {vendor.response_sla_hours}h SLA
          </span>
        )}
        {vendor.lead_time_days && (
          <span className="flex items-center gap-1">
            <Truck size={12} />
            {vendor.lead_time_days}d lead
          </span>
        )}
      </div>
    </div>
  );
}
