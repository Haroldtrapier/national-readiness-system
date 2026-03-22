import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { Shield, AlertTriangle, MapPin } from 'lucide-react';
import MetricCard from '../components/cards/MetricCard';
import ReadinessBadge from '../components/ReadinessBadge';
import DataTable from '../components/tables/DataTable';
import PocCard from '../components/cards/PocCard';
import { useApi } from '../hooks/useApi';
import { api } from '../services/api';

export default function RegionOperationsPage() {
  const [searchParams] = useSearchParams();
  const initialRegion = parseInt(searchParams.get('region') || '4');
  const [selectedRegion, setSelectedRegion] = useState(initialRegion);

  const { data: regionData, loading } = useApi(
    () => api.hazards.getRegionHazards(selectedRegion),
    [selectedRegion]
  );

  const { data: pocs } = useApi(
    () => api.pocs.getFema(selectedRegion),
    [selectedRegion]
  );

  const { data: vendors } = useApi(
    () => api.vendors.getByRegion(selectedRegion),
    [selectedRegion]
  );

  const { data: brief } = useApi(
    () => api.briefs.getRegion(selectedRegion),
    [selectedRegion]
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold">FEMA Region Operations</h1>
          <p className="text-sm text-gray-400 mt-0.5">Regional hazard and operations command view</p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-400">Region:</label>
          <select
            value={selectedRegion}
            onChange={e => setSelectedRegion(parseInt(e.target.value))}
            className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-orange-500"
          >
            {Array.from({ length: 10 }, (_, i) => i + 1).map(n => (
              <option key={n} value={n}>Region {n}</option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Region"
              value={`Region ${selectedRegion}`}
              subtitle={regionData?.region_name || ''}
              icon={Shield}
              color="blue"
            />
            <MetricCard
              title="Active Hazards"
              value={regionData?.active_hazards || 0}
              icon={AlertTriangle}
              color="orange"
            />
            <MetricCard
              title="Counties at Risk"
              value={regionData?.counties_at_risk || 0}
              icon={MapPin}
              color="red"
            />
            <div className="rounded-xl border border-gray-700/50 bg-gray-800/30 p-4">
              <p className="text-xs font-medium text-gray-400 uppercase tracking-wide">Readiness Level</p>
              <div className="mt-2">
                <ReadinessBadge band={regionData?.readiness_band || 'GREEN'} size="md" />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">County Hazards</h3>
              <DataTable
                columns={[
                  { key: 'county_name', label: 'County' },
                  { key: 'state_code', label: 'State' },
                  { key: 'hazard_name', label: 'Hazard' },
                  {
                    key: 'readiness_band',
                    label: 'Risk',
                    render: (row: any) => <ReadinessBadge band={row.readiness_band} />,
                  },
                  {
                    key: 'probability_score',
                    label: 'Probability',
                    render: (row: any) => row.probability_score != null ? `${(row.probability_score * 100).toFixed(0)}%` : '-',
                  },
                ]}
                data={regionData?.hazards || []}
                searchKey="county_name"
                emptyMessage="No hazards detected in this region"
              />
            </div>

            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Region Contacts</h3>
              {(pocs || []).length === 0 ? (
                <p className="text-sm text-gray-500">No contacts loaded for this region</p>
              ) : (
                (pocs || []).map((poc: any) => <PocCard key={poc.id} poc={poc} />)
              )}

              {brief?.recommended_actions && brief.recommended_actions.length > 0 && (
                <div className="mt-4">
                  <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-2">Recommended Actions</h3>
                  <ul className="space-y-1.5">
                    {brief.recommended_actions.slice(0, 8).map((action: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-xs text-gray-400">
                        <span className="text-orange-400 mt-0.5">&#8226;</span>
                        {action}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {vendors && vendors.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">Regional Vendors</h3>
              <DataTable
                columns={[
                  { key: 'organization_name', label: 'Vendor' },
                  { key: 'vendor_type', label: 'Type' },
                  { key: 'geographic_coverage', label: 'Coverage' },
                  {
                    key: 'contract_ready',
                    label: 'Contract',
                    render: (row: any) => (
                      <span className={row.contract_ready ? 'text-green-400' : 'text-red-400'}>
                        {row.contract_ready ? 'Ready' : 'Not Ready'}
                      </span>
                    ),
                  },
                  {
                    key: 'emergency_surge_capable',
                    label: 'Surge',
                    render: (row: any) => (
                      <span className={row.emergency_surge_capable ? 'text-green-400' : 'text-gray-500'}>
                        {row.emergency_surge_capable ? 'Yes' : 'No'}
                      </span>
                    ),
                  },
                ]}
                data={vendors}
                searchKey="organization_name"
              />
            </div>
          )}
        </>
      )}
    </div>
  );
}
