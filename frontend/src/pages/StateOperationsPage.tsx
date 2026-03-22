import { useState } from 'react';
import { Building2, AlertTriangle, MapPin, Shield } from 'lucide-react';
import MetricCard from '../components/cards/MetricCard';
import ReadinessBadge from '../components/ReadinessBadge';
import DataTable from '../components/tables/DataTable';
import PocCard from '../components/cards/PocCard';
import { useApi } from '../hooks/useApi';
import { api } from '../services/api';

const PILOT_STATES = ['NC', 'SC', 'GA', 'FL', 'TX', 'LA', 'VA', 'MD', 'PA'];

export default function StateOperationsPage() {
  const [selectedState, setSelectedState] = useState('NC');

  const { data: stateHazards, loading } = useApi(
    () => api.hazards.getStateHazards(selectedState),
    [selectedState]
  );

  const { data: pocs } = useApi(
    () => api.pocs.getSema(selectedState),
    [selectedState]
  );

  const { data: itForecast } = useApi(
    () => api.itAssets.getStateForecast(selectedState),
    [selectedState]
  );

  const hazards = stateHazards?.hazards || [];
  const riskyCounties = hazards.filter((h: any) => ['ORANGE', 'RED', 'BLACK'].includes(h.readiness_band));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold">State Operations</h1>
          <p className="text-sm text-gray-400 mt-0.5">
            State-level emergency, supply, and IT operations view
          </p>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-400">State:</label>
          <select
            value={selectedState}
            onChange={e => setSelectedState(e.target.value)}
            className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-orange-500"
          >
            {PILOT_STATES.map(s => (
              <option key={s} value={s}>{s}</option>
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
              title="State"
              value={stateHazards?.state_name || selectedState}
              icon={Building2}
              color="blue"
            />
            <MetricCard
              title="Active Threats"
              value={hazards.length}
              icon={AlertTriangle}
              color="orange"
            />
            <MetricCard
              title="Counties at Risk"
              value={riskyCounties.length}
              subtitle="Orange or higher"
              icon={MapPin}
              color="red"
            />
            <MetricCard
              title="IT Forecast Items"
              value={itForecast?.forecasts?.length || 0}
              icon={Shield}
              color="purple"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">County Risk Table</h3>
              <DataTable
                columns={[
                  { key: 'county_name', label: 'County' },
                  { key: 'hazard_name', label: 'Hazard' },
                  {
                    key: 'readiness_band',
                    label: 'Risk',
                    render: (row: any) => <ReadinessBadge band={row.readiness_band} />,
                  },
                  {
                    key: 'probability_score',
                    label: 'Prob',
                    render: (row: any) => row.probability_score != null ? `${(row.probability_score * 100).toFixed(0)}%` : '-',
                  },
                  {
                    key: 'severity_score',
                    label: 'Severity',
                    render: (row: any) => row.severity_score != null ? `${(row.severity_score * 100).toFixed(0)}%` : '-',
                  },
                  { key: 'confidence_band', label: 'Confidence' },
                ]}
                data={hazards}
                searchKey="county_name"
                emptyMessage="No hazards detected for this state"
              />
            </div>

            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">State Contacts</h3>
              {(pocs || []).length === 0 ? (
                <p className="text-sm text-gray-500">No SEMA contacts loaded</p>
              ) : (
                (pocs || []).map((poc: any) => <PocCard key={poc.id} poc={poc} />)
              )}
            </div>
          </div>

          {itForecast?.forecasts && itForecast.forecasts.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3">IT Equipment Forecast</h3>
              <DataTable
                columns={[
                  { key: 'agency_name', label: 'Agency' },
                  { key: 'item_category', label: 'Item' },
                  { key: 'quantity_needed', label: 'Qty Needed' },
                  { key: 'date_needed', label: 'Date Needed' },
                  { key: 'reason_code', label: 'Reason' },
                  {
                    key: 'confidence_score',
                    label: 'Confidence',
                    render: (row: any) => row.confidence_score != null ? `${(row.confidence_score * 100).toFixed(0)}%` : '-',
                  },
                ]}
                data={itForecast.forecasts}
                searchKey="agency_name"
              />
            </div>
          )}
        </>
      )}
    </div>
  );
}
