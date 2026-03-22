import { useMemo } from 'react';
import type { HazardSummary } from '../../types';

interface MapProps {
  hazards: HazardSummary[];
  onRegionClick?: (regionNumber: number) => void;
}

const regionPositions: Record<number, { x: number; y: number; label: string; states: string }> = {
  1: { x: 82, y: 12, label: 'R1', states: 'CT, ME, MA, NH, RI, VT' },
  2: { x: 78, y: 22, label: 'R2', states: 'NJ, NY' },
  3: { x: 72, y: 32, label: 'R3', states: 'DC, DE, MD, PA, VA, WV' },
  4: { x: 68, y: 52, label: 'R4', states: 'AL, FL, GA, KY, MS, NC, SC, TN' },
  5: { x: 55, y: 22, label: 'R5', states: 'IL, IN, MI, MN, OH, WI' },
  6: { x: 42, y: 58, label: 'R6', states: 'AR, LA, NM, OK, TX' },
  7: { x: 45, y: 32, label: 'R7', states: 'IA, KS, MO, NE' },
  8: { x: 30, y: 22, label: 'R8', states: 'CO, MT, ND, SD, UT, WY' },
  9: { x: 10, y: 42, label: 'R9', states: 'AZ, CA, HI, NV' },
  10: { x: 12, y: 12, label: 'R10', states: 'AK, ID, OR, WA' },
};

const bandColor: Record<string, string> = {
  GREEN: '#22c55e',
  YELLOW: '#eab308',
  ORANGE: '#f97316',
  RED: '#ef4444',
  BLACK: '#374151',
};

export default function NationalHazardMap({ hazards, onRegionClick }: MapProps) {
  const regionBands = useMemo(() => {
    const bands: Record<number, string> = {};
    const priority = ['BLACK', 'RED', 'ORANGE', 'YELLOW', 'GREEN'];

    for (let i = 1; i <= 10; i++) bands[i] = 'GREEN';

    for (const h of hazards) {
      if (!h.region_number) continue;
      const current = bands[h.region_number];
      const incoming = h.readiness_band;
      if (priority.indexOf(incoming) < priority.indexOf(current)) {
        bands[h.region_number] = incoming;
      }
    }
    return bands;
  }, [hazards]);

  return (
    <div className="relative w-full h-full min-h-[400px] bg-gray-800/30 rounded-xl border border-gray-700/50 p-4">
      <h3 className="text-sm font-semibold text-gray-400 mb-3">FEMA Region Risk Map</h3>
      <svg viewBox="0 0 100 80" className="w-full h-full max-h-[350px]">
        {Object.entries(regionPositions).map(([num, pos]) => {
          const regionNum = parseInt(num);
          const band = regionBands[regionNum] || 'GREEN';
          const color = bandColor[band];
          return (
            <g
              key={num}
              onClick={() => onRegionClick?.(regionNum)}
              className="cursor-pointer"
            >
              <circle
                cx={pos.x}
                cy={pos.y}
                r={6}
                fill={color}
                opacity={0.3}
                stroke={color}
                strokeWidth={1}
              />
              <circle
                cx={pos.x}
                cy={pos.y}
                r={3.5}
                fill={color}
                opacity={0.8}
              />
              <text
                x={pos.x}
                y={pos.y + 0.8}
                textAnchor="middle"
                fill="white"
                fontSize="2.2"
                fontWeight="bold"
              >
                {pos.label}
              </text>
              <text
                x={pos.x}
                y={pos.y + 10}
                textAnchor="middle"
                fill="#9ca3af"
                fontSize="1.5"
              >
                {pos.states}
              </text>
            </g>
          );
        })}
      </svg>
      <div className="flex items-center gap-3 mt-2">
        {['GREEN', 'YELLOW', 'ORANGE', 'RED', 'BLACK'].map(band => (
          <div key={band} className="flex items-center gap-1">
            <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: bandColor[band] }} />
            <span className="text-[10px] text-gray-500 uppercase">{band}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
