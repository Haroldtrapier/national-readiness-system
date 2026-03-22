import { useState, useMemo } from 'react';
import { ChevronUp, ChevronDown, Search } from 'lucide-react';

interface Column<T> {
  key: string;
  label: string;
  render?: (row: T) => React.ReactNode;
  sortable?: boolean;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  searchKey?: string;
  emptyMessage?: string;
}

export default function DataTable<T extends Record<string, any>>({
  columns,
  data,
  searchKey,
  emptyMessage = 'No data available',
}: DataTableProps<T>) {
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc');

  const filtered = useMemo(() => {
    if (!search || !searchKey) return data;
    const q = search.toLowerCase();
    return data.filter(row => {
      const val = row[searchKey];
      return val && String(val).toLowerCase().includes(q);
    });
  }, [data, search, searchKey]);

  const sorted = useMemo(() => {
    if (!sortKey) return filtered;
    return [...filtered].sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      if (aVal == null) return 1;
      if (bVal == null) return -1;
      const cmp = aVal < bVal ? -1 : aVal > bVal ? 1 : 0;
      return sortDir === 'asc' ? cmp : -cmp;
    });
  }, [filtered, sortKey, sortDir]);

  const handleSort = (key: string) => {
    if (sortKey === key) {
      setSortDir(d => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  };

  return (
    <div>
      {searchKey && (
        <div className="relative mb-3">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input
            type="text"
            placeholder="Search..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full pl-9 pr-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-200 placeholder:text-gray-500 focus:outline-none focus:border-gray-600"
          />
        </div>
      )}
      <div className="overflow-x-auto rounded-lg border border-gray-800">
        <table className="w-full text-sm">
          <thead>
            <tr className="bg-gray-800/50">
              {columns.map(col => (
                <th
                  key={col.key}
                  className={`px-3 py-2.5 text-left text-xs font-semibold uppercase tracking-wider text-gray-400 ${
                    col.sortable !== false ? 'cursor-pointer hover:text-gray-200 select-none' : ''
                  }`}
                  onClick={() => col.sortable !== false && handleSort(col.key)}
                >
                  <span className="flex items-center gap-1">
                    {col.label}
                    {sortKey === col.key && (
                      sortDir === 'asc' ? <ChevronUp size={12} /> : <ChevronDown size={12} />
                    )}
                  </span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {sorted.length === 0 ? (
              <tr>
                <td colSpan={columns.length} className="px-3 py-8 text-center text-gray-500">
                  {emptyMessage}
                </td>
              </tr>
            ) : (
              sorted.map((row, i) => (
                <tr key={i} className="hover:bg-gray-800/30 transition-colors">
                  {columns.map(col => (
                    <td key={col.key} className="px-3 py-2.5 text-gray-300">
                      {col.render ? col.render(row) : row[col.key]}
                    </td>
                  ))}
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
