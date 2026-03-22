import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell,
} from 'recharts';

interface HazardChartData {
  name: string;
  count: number;
  color: string;
}

interface HazardTrendChartProps {
  data: HazardChartData[];
  title?: string;
}

export default function HazardTrendChart({ data, title = 'Hazard Distribution' }: HazardTrendChartProps) {
  return (
    <div className="rounded-xl border border-gray-700/50 bg-gray-800/30 p-4">
      <h3 className="text-sm font-semibold text-gray-400 mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis dataKey="name" tick={{ fill: '#9ca3af', fontSize: 11 }} />
          <YAxis tick={{ fill: '#9ca3af', fontSize: 11 }} />
          <Tooltip
            contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: 8, fontSize: 12 }}
            labelStyle={{ color: '#e5e7eb' }}
          />
          <Bar dataKey="count" radius={[4, 4, 0, 0]}>
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
