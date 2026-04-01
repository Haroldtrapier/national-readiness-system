import type { HazardSummary } from '../../types';
import ReadinessBadge from '../ReadinessBadge';

interface ThreatCardProps {
  hazard: HazardSummary;
}

export default function ThreatCard({ hazard }: ThreatCardProps) {
  return (
    <div className="flex items-start gap-3 p-3 rounded-lg bg-gray-800/50 border border-gray-700/50 hover:border-gray-600/50 transition-colors">
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-medium text-sm truncate">{hazard.hazard_name}</span>
          <ReadinessBadge band={hazard.readiness_band} />
        </div>
        <p className="text-xs text-gray-400 mt-1">
          {hazard.county_name && `${hazard.county_name} County, `}
          {hazard.state_code}
        </p>
        <div className="flex items-center gap-3 mt-1.5 text-xs text-gray-500">
          {hazard.probability_score != null && (
            <span>Prob: {(hazard.probability_score * 100).toFixed(0)}%</span>
          )}
          {hazard.severity_score != null && (
            <span>Sev: {(hazard.severity_score * 100).toFixed(0)}%</span>
          )}
          {hazard.confidence_band && (
            <span>Conf: {hazard.confidence_band}</span>
          )}
        </div>
      </div>
    </div>
  );
}
