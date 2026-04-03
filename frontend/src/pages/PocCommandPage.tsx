import { useState } from 'react';
import { Users, Phone, Shield, Building2 } from 'lucide-react';
import MetricCard from '../components/cards/MetricCard';
import PocCard from '../components/cards/PocCard';
import SubscriptionBanner from '../components/SubscriptionBanner';
import { useApi } from '../hooks/useApi';
import { useSubscription } from '../hooks/useSubscription';
import { api } from '../services/api';

const CONTACT_TYPES = [
  { value: '', label: 'All Types' },
  { value: 'fema_ops', label: 'FEMA Operations' },
  { value: 'fema_logistics', label: 'FEMA Logistics' },
  { value: 'sema_leadership', label: 'SEMA Leadership' },
  { value: 'sema_logistics', label: 'SEMA Logistics' },
  { value: 'local_em', label: 'Local EM' },
  { value: 'it_owner', label: 'IT Owner' },
  { value: 'vendor_sales', label: 'Vendor' },
];

export default function PocCommandPage() {
  const [contactType, setContactType] = useState('');
  const [stateFilter, setStateFilter] = useState('');
  const { subscribed } = useSubscription();

  const { data: pocs, loading } = useApi(
    () => api.pocs.getAll(contactType || undefined, stateFilter || undefined),
    [contactType, stateFilter]
  );

  const pocsList = pocs || [];
  const femaCount = pocsList.filter((p: any) => p.contact_type.startsWith('fema')).length;
  const semaCount = pocsList.filter((p: any) => p.contact_type.startsWith('sema')).length;
  const localCount = pocsList.filter((p: any) => p.contact_type === 'local_em').length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold">POC Command Center</h1>
          <p className="text-sm text-gray-400 mt-0.5">
            FEMA, SEMA, local, IT, and vendor contact directory
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={contactType}
            onChange={e => setContactType(e.target.value)}
            className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-orange-500"
          >
            {CONTACT_TYPES.map(ct => (
              <option key={ct.value} value={ct.value}>{ct.label}</option>
            ))}
          </select>
          <select
            value={stateFilter}
            onChange={e => setStateFilter(e.target.value)}
            className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-orange-500"
          >
            <option value="">All States</option>
            {['NC', 'SC', 'GA', 'FL', 'TX', 'LA', 'VA', 'MD', 'PA'].map(s => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
      </div>

      {!subscribed && <SubscriptionBanner />}

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard title="Total Contacts" value={pocsList.length} icon={Users} color="blue" />
            <MetricCard title="FEMA Contacts" value={femaCount} icon={Shield} color="orange" />
            <MetricCard title="SEMA Contacts" value={semaCount} icon={Building2} color="green" />
            <MetricCard title="Local EM" value={localCount} icon={Phone} color="purple" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {pocsList.map((poc: any) => (
              <PocCard key={poc.id} poc={poc} subscribed={subscribed} />
            ))}
          </div>

          {pocsList.length === 0 && (
            <div className="p-8 text-center text-gray-500">
              No contacts found for the selected filters
            </div>
          )}
        </>
      )}
    </div>
  );
}
