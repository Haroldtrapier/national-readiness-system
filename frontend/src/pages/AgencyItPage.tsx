import { useState, useMemo } from 'react';
import { Monitor, AlertTriangle, Clock, Zap } from 'lucide-react';
import MetricCard from '../components/cards/MetricCard';
import DataTable from '../components/tables/DataTable';
import AssetAgeChart from '../components/charts/AssetAgeChart';
import { useApi } from '../hooks/useApi';
import { api } from '../services/api';

export default function AgencyItPage() {
  const { data: agencies, loading: loadingAgencies } = useApi(
    () => api.agencies.getAll(),
    []
  );

  const [selectedAgency, setSelectedAgency] = useState<string>('');

  const agencyId = selectedAgency || (agencies && agencies.length > 0 ? agencies[0].id : '');

  const { data: itSummary, loading: loadingIt } = useApi(
    () => agencyId ? api.itAssets.getAgencyAssets(agencyId) : Promise.resolve(null),
    [agencyId]
  );

  const assetChartData = useMemo(() => {
    if (!itSummary?.assets) return [];
    const typeCounts: Record<string, number> = {};
    for (const a of itSummary.assets) {
      typeCounts[a.asset_type] = (typeCounts[a.asset_type] || 0) + 1;
    }
    const colors = ['#3b82f6', '#f97316', '#22c55e', '#8b5cf6', '#eab308', '#ec4899'];
    return Object.entries(typeCounts).map(([name, value], i) => ({
      name,
      value,
      color: colors[i % colors.length],
    }));
  }, [itSummary]);

  const securityChartData = useMemo(() => {
    if (!itSummary?.assets) return [];
    const statusCounts: Record<string, number> = {};
    for (const a of itSummary.assets) {
      const status = a.security_status || 'unknown';
      statusCounts[status] = (statusCounts[status] || 0) + 1;
    }
    const colorMap: Record<string, string> = {
      compliant: '#22c55e',
      upgrade_needed: '#f97316',
      non_compliant: '#ef4444',
      unknown: '#6b7280',
    };
    return Object.entries(statusCounts).map(([name, value]) => ({
      name,
      value,
      color: colorMap[name] || '#6b7280',
    }));
  }, [itSummary]);

  const loading = loadingAgencies || loadingIt;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold">Agency IT Command</h1>
          <p className="text-sm text-gray-400 mt-0.5">
            Lifecycle, replacement, and surge device planning
          </p>
        </div>
        {agencies && agencies.length > 0 && (
          <div className="flex items-center gap-2">
            <label className="text-sm text-gray-400">Agency:</label>
            <select
              value={agencyId}
              onChange={e => setSelectedAgency(e.target.value)}
              className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-orange-500"
            >
              {agencies.map((a: any) => (
                <option key={a.id} value={a.id}>{a.organization_name}</option>
              ))}
            </select>
          </div>
        )}
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : itSummary ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Total Assets"
              value={itSummary.total_assets}
              icon={Monitor}
              color="blue"
            />
            <MetricCard
              title="90-Day Warranty Expirations"
              value={itSummary.expiring_warranty_90d}
              icon={Clock}
              color="yellow"
            />
            <MetricCard
              title="High-Risk Replacements"
              value={itSummary.high_risk_replacements}
              icon={AlertTriangle}
              color="red"
            />
            <MetricCard
              title="Surge Devices Needed"
              value={itSummary.surge_devices_needed}
              icon={Zap}
              color="orange"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AssetAgeChart data={assetChartData} title="Asset Type Distribution" />
            <AssetAgeChart data={securityChartData} title="Security Status" />
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Asset Inventory</h3>
            <DataTable
              columns={[
                { key: 'asset_tag', label: 'Tag' },
                { key: 'asset_type', label: 'Type' },
                { key: 'manufacturer', label: 'Manufacturer' },
                { key: 'model', label: 'Model' },
                { key: 'purchase_date', label: 'Purchased' },
                { key: 'warranty_end_date', label: 'Warranty End' },
                { key: 'operating_status', label: 'Status' },
                {
                  key: 'security_status',
                  label: 'Security',
                  render: (row: any) => (
                    <span className={
                      row.security_status === 'compliant' ? 'text-green-400' :
                      row.security_status === 'upgrade_needed' ? 'text-orange-400' : 'text-gray-400'
                    }>
                      {row.security_status}
                    </span>
                  ),
                },
                {
                  key: 'replacement_score',
                  label: 'Risk Score',
                  render: (row: any) => {
                    const score = row.replacement_score || 0;
                    const color = score >= 70 ? 'text-red-400' : score >= 40 ? 'text-orange-400' : 'text-green-400';
                    return <span className={`font-bold ${color}`}>{score.toFixed(0)}</span>;
                  },
                },
              ]}
              data={itSummary.assets || []}
              searchKey="asset_tag"
            />
          </div>

          {itSummary.forecasts && itSummary.forecasts.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Demand Forecasts</h3>
              <DataTable
                columns={[
                  { key: 'item_category', label: 'Item Category' },
                  { key: 'quantity_needed', label: 'Qty Needed' },
                  { key: 'date_needed', label: 'Date Needed' },
                  { key: 'reason_code', label: 'Reason' },
                  {
                    key: 'confidence_score',
                    label: 'Confidence',
                    render: (row: any) => row.confidence_score != null ? `${(row.confidence_score * 100).toFixed(0)}%` : '-',
                  },
                  {
                    key: 'procurement_action_score',
                    label: 'Action Score',
                    render: (row: any) => row.procurement_action_score != null ? row.procurement_action_score.toFixed(1) : '-',
                  },
                  { key: 'notes', label: 'Notes' },
                ]}
                data={itSummary.forecasts}
              />
            </div>
          )}
        </>
      ) : (
        <div className="p-8 text-center text-gray-500">
          <p>No agencies loaded. Run the seed script to populate data.</p>
        </div>
      )}
    </div>
  );
}
