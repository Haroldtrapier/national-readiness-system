import { useState } from 'react';
import { FileText, AlertTriangle, Package, Users, Shield } from 'lucide-react';
import ReadinessBadge from '../components/ReadinessBadge';
import SupplyGapCard from '../components/cards/SupplyGapCard';
import { useApi } from '../hooks/useApi';
import { api } from '../services/api';

export default function BriefsPage() {
  const [briefType, setBriefType] = useState<'national' | 'region'>('national');
  const [selectedRegion, setSelectedRegion] = useState(4);

  const { data: brief, loading } = useApi(
    () => briefType === 'national'
      ? api.briefs.getNational()
      : api.briefs.getRegion(selectedRegion),
    [briefType, selectedRegion]
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div>
          <h1 className="text-2xl font-bold">Operational Briefs</h1>
          <p className="text-sm text-gray-400 mt-0.5">
            Generated operational intelligence and action packages
          </p>
        </div>
        <div className="flex items-center gap-3">
          <select
            value={briefType}
            onChange={e => setBriefType(e.target.value as any)}
            className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-orange-500"
          >
            <option value="national">National Brief</option>
            <option value="region">Region Brief</option>
          </select>
          {briefType === 'region' && (
            <select
              value={selectedRegion}
              onChange={e => setSelectedRegion(parseInt(e.target.value))}
              className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-200 focus:outline-none focus:border-orange-500"
            >
              {Array.from({ length: 10 }, (_, i) => i + 1).map(n => (
                <option key={n} value={n}>Region {n}</option>
              ))}
            </select>
          )}
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center py-20">
          <div className="w-8 h-8 border-2 border-orange-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : brief ? (
        <>
          {/* Brief Header */}
          <div className="rounded-xl border border-gray-700/50 bg-gray-800/30 p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <FileText size={24} className="text-orange-400" />
                <div>
                  <h2 className="text-lg font-bold">{brief.title}</h2>
                  <p className="text-xs text-gray-500">
                    Generated: {new Date(brief.generated_at).toLocaleString()}
                  </p>
                </div>
              </div>
              <ReadinessBadge band={brief.readiness_band} size="md" />
            </div>
            <p className="text-sm text-gray-400">Scope: {brief.scope}</p>
          </div>

          {/* Threats */}
          {brief.threats && brief.threats.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                <AlertTriangle size={14} /> Identified Threats
              </h3>
              <div className="space-y-2">
                {brief.threats.map((t: any, i: number) => (
                  <div key={i} className="p-3 rounded-lg bg-gray-800/50 border border-gray-700/50">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium">{t.hazard_type}</span>
                      <ReadinessBadge band={t.risk_level} />
                    </div>
                    <p className="text-xs text-gray-400 mt-1">{t.area}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{t.narrative}</p>
                    <p className="text-xs text-gray-600 mt-0.5">Confidence: {t.confidence}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Supply Needs */}
          {brief.supply_needs && brief.supply_needs.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                <Package size={14} /> Supply Requirements
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {brief.supply_needs.map((s: any, i: number) => (
                  <SupplyGapCard
                    key={i}
                    itemName={s.item_name}
                    required={s.required}
                    available={s.available}
                    shortage={s.shortage}
                    shortagePct={s.shortage_pct}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Recommended Vendors */}
          {brief.recommended_vendors && brief.recommended_vendors.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                <Shield size={14} /> Recommended Vendors
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {brief.recommended_vendors.map((v: any, i: number) => (
                  <div key={i} className="p-3 rounded-lg bg-gray-800/50 border border-gray-700/50">
                    <p className="text-sm font-medium">{v.vendor_name}</p>
                    <p className="text-xs text-gray-400">{v.capability}</p>
                    <div className="flex items-center gap-3 mt-1.5 text-xs text-gray-500">
                      {v.sla_hours && <span>SLA: {v.sla_hours}h</span>}
                      <span className={v.contract_ready ? 'text-green-400' : 'text-red-400'}>
                        {v.contract_ready ? 'Contract Ready' : 'Open Market'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Key Contacts */}
          {brief.key_contacts && brief.key_contacts.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-3 flex items-center gap-2">
                <Users size={14} /> Key Contacts
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {brief.key_contacts.map((c: any, i: number) => (
                  <div key={i} className="p-3 rounded-lg bg-gray-800/50 border border-gray-700/50">
                    <p className="text-sm font-medium">{c.name}</p>
                    <p className="text-xs text-gray-400">{c.role}</p>
                    <div className="flex items-center gap-3 mt-1.5 text-xs text-gray-500">
                      {c.phone && <span>{c.phone}</span>}
                      {c.email && <span>{c.email}</span>}
                      {c.availability && <span>{c.availability}</span>}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recommended Actions */}
          {brief.recommended_actions && brief.recommended_actions.length > 0 && (
            <div className="rounded-xl border border-orange-500/20 bg-orange-500/5 p-4">
              <h3 className="text-sm font-semibold text-orange-400 uppercase tracking-wider mb-3">
                Recommended Actions
              </h3>
              <ul className="space-y-2">
                {brief.recommended_actions.map((action: string, i: number) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                    <span className="text-orange-400 mt-0.5 font-bold">{i + 1}.</span>
                    {action}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      ) : (
        <div className="p-8 text-center text-gray-500">
          No brief data available. Refresh hazard feeds first.
        </div>
      )}
    </div>
  );
}
