import { Phone, Mail, Clock } from 'lucide-react';
import type { Poc } from '../../types';

interface PocCardProps {
  poc: Poc;
}

export default function PocCard({ poc }: PocCardProps) {
  const typeLabels: Record<string, string> = {
    fema_ops: 'FEMA Operations',
    fema_logistics: 'FEMA Logistics',
    sema_leadership: 'State EM Leadership',
    sema_logistics: 'State EM Logistics',
    local_em: 'Local Emergency Management',
    it_owner: 'IT Operations',
    vendor_sales: 'Vendor Contact',
  };

  return (
    <div className="p-3 rounded-lg bg-gray-800/50 border border-gray-700/50">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium">{poc.contact_name}</p>
          {poc.title && <p className="text-xs text-gray-400">{poc.title}</p>}
          {poc.organization_name && <p className="text-xs text-gray-500">{poc.organization_name}</p>}
        </div>
        <span className="text-[10px] uppercase tracking-wider font-semibold text-blue-400 bg-blue-500/10 border border-blue-500/20 rounded px-1.5 py-0.5">
          {typeLabels[poc.contact_type] || poc.contact_type}
        </span>
      </div>
      <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
        {poc.phone && (
          <a href={`tel:${poc.phone}`} className="flex items-center gap-1 hover:text-blue-400 transition-colors">
            <Phone size={12} />
            {poc.phone}
          </a>
        )}
        {poc.email && (
          <a href={`mailto:${poc.email}`} className="flex items-center gap-1 hover:text-blue-400 transition-colors">
            <Mail size={12} />
            Email
          </a>
        )}
        {poc.availability_type && (
          <span className="flex items-center gap-1">
            <Clock size={12} />
            {poc.availability_type}
          </span>
        )}
      </div>
    </div>
  );
}
