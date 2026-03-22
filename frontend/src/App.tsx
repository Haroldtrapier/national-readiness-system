import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppShell from './components/layout/AppShell';
import NationalCommandPage from './pages/NationalCommandPage';
import RegionOperationsPage from './pages/RegionOperationsPage';
import StateOperationsPage from './pages/StateOperationsPage';
import CountyOperationsPage from './pages/CountyOperationsPage';
import AgencyItPage from './pages/AgencyItPage';
import VendorOperationsPage from './pages/VendorOperationsPage';
import PocCommandPage from './pages/PocCommandPage';
import BriefsPage from './pages/BriefsPage';

export default function App() {
  return (
    <BrowserRouter>
      <AppShell>
        <Routes>
          <Route path="/" element={<NationalCommandPage />} />
          <Route path="/regions" element={<RegionOperationsPage />} />
          <Route path="/states" element={<StateOperationsPage />} />
          <Route path="/counties" element={<CountyOperationsPage />} />
          <Route path="/agency-it" element={<AgencyItPage />} />
          <Route path="/vendors" element={<VendorOperationsPage />} />
          <Route path="/pocs" element={<PocCommandPage />} />
          <Route path="/briefs" element={<BriefsPage />} />
        </Routes>
      </AppShell>
    </BrowserRouter>
  );
}
