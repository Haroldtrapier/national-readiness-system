import { useState } from 'react';
import { MapPin, AlertTriangle, Package } from 'lucide-react';
import MetricCard from '../components/cards/MetricCard';
import ReadinessBadge from '../components/ReadinessBadge';
import SupplyGapCard from '../components/cards/SupplyGapCard';
import DataTable from '../components/tables/DataTable';
import PocCard from '../components/cards/PocCard';
import { useApi } from '../hooks/useApi';
import { api } from '../services/api';

const PILOT_COUNTIES = [
  { fips: '37119', label: 'Mecklenburg, NC' },
  { fips: '37183', label: 'Wake, NC' },
  { fips: '37129', label: 'New Hanover, NC' },
  { fips: '45019', label: 'Charleston, SC' },
  { fips: '13051', label: 'Chatham, GA' },
  { fips: '12086', label: 'Miami-Dade, FL' },
  { fips: '48201', label: 'Harris, TX' },
  { fips: '22071', label: 'Orleans, LA' },
];

export default function CountyOperationsPage() {
  const [selectedCounty, setSelectedCounty] = useState('37119');

  const { data: countyHazards, loading } = useApi(
    () => api.hazards.getCountyHazards(selectedCounty),
    [selectedCounty]
  );

  const { data: supplyReqs } = useApi(
    () => api.supplies.getRequirements(selectedCounty),
    [selectedCounty]
  );

  const { data: pocs } = useApi(
    () => api.pocs.getLocal(selectedCounty),
    [selectedCounty]
  );

  const hazards = countyHazards?.hazards || [];
  const requirements = supplyReqs?.requirements || [];
  const maxBand = hazards.length > 0 ? hazards[0].readiness_band : 'GREEN';

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold">County Operations</h1>
          <p className="text-sm text-gray-400 mt-0.5">County-level hazard, supply, and contact view</p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-400">County:</label>
          <select
            value={selectedCounty}
            onChange={e => setSelectedCounty(e.target.value)}
            className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-orange-500"
          >
            {PILOT_COUNTIES.map(c => (
              <option key={c.fips} value={c.fips}>{c.label}</option>
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
              title="County"
              value={countyHazards?.county_name || selectedCounty}
              icon={MapPin}
              color="blue"
            />
            <MetricCard
              title="Active Hazards"
              value={hazards.length}
              icon={AlertTriangle}
              color="orange"
            />
            <MetricCard
              title="Supply Shortages"
              value={requirements.length}
              icon={Package}
              color="red"
            />
            <div className="rounded-xl border border-gray-700/50 bg-gray-800/30 p-4">
              <p className="text-xs font-medium text-gray-400 uppercase tracking-wide">Readiness</p>
              <div className="mt-2">
                <ReadinessBadge band={maxBand} size="md" />
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Active Hazards</h3>
              <DataTable
                columns={[
                  { key: 'hazard_name', label: 'Hazard' },
                  {
                    key: 'readiness_band',
                    label: 'Risk',
                    render: (row: any) => <ReadinessBadge band={row.readiness_band} />,
                  },
                  {
                    key: 'hazard_score',
                    label: 'Score',
                    render: (row: any) => row.hazard_score != null ? row.hazard_score.toFixed(1) : '-',
                  },
                  {
                    key: 'probability_score',
                    label: 'Probability',
                    render: (row: any) => row.probability_score != null ? `${(row.probability_score * 100).toFixed(0)}%` : '-',
                  },
                  { key: 'confidence_band', label: 'Confidence' },
                ]}
                data={hazards}
                emptyMessage="No active hazards"
              />

              {requirements.length > 0 && (
                <>
                  <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mt-6">Supply Requirements</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {requirements.map((req: any, i: number) => (
                      <SupplyGapCard
                        key={i}
                        itemName={req.item_name}
                        required={req.required_quantity}
                        available={req.available_quantity}
                        shortage={req.shortage_quantity}
                        shortagePct={req.shortage_pct}
                      />
                    ))}
                  </div>
                </>
              )}
            </div>

            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Local Contacts</h3>
              {(pocs || []).length === 0 ? (
                <p className="text-sm text-gray-500">No local POCs loaded for this county</p>
              ) : (
                (pocs || []).map((poc: any) => <PocCard key={poc.id} poc={poc} />)
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
