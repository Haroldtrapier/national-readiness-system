import {
  PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';

interface AssetAgeData {
  name: string;
  value: number;
  color: string;
}

interface AssetAgeChartProps {
  data: AssetAgeData[];
  title?: string;
}

export default function AssetAgeChart({ data, title = 'Asset Distribution' }: AssetAgeChartProps) {
  return (
    <div className="rounded-xl border border-gray-700/50 bg-gray-800/30 p-4">
      <h3 className="text-sm font-semibold text-gray-400 mb-4">{title}</h3>
      <ResponsiveContainer width="100%" height={200}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={70}
            innerRadius={40}
            paddingAngle={2}
          >
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: 8, fontSize: 12 }}
          />
          <Legend
            wrapperStyle={{ fontSize: 11, color: '#9ca3af' }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
