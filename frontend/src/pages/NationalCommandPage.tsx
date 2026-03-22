import { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { AlertTriangle, MapPin, Package, Monitor, RefreshCw } from 'lucide-react';
import MetricCard from '../components/cards/MetricCard';
import ThreatCard from '../components/cards/ThreatCard';
import NationalHazardMap from '../components/maps/NationalHazardMap';
import HazardTrendChart from '../components/charts/HazardTrendChart';
import { useApi } from '../hooks/useApi';
import { api } from '../services/api';

export default function NationalCommandPage() {
  const navigate = useNavigate();
  const [refreshing, setRefreshing] = useState(false);

  const { data: summary, loading, refetch } = useApi(
    () => api.hazards.getNationalSummary(),
    []
  );

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      await api.hazards.refresh();
      refetch();
    } finally {
      setRefreshing(false);
    }
  };

  const hazardChartData = useMemo(() => {
    if (!summary?.top_hazards) return [];
    const counts: Record<string, number> = {};
    for (const h of summary.top_hazards) {
      counts[h.hazard_name] = (counts[h.hazard_name] || 0) + 1;
    }
    const colors = ['#f97316', '#ef4444', '#eab308', '#22c55e', '#3b82f6', '#8b5cf6', '#ec4899', '#14b8a6'];
    return Object.entries(counts).map(([name, count], i) => ({
      name: name.split('/')[0].trim(),
      count,
      color: colors[i % colors.length],
    }));
  }, [summary]);

  const topHazards = summary?.top_hazards || [];

  const mapHazards = useMemo(() => {
    return topHazards.map((h: any) => ({
      ...h,
      region_number: h.region_number || null,
    }));
  }, [topHazards]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">National Command</h1>
          <p className="text-sm text-gray-400 mt-0.5">
            National hazard, supply, and IT readiness overview
          </p>
        </div>
        <button
          onClick={handleRefresh}
          disabled={refreshing}
          className="flex items-center gap-2 px-4 py-2 bg-orange-500/20 text-orange-400 rounded-lg border border-orange-500/30 hover:bg-orange-500/30 transition-colors text-sm font-medium disabled:opacity-50"
        >
          <RefreshCw size={14} className={refreshing ? 'animate-spin' : ''} />
          {refreshing ? 'Refreshing...' : 'Refresh Feeds'}
        </button>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <MetricCard
              title="Active Hazards"
              value={summary?.active_hazards || 0}
              subtitle="Across all regions"
              icon={AlertTriangle}
              color="orange"
            />
            <MetricCard
              title="Counties at Risk"
              value={summary?.counties_at_risk || 0}
              subtitle="Orange / Red / Black"
              icon={MapPin}
              color="red"
            />
            <MetricCard
              title="Supply Categories"
              value={hazardChartData.length}
              subtitle="Active hazard types"
              icon={Package}
              color="yellow"
            />
            <MetricCard
              title="FEMA Regions"
              value={10}
              subtitle="Monitoring all regions"
              icon={Monitor}
              color="blue"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <NationalHazardMap
                hazards={mapHazards}
                onRegionClick={(num) => navigate(`/regions?region=${num}`)}
              />
            </div>
            <div className="space-y-3">
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">
                Top Emerging Threats
              </h3>
              {topHazards.length === 0 ? (
                <div className="p-4 rounded-xl bg-gray-800/30 border border-gray-700/50 text-center">
                  <p className="text-sm text-gray-500">No active threats detected</p>
                  <p className="text-xs text-gray-600 mt-1">Click "Refresh Feeds" to ingest latest data from NWS and USGS</p>
                </div>
              ) : (
                topHazards.slice(0, 6).map((h: any, i: number) => (
                  <ThreatCard key={i} hazard={h} />
                ))
              )}
            </div>
          </div>

          {hazardChartData.length > 0 && (
            <HazardTrendChart data={hazardChartData} title="Active Hazard Types" />
          )}
        </>
      )}
    </div>
  );
}
