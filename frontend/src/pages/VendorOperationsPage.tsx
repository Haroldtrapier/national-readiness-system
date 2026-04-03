import { Truck, Check, Clock, AlertTriangle, Lock } from 'lucide-react';
import MetricCard from '../components/cards/MetricCard';
import DataTable from '../components/tables/DataTable';
import SubscriptionBanner from '../components/SubscriptionBanner';
import { useApi } from '../hooks/useApi';
import { useSubscription } from '../hooks/useSubscription';
import { api } from '../services/api';

export default function VendorOperationsPage() {
  const { subscribed } = useSubscription();
  const { data: vendors, loading } = useApi(
    () => api.vendors.getAll(),
    []
  );

  const contractReady = (vendors || []).filter((v: any) => v.contract_ready).length;
  const surgeCapable = (vendors || []).filter((v: any) => v.emergency_surge_capable).length;
  const avgLead = (vendors || []).reduce((sum: number, v: any) => sum + (v.lead_time_days || 0), 0) / Math.max((vendors || []).length, 1);

  const columns = [
    {
      key: 'organization_name',
      label: 'Supplier',
      render: (row: any) => subscribed
        ? <span className="text-gray-200">{row.organization_name}</span>
        : (
          <span className="inline-flex items-center gap-1 text-orange-400/70 text-xs font-medium bg-orange-500/10 border border-orange-500/20 rounded px-1.5 py-0.5 select-none">
            <Lock size={10} />
            Subscribe to View
          </span>
        ),
    },
    { key: 'vendor_type', label: 'Type' },
    { key: 'geographic_coverage', label: 'Coverage' },
    {
      key: 'contract_ready',
      label: 'Contract',
      render: (row: any) => (
        <span className={row.contract_ready ? 'text-green-400 font-medium' : 'text-red-400'}>
          {row.contract_ready ? 'Ready' : 'Not Ready'}
        </span>
      ),
    },
    {
      key: 'emergency_surge_capable',
      label: 'Emergency Surge',
      render: (row: any) => (
        <span className={row.emergency_surge_capable ? 'text-green-400 font-medium' : 'text-gray-500'}>
          {row.emergency_surge_capable ? 'Yes' : 'No'}
        </span>
      ),
    },
    {
      key: 'response_sla_hours',
      label: 'SLA (hrs)',
      render: (row: any) => row.response_sla_hours != null ? `${row.response_sla_hours}h` : '-',
    },
    {
      key: 'lead_time_days',
      label: 'Lead Time',
      render: (row: any) => row.lead_time_days != null ? `${row.lead_time_days}d` : '-',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Vendor Operations</h1>
        <p className="text-sm text-gray-400 mt-0.5">
          Supply and IT vendor network, capacity, and fulfillment readiness
        </p>
      </div>

      {!subscribed && <SubscriptionBanner />}

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard title="Total Suppliers" value={(vendors || []).length} icon={Truck} color="blue" />
            <MetricCard title="Contract Ready" value={contractReady} icon={Check} color="green" />
            <MetricCard title="Surge Capable" value={surgeCapable} icon={AlertTriangle} color="orange" />
            <MetricCard title="Avg Lead Time" value={`${avgLead.toFixed(1)} days`} icon={Clock} color="purple" />
          </div>

          <DataTable
            columns={columns}
            data={vendors || []}
            searchKey="vendor_type"
            emptyMessage="No vendors loaded"
          />
        </>
      )}
    </div>
  );
}
