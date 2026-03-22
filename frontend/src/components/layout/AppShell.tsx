import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Shield, Map, Building2, MapPin, Monitor, Truck, Users, FileText,
  Menu, X, AlertTriangle, Activity
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'National Command', icon: Shield },
  { path: '/regions', label: 'FEMA Regions', icon: Map },
  { path: '/states', label: 'State Operations', icon: Building2 },
  { path: '/counties', label: 'County Operations', icon: MapPin },
  { path: '/agency-it', label: 'Agency IT Command', icon: Monitor },
  { path: '/vendors', label: 'Vendor Operations', icon: Truck },
  { path: '/pocs', label: 'POC Command Center', icon: Users },
  { path: '/briefs', label: 'Operational Briefs', icon: FileText },
];

export default function AppShell({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Top bar */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-gray-900/95 backdrop-blur border-b border-gray-800 h-14">
        <div className="flex items-center h-full px-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="lg:hidden mr-3 p-1.5 rounded-lg hover:bg-gray-800 transition-colors"
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <div className="flex items-center gap-2">
            <AlertTriangle className="text-orange-500" size={22} />
            <h1 className="text-base font-bold tracking-tight">
              National Readiness System
            </h1>
          </div>
          <div className="ml-auto flex items-center gap-3">
            <div className="flex items-center gap-1.5 text-xs text-gray-400">
              <Activity size={14} className="text-green-500" />
              <span>System Operational</span>
            </div>
          </div>
        </div>
      </header>

      {/* Sidebar */}
      <aside className={`
        fixed top-14 bottom-0 left-0 z-40 w-60 bg-gray-900 border-r border-gray-800
        transition-transform duration-200
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0
      `}>
        <nav className="p-3 space-y-1">
          {navItems.map(item => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                onClick={() => setSidebarOpen(false)}
                className={`
                  flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors
                  ${isActive
                    ? 'bg-orange-500/15 text-orange-400'
                    : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'}
                `}
              >
                <Icon size={18} />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Main content */}
      <main className="lg:ml-60 pt-14 min-h-screen">
        <div className="p-6">
          {children}
        </div>
      </main>

      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
