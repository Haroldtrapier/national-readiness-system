interface SupplyGapCardProps {
  itemName: string;
  required: number;
  available: number;
  shortage: number;
  shortagePct: number;
}

export default function SupplyGapCard({ itemName, required, available, shortage, shortagePct }: SupplyGapCardProps) {
  const severityColor =
    shortagePct >= 75 ? 'text-red-400' :
    shortagePct >= 50 ? 'text-orange-400' :
    shortagePct >= 25 ? 'text-yellow-400' : 'text-green-400';

  const barColor =
    shortagePct >= 75 ? 'bg-red-500' :
    shortagePct >= 50 ? 'bg-orange-500' :
    shortagePct >= 25 ? 'bg-yellow-500' : 'bg-green-500';

  return (
    <div className="p-3 rounded-lg bg-gray-800/50 border border-gray-700/50">
      <div className="flex items-center justify-between mb-1.5">
        <span className="text-sm font-medium">{itemName}</span>
        <span className={`text-xs font-bold ${severityColor}`}>{shortagePct.toFixed(0)}% gap</span>
      </div>
      <div className="h-1.5 bg-gray-700 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all ${barColor}`}
          style={{ width: `${Math.min(100 - shortagePct, 100)}%` }}
        />
      </div>
      <div className="flex items-center justify-between mt-1.5 text-xs text-gray-500">
        <span>Need: {required.toLocaleString()}</span>
        <span>Have: {available.toLocaleString()}</span>
        <span>Gap: {shortage.toLocaleString()}</span>
      </div>
    </div>
  );
}
