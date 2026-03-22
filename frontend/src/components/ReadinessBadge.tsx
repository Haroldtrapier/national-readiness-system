const bandStyles: Record<string, string> = {
  GREEN: 'bg-green-500/20 text-green-400 border-green-500/30',
  YELLOW: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  ORANGE: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  RED: 'bg-red-500/20 text-red-400 border-red-500/30',
  BLACK: 'bg-gray-700 text-gray-200 border-gray-600',
};

interface ReadinessBadgeProps {
  band: string;
  size?: 'sm' | 'md';
}

export default function ReadinessBadge({ band, size = 'sm' }: ReadinessBadgeProps) {
  const style = bandStyles[band] || bandStyles.GREEN;
  const sizeClass = size === 'sm' ? 'text-[10px] px-1.5 py-0.5' : 'text-xs px-2 py-1';

  return (
    <span className={`inline-flex items-center rounded-md border font-semibold uppercase tracking-wider ${style} ${sizeClass}`}>
      {band}
    </span>
  );
}
