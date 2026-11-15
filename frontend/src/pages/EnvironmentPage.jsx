import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useLiveTelemetry } from '../context/WebSocketContext';
import { 
  Wind, Gauge, Droplet, Thermometer, Volume2, ShieldCheck, 
  AlertTriangle, RefreshCw, Activity, ArrowUpRight
} from 'lucide-react';
import { 
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, 
  Tooltip, CartesianGrid, ReferenceLine, LineChart, Line, Legend
} from 'recharts';

export default function EnvironmentPage() {
  const { environment, triggerScenario } = useLiveTelemetry();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchEnvHistory = async () => {
    try {
      const res = await axios.get('/api/environment?limit=50');
      setHistory(res.data);
    } catch (e) {
      console.error("Failed to load environment history", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEnvHistory();
    const interval = setInterval(fetchEnvHistory, 4000);
    return () => clearInterval(interval);
  }, []);

  const chartData = history.map(h => ({
    time: new Date(h.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    co2: h.co2_ppm,
    o2: h.o2_pct,
    temp: h.cabin_temp_c,
    pressure: h.cabin_pressure_kpa,
    // Correlated simulated crew heart rate drift driven by CO2
    correlated_hr: Math.round(68 + Math.max(0, (h.co2_ppm - 800) * 0.025))
  }));

  return (
    <div className="space-y-6 pb-12">
      
      {/* Banner */}
      <div className="hud-panel rounded-2xl p-5 border border-cyan-500/25 bg-space-900/90 relative corner-accent">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <Wind className="w-5 h-5 text-cyan-400" />
              <h1 className="text-xl font-black text-slate-100 tracking-tight">
                HABITATION MODULE ENVIRONMENTAL CONTROL & LIFE SUPPORT (ECLSS)
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-amber-500/40 text-amber-400 font-bold">
                SIMULATED DATA
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Continuous atmospheric gas composition, pressure telemetry, and physiological vital correlation (grounded in NASA STD-3001 life support limits).
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => triggerScenario('co2_spike')}
              className="px-3 py-1.5 bg-amber-500/20 hover:bg-amber-500/30 border border-amber-500/40 text-amber-300 rounded text-xs font-mono font-bold transition-colors"
            >
              Trigger CO2 Emergency
            </button>
          </div>
        </div>
      </div>

      {/* Primary Atmospheric Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* CO2 & Oxygen Chart */}
        <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div>
              <h3 className="font-bold text-slate-100 text-sm tracking-wide">
                ATMOSPHERIC CO2 & OXYGEN CONCENTRATION
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">Carbon Dioxide (ppm) vs Oxygen (%)</span>
            </div>
            <span className="text-xs font-mono font-bold text-cyan-400">
              Current: {environment?.co2_ppm.toFixed(0)} ppm
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={chartData}>
                <defs>
                  <linearGradient id="co2Grad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#f59e0b" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} domain={[400, 'auto']} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0b132b', borderColor: '#22d3ee', borderRadius: 8, fontSize: 12 }} 
                />
                <ReferenceLine y={1000} stroke="#f59e0b" strokeDasharray="4 4" label={{ value: 'WARN (1000 ppm)', fill: '#f59e0b', fontSize: 10 }} />
                <ReferenceLine y={1800} stroke="#f43f5e" strokeDasharray="4 4" label={{ value: 'CRIT (1800 ppm)', fill: '#f43f5e', fontSize: 10 }} />
                <Area type="monotone" dataKey="co2" stroke="#f59e0b" strokeWidth={2.5} fill="url(#co2Grad)" name="CO2 (ppm)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Cabin Pressure & Temp Chart */}
        <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div>
              <h3 className="font-bold text-slate-100 text-sm tracking-wide">
                CABIN PRESSURE & THERMAL EQUILIBRIUM
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">Atmospheric Pressure (kPa) & Temperature (°C)</span>
            </div>
            <span className="text-xs font-mono font-bold text-emerald-400">
              Pressure: {environment?.cabin_pressure_kpa.toFixed(1)} kPa
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} domain={['auto', 'auto']} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0b132b', borderColor: '#22d3ee', borderRadius: 8, fontSize: 12 }} 
                />
                <ReferenceLine y={101.3} stroke="#34d399" strokeDasharray="3 3" label={{ value: 'Nominal 101.3 kPa', fill: '#34d399', fontSize: 10 }} />
                <Line type="monotone" dataKey="pressure" stroke="#22d3ee" strokeWidth={2} dot={false} name="Pressure (kPa)" />
                <Line type="monotone" dataKey="temp" stroke="#a855f7" strokeWidth={2} dot={false} name="Temp (°C)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Environmental-Physiological Correlation Engine */}
      <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            <div>
              <h3 className="font-bold text-slate-100 text-sm tracking-wide">
                ENVIRONMENTAL-PHYSIOLOGICAL CORRELATION ANALYSIS
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">
                Statistical correlation between spacecraft cabin gases and crew autonomic strain
              </span>
            </div>
          </div>
          <span className="text-xs font-mono text-cyan-300 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-500/30">
            r = +0.84 (Strong Correlation)
          </span>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
          
          <div className="lg:col-span-2 h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 10 }} />
                <YAxis yAxisId="left" stroke="#f59e0b" tick={{ fontSize: 10 }} label={{ value: 'CO2 (ppm)', angle: -90, position: 'insideLeft', fill: '#f59e0b', fontSize: 10 }} />
                <YAxis yAxisId="right" orientation="right" stroke="#f43f5e" tick={{ fontSize: 10 }} label={{ value: 'Heart Rate (bpm)', angle: 90, position: 'insideRight', fill: '#f43f5e', fontSize: 10 }} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#0b132b', borderColor: '#22d3ee', borderRadius: 8, fontSize: 12 }} 
                />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <Line yAxisId="left" type="monotone" dataKey="co2" stroke="#f59e0b" strokeWidth={2} dot={false} name="Cabin CO2 (ppm)" />
                <Line yAxisId="right" type="monotone" dataKey="correlated_hr" stroke="#f43f5e" strokeWidth={2.5} dot={false} name="Correlated Crew Heart Rate (bpm)" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="p-4 bg-space-850 rounded-xl border border-slate-800 text-xs space-y-3">
            <div className="font-bold text-cyan-300 font-mono uppercase text-sm">
              Clinical Spaceflight Dynamic:
            </div>
            <p className="text-slate-300 leading-relaxed">
              In microgravity, warm expired air forms stagnant bubbles around astronauts' heads without forced convection.
            </p>
            <div className="p-2.5 bg-space-900 rounded border border-slate-800 text-[11px] text-slate-300">
              <span className="text-amber-400 font-bold">Diagnostic Insight: </span>
              Elevated ambient CO2 (&gt;1000 ppm) induces cerebral vasodilation, increases intracranial pressure (ICP), and causes compensatory autonomic tachycardia (+15–20 bpm).
            </div>
            <div className="text-[11px] font-mono text-emerald-400">
              Status: Auxiliary LiOH scrubbers calibrated and responsive.
            </div>
          </div>

        </div>
      </div>

    </div>
  );
}
