import React, { useState } from 'react';
import { 
  TrendingUp, Radio, Bone, Activity, Moon, Droplets, 
  ShieldCheck, AlertTriangle, Compass, Calendar
} from 'lucide-react';
import { 
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, 
  Tooltip, CartesianGrid, ReferenceLine, LineChart, Line, Legend
} from 'recharts';

export default function MissionTrendsPage() {
  const [selectedPhase, setSelectedPhase] = useState('all');

  // Simulated Mission Days 1 to 142 (sampled every 10 days) + Projected to Sol 540
  const missionTrendData = [
    { sol: 'Sol 1', radiation: 0.8, bone_loss: 0.1, muscle: 100, fluid_shift: 38, circadian_disruption: 35 },
    { sol: 'Sol 20', radiation: 18.5, bone_loss: 0.4, muscle: 98.8, fluid_shift: 32, circadian_disruption: 28 },
    { sol: 'Sol 40', radiation: 39.2, bone_loss: 0.8, muscle: 97.5, fluid_shift: 25, circadian_disruption: 20 },
    { sol: 'Sol 60', radiation: 61.0, bone_loss: 1.1, muscle: 96.4, fluid_shift: 20, circadian_disruption: 16 },
    { sol: 'Sol 80', radiation: 82.4, bone_loss: 1.4, muscle: 95.8, fluid_shift: 18, circadian_disruption: 15 },
    { sol: 'Sol 100', radiation: 104.1, bone_loss: 1.8, muscle: 95.0, fluid_shift: 17, circadian_disruption: 14 },
    { sol: 'Sol 120', radiation: 125.6, bone_loss: 2.1, muscle: 94.6, fluid_shift: 16, circadian_disruption: 13 },
    { sol: 'Sol 142 (Today)', radiation: 142.5, bone_loss: 2.4, muscle: 94.2, fluid_shift: 16, circadian_disruption: 12 },
    // Projected
    { sol: 'Sol 200 (Proj)', radiation: 205.0, bone_loss: 3.2, muscle: 93.1, fluid_shift: 15, circadian_disruption: 15 },
    { sol: 'Sol 300 (Proj)', radiation: 310.0, bone_loss: 4.4, muscle: 91.5, fluid_shift: 15, circadian_disruption: 18 },
    { sol: 'Sol 400 (Proj)', radiation: 415.0, bone_loss: 5.5, muscle: 90.2, fluid_shift: 14, circadian_disruption: 20 },
    { sol: 'Sol 540 (Return)', radiation: 550.0, bone_loss: 6.8, muscle: 88.5, fluid_shift: 28, circadian_disruption: 30 },
  ];

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="hud-panel rounded-2xl p-5 border border-cyan-500/25 bg-space-900/90 relative corner-accent">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <TrendingUp className="w-5 h-5 text-cyan-400" />
              <h1 className="text-xl font-black text-slate-100 tracking-tight">
                LONG-DURATION SPACEFLIGHT PHYSIOLOGICAL TRENDS
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-amber-500/40 text-amber-400 font-bold">
                SIMULATED DATA
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-purple-500/40 text-purple-300 font-bold">
                MODEL-GENERATED PROJECTION
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Multi-sol longitudinal adaptation tracking: musculoskeletal remodeling, cumulative cosmic radiation (600 mSv PEL cap), and fluid redistribution based on NASA HRP evidence reports.
            </p>
          </div>

          <div className="flex items-center space-x-2 text-xs font-mono">
            <span className="px-3 py-1 bg-cyan-950 border border-cyan-500/30 text-cyan-400 rounded">
              Current Mission Sol: 142
            </span>
            <span className="px-3 py-1 bg-space-850 border border-slate-700 text-slate-300 rounded">
              Total Transit Target: 540 Sols
            </span>
          </div>
        </div>
      </div>

      {/* Primary Longitudinal Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Bone Density & Muscle Mass Retention */}
        <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div>
              <h3 className="font-bold text-slate-100 text-sm tracking-wide flex items-center space-x-2">
                <Bone className="w-4 h-4 text-amber-400" />
                <span>BONE DENSITY LOSS & MUSCLE RETENTION</span>
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">ARED Resistive Exercise Adherence Outcome</span>
            </div>
            <span className="text-xs font-mono font-bold text-amber-400">
              Loss: -2.4% (Nominal Target &lt; 3.5%)
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={missionTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="sol" stroke="#64748b" tick={{ fontSize: 9 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                <Tooltip contentStyle={{ backgroundColor: '#0b132b', borderColor: '#22d3ee', borderRadius: 8, fontSize: 12 }} />
                <Legend wrapperStyle={{ fontSize: 11 }} />
                <ReferenceLine x="Sol 142 (Today)" stroke="#22d3ee" strokeDasharray="3 3" label={{ value: 'CURRENT SOL', fill: '#22d3ee', fontSize: 9 }} />
                <Line type="monotone" dataKey="bone_loss" stroke="#f59e0b" strokeWidth={2.5} name="Bone Loss (%)" />
                <Line type="monotone" dataKey="muscle" stroke="#34d399" strokeWidth={2.5} name="Muscle Mass Index (%)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Radiation Exposure vs Career/Mission Limit */}
        <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
            <div>
              <h3 className="font-bold text-slate-100 text-sm tracking-wide flex items-center space-x-2">
                <Radio className="w-4 h-4 text-purple-400" />
                <span>CUMULATIVE IONIZING RADIATION (mSv)</span>
              </h3>
              <span className="text-[10px] text-slate-400 font-mono">Galactic Cosmic Rays (GCR) + Solar Protons</span>
            </div>
            <span className="text-xs font-mono font-bold text-purple-400">
              142.5 mSv (Safe Limit 600 mSv)
            </span>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={missionTrendData}>
                <defs>
                  <linearGradient id="radGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#a855f7" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#a855f7" stopOpacity={0.0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="sol" stroke="#64748b" tick={{ fontSize: 9 }} />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} domain={[0, 650]} />
                <Tooltip contentStyle={{ backgroundColor: '#0b132b', borderColor: '#22d3ee', borderRadius: 8, fontSize: 12 }} />
                <ReferenceLine y={600} stroke="#f43f5e" strokeDasharray="4 4" label={{ value: 'MISSION CEILING (600 mSv)', fill: '#f43f5e', fontSize: 10 }} />
                <ReferenceLine x="Sol 142 (Today)" stroke="#22d3ee" strokeDasharray="3 3" />
                <Area type="monotone" dataKey="radiation" stroke="#a855f7" strokeWidth={2.5} fill="url(#radGrad)" name="Dose (mSv)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

      </div>

      {/* Fluid Shift & Circadian Trends */}
      <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
          <div>
            <h3 className="font-bold text-slate-100 text-sm tracking-wide flex items-center space-x-2">
              <Droplets className="w-4 h-4 text-cyan-400" />
              <span>CEPHALAD FLUID SHIFT & CIRCADIAN RHYTHM DISRUPTION SCORE</span>
            </h3>
            <span className="text-[10px] text-slate-400 font-mono">
              Initial acute adaptation vs long-duration stabilization
            </span>
          </div>
          <span className="text-xs font-mono text-emerald-400">
            Stabilized in Mars Transit
          </span>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={missionTrendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="sol" stroke="#64748b" tick={{ fontSize: 9 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 10 }} domain={[0, 50]} />
              <Tooltip contentStyle={{ backgroundColor: '#0b132b', borderColor: '#22d3ee', borderRadius: 8, fontSize: 12 }} />
              <Legend wrapperStyle={{ fontSize: 11 }} />
              <ReferenceLine x="Sol 142 (Today)" stroke="#22d3ee" strokeDasharray="3 3" />
              <Line type="monotone" dataKey="fluid_shift" stroke="#22d3ee" strokeWidth={2.5} name="Fluid Shift / ICP Risk Score" />
              <Line type="monotone" dataKey="circadian_disruption" stroke="#eab308" strokeWidth={2} strokeDasharray="3 3" name="Circadian Disruption Index" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
}
