import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useLiveTelemetry } from '../context/WebSocketContext';
import CrewCard from '../components/CrewCard';
import EnvironmentWidget from '../components/EnvironmentWidget';
import { 
  Activity, Radio, AlertTriangle, Shield, Clock, 
  Compass, Zap, RefreshCw, Flame, HeartPulse
} from 'lucide-react';

export default function DashboardPage() {
  const { user, isAstronaut } = useAuth();
  const { crewTelemetry, environment, activeScenarios, triggerScenario } = useLiveTelemetry();
  const [astronauts, setAstronauts] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    try {
      const [astroRes, alertRes] = await Promise.all([
        axios.get('/api/astronauts'),
        axios.get('/api/alerts?limit=5')
      ]);
      setAstronauts(astroRes.data);
      setAlerts(alertRes.data);
    } catch (e) {
      console.error("Dashboard data load error", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 4000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6 pb-12">
      
      {/* Mission Banner */}
      <div className="hud-panel rounded-2xl p-5 border border-cyan-500/25 bg-space-900/80 relative corner-accent">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping" />
              <span className="text-xs font-mono font-bold tracking-widest text-cyan-400 uppercase">
                DR D DEEP SPACE HEALTH TELEMETRY MATRIX
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-amber-500/40 text-amber-400 font-bold">
                SIMULATED DATA
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-cyan-500/40 text-cyan-300 font-semibold">
                NASA HRP EVIDENCE LAYER
              </span>
            </div>
            <h1 className="text-2xl font-black text-slate-100 tracking-tight flex items-center space-x-3">
              <span>MISSION ARES-V: MARS TRANSIT PHASE II</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-xl">
              Real-time physiological telemetry ingestion, rolling baseline z-score anomaly detection, and ground flight surgeon telemetry link.
            </p>
          </div>

          {/* Mission Telemetry Stats */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs font-mono">
            <div className="bg-space-850 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase">Mission Sol</span>
              <span className="text-lg font-black text-cyan-400">DAY 142</span>
              <span className="text-[10px] text-slate-400 block">/ 540 Sols</span>
            </div>

            <div className="bg-space-850 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase">Earth Distance</span>
              <span className="text-base font-bold text-slate-200">78.45M</span>
              <span className="text-[10px] text-slate-400 block">Kilometers</span>
            </div>

            <div className="bg-space-850 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase">Comm Delay</span>
              <span className="text-base font-bold text-amber-400">4.20 s</span>
              <span className="text-[10px] text-slate-400 block">One-way Speed</span>
            </div>

            <div className="bg-space-850 p-2.5 rounded-lg border border-slate-800">
              <span className="text-slate-500 block text-[10px] uppercase">EVA Protocol</span>
              <span className="text-base font-bold text-emerald-400">STANDBY</span>
              <span className="text-[10px] text-slate-400 block">Suit Pressure OK</span>
            </div>
          </div>

        </div>

        {/* Quick Scenario Inject Bar */}
        <div className="mt-4 pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
            <Zap className="w-4 h-4 text-amber-400" />
            <span className="font-semibold text-slate-300">Quick Crisis Scenarios:</span>
          </div>

          <div className="flex flex-wrap items-center gap-1.5 text-xs font-mono">
            <button
              onClick={() => triggerScenario('co2_spike')}
              className="px-2.5 py-1 bg-amber-500/10 hover:bg-amber-500/25 text-amber-300 border border-amber-500/30 rounded transition-colors"
            >
              ⚠️ CO2 Spike
            </button>
            <button
              onClick={() => triggerScenario('eva_cardiac_stress', 3)}
              className="px-2.5 py-1 bg-rose-500/10 hover:bg-rose-500/25 text-rose-300 border border-rose-500/30 rounded transition-colors"
            >
              🫀 EVA Tachycardia
            </button>
            <button
              onClick={() => triggerScenario('radiation_storm')}
              className="px-2.5 py-1 bg-purple-500/10 hover:bg-purple-500/25 text-purple-300 border border-purple-500/30 rounded transition-colors"
            >
              ☢️ Solar Storm
            </button>
            <button
              onClick={() => triggerScenario('sleep_deprivation', 1)}
              className="px-2.5 py-1 bg-indigo-500/10 hover:bg-indigo-500/25 text-indigo-300 border border-indigo-500/30 rounded transition-colors"
            >
              😴 Sleep Deficit
            </button>
          </div>
        </div>
      </div>

      {/* Crew Health Roster Grid */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            <h2 className="text-base font-bold text-slate-100 tracking-wide uppercase">
              {isAstronaut ? 'PERSONAL BIOMETRIC CHANNELS' : 'CREW HEALTH ROSTER (4 ASTRONAUTS)'}
            </h2>
          </div>
          <span className="text-xs font-mono text-slate-400">
            Updated via high-rate telemetry websocket
          </span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 font-mono">Loading crew vitals telemetry...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {astronauts.map(astro => (
              <CrewCard
                key={astro.id}
                astronaut={astro}
                liveData={crewTelemetry[astro.id]}
              />
            ))}
          </div>
        )}
      </div>

      {/* Cabin Environment Panel */}
      <EnvironmentWidget environment={environment} />

      {/* Recent Alerts Feed Ticker */}
      <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <h3 className="font-bold text-slate-100 text-sm">MISSION INCIDENT & ALERT FEED</h3>
          </div>
          <span className="text-xs font-mono text-slate-400">
            {alerts.filter(a => a.status === 'ACTIVE').length} Active Alerts
          </span>
        </div>

        <div className="divide-y divide-slate-800/80">
          {alerts.length === 0 ? (
            <div className="py-4 text-center text-xs text-slate-500 font-mono">No incidents logged. All systems nominal.</div>
          ) : (
            alerts.map((al, idx) => (
              <div key={idx} className="py-2.5 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                <div className="flex items-center space-x-3">
                  <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded border uppercase ${
                    al.threshold_level === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' : 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                  }`}>
                    {al.threshold_level}
                  </span>
                  <div>
                    <span className="font-semibold text-slate-200">
                      {al.astronaut_callsign ? `[${al.astronaut_callsign}]` : '[CABIN]'} {al.message}
                    </span>
                    <span className="block text-[11px] text-slate-400">
                      Protocol: {al.suggested_action}
                    </span>
                  </div>
                </div>

                <div className="flex items-center space-x-3 shrink-0">
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                    al.status === 'ACTIVE' ? 'bg-rose-950 text-rose-400 border border-rose-800' : 'bg-slate-800 text-slate-300'
                  }`}>
                    {al.status}
                  </span>
                  <span className="text-[11px] font-mono text-slate-500">
                    {new Date(al.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

    </div>
  );
}
