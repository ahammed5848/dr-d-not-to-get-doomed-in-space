import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { WebSocketProvider } from './context/WebSocketContext';
import Navbar from './components/Navbar';
import AlertBanner from './components/AlertBanner';

import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import AstronautDetailPage from './pages/AstronautDetailPage';
import AlertsCenterPage from './pages/AlertsCenterPage';
import EnvironmentPage from './pages/EnvironmentPage';
import MissionTrendsPage from './pages/MissionTrendsPage';
import DailyCheckinPage from './pages/DailyCheckinPage';
import AdminThresholdsPage from './pages/AdminThresholdsPage';
import ReportsPage from './pages/ReportsPage';
import NasaResearchPage from './pages/NasaResearchPage';

function ProtectedLayout() {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen bg-space-950 flex items-center justify-center font-mono text-cyan-400">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-10 h-10 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
          <span className="text-xs tracking-widest uppercase">Connecting to Dr D Telemetry Matrix...</span>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return (
    <WebSocketProvider>
      <div className="min-h-screen bg-space-950 text-slate-100 flex flex-col justify-between selection:bg-cyan-500 selection:text-space-950">
        <div>
          <Navbar />
          <AlertBanner />
          <main className="max-w-7xl mx-auto px-4 lg:px-8 pt-6">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/astronauts/:id" element={<AstronautDetailPage />} />
              <Route path="/alerts" element={<AlertsCenterPage />} />
              <Route path="/environment" element={<EnvironmentPage />} />
              <Route path="/trends" element={<MissionTrendsPage />} />
              <Route path="/checkin" element={<DailyCheckinPage />} />
              <Route path="/admin/thresholds" element={<AdminThresholdsPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/research" element={<NasaResearchPage />} />
              <Route path="*" element={<Navigate to="/dashboard" replace />} />
            </Routes>
          </main>
        </div>

        {/* Global Spaceflight Medical Disclaimer Footer */}
        <footer className="mt-12 border-t border-slate-900 bg-space-950/90 py-4 px-4 text-center font-mono text-[10px] text-slate-500">
          <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
            <div>
              <span className="font-bold text-slate-400">Dr D v1.0.0</span> • Deep Space Exploration Telemetry & Bio-advisory Platform
            </div>
            <div className="text-amber-500/80">
              DISCLAIMER: Dr D is an experimental aerospace prototype for demonstration. Not a certified clinical medical device.
            </div>
          </div>
        </footer>
      </div>
    </WebSocketProvider>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/*" element={<ProtectedLayout />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
