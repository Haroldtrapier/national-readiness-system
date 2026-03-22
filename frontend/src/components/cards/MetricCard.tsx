import type { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: number | string;
  subtitle?: string;
  icon: LucideIcon;
  color?: 'green' | 'yellow' | 'orange' | 'red' | 'blue' | 'purple' | 'gray';
}

const colorMap = {
  green: 'text-green-400 bg-green-500/10 border-green-500/20',
  yellow: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20',
  orange: 'text-orange-400 bg-orange-500/10 border-orange-500/20',
  red: 'text-red-400 bg-red-500/10 border-red-500/20',
  blue: 'text-blue-400 bg-blue-500/10 border-blue-500/20',
  purple: 'text-purple-400 bg-purple-500/10 border-purple-500/20',
  gray: 'text-gray-400 bg-gray-500/10 border-gray-500/20',
};

const iconColorMap = {
  green: 'text-green-400',
  yellow: 'text-yellow-400',
  orange: 'text-orange-400',
  red: 'text-red-400',
  blue: 'text-blue-400',
  purple: 'text-purple-400',
  gray: 'text-gray-400',
};

export default function MetricCard({ title, value, subtitle, icon: Icon, color = 'blue' }: MetricCardProps) {
  return (
    <div className={`rounded-xl border p-4 ${colorMap[color]}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium text-gray-400 uppercase tracking-wide">{title}</p>
          <p className="text-2xl font-bold mt-1">{value}</p>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <Icon size={20} className={iconColorMap[color]} />
      </div>
    </div>
  );
}
