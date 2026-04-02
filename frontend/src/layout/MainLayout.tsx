import { ReactNode } from 'react'
import { AlertTriangle } from 'lucide-react'

export function MainLayout({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen bg-gray-50">
      <div className="w-64 bg-slate-900 text-white shadow-lg p-6">
        <div className="flex items-center gap-3 mb-8">
          <AlertTriangle className="w-8 h-8 text-red-500" />
          <div>
            <h1 className="text-xl font-bold">National Readiness</h1>
            <p className="text-xs text-slate-400">System</p>
          </div>
        </div>
      </div>
      <div className="flex-1 overflow-auto">
        <div className="bg-white border-b p-6">
          <h2 className="text-2xl font-bold">National Readiness System</h2>
        </div>
        <div className="p-6">{children}</div>
      </div>
    </div>
  )
}
