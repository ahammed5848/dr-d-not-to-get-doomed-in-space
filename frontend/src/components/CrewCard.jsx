import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, Activity, Thermometer, Wind, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function CrewCard({ astronaut, liveData }) {
  const navigate = useNavigate();

  // Prefer live telemetry if available, else static
  const vitals = liveData?.vitals || astronaut.latest_vitals || {
    heart_rate: astronaut.baseline_hr || 70,
    spo2: astronaut.baseline_spo2 || 98.5,
    core_temp: astronaut.baseline_temp || 36.8,
    stress_index: 22,
    activity_level: 'REST'
  };

  const riskScore = liveData?.risk?.composite_risk_score ?? astronaut.current_risk_score ?? 15.0;
  const status = liveData?.status || astronaut.status || 'NOMINAL';
  const alertsCount = astronaut.active_alerts_count || (status !== 'NOMINAL' ? 1 : 0);

  // Status styles
  const isCritical = status === 'CRITICAL' || riskScore >= 70;
  const isWarning = (status === 'WARNING' || riskScore >= 35) && !isCritical;

  let borderColor = 'border-cyan-500/20 hover:border-cyan-400/50';
  let glowStyle = 'shadow-glow-cyan';
  let badgeColor = 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30';
  let riskColor = 'text-cyan-400';

  if (isCritical) {
    borderColor = 'border-rose-500/60 hover:border-rose-400';
    glowStyle = 'shadow-glow-rose animate-pulse-slow';
    badgeColor = 'bg-rose-500/20 text-rose-300 border-rose-500/40';
    riskColor = 'text-rose-400';
  } else if (isWarning) {
    borderColor = 'border-amber-500/40 hover:border-amber-400';
    glowStyle = 'shadow-glow-amber';
    badgeColor = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
    riskColor = 'text-amber-400';
  }

  return (
    <div 
      onClick={() => navigate(`/astronauts/${astronaut.id}`)}
      className={`hud-panel rounded-xl p-4 cursor-pointer transition-all duration-300 hover:scale-[1.01] border ${borderColor} ${glowStyle} flex flex-col justify-between`}
    >
      <div>
        {/* Top Header: Avatar, Name, Callsign, Status */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            <div className="relative">
              <img 
                src={astronaut.avatar_url || "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=100"} 
                alt={astronaut.name}
                className="w-12 h-12 rounded-lg object-cover border border-slate-700" 
              />
              <span className={`absolute -bottom-1 -right-1 w-3.5 h-3.5 rounded-full border-2 border-space-900 ${
                isCritical ? 'bg-rose-500 animate-ping' : isWarning ? 'bg-amber-400' : 'bg-emerald-400'
              }`} />
            </div>

            <div>
              <div className="flex items-center space-x-2">
                <span className="font-bold text-slate-100 text-sm">{astronaut.name}</span>
                <span className="text-[11px] font-mono text-cyan-400 font-semibold bg-cyan-950/80 px-1.5 py-0.5 rounded border border-cyan-500/30">
                  "{astronaut.callsign}"
                </span>
              </div>
              <div className="text-xs text-slate-400">{astronaut.role_title}</div>
            </div>
          </div>

          {/* Status Badge */}
          <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border uppercase ${badgeColor}`}>
            {status}
          </span>
        </div>

        {/* Health Risk Gauge & Mini Sparkline Row */}
        <div className="flex items-center justify-between p-2.5 bg-space-850/80 rounded-lg border border-slate-800 my-2">
          <div className="flex items-center space-x-2.5">
            <div className="text-center">
              <div className="text-[10px] font-mono text-slate-400 uppercase">Risk Index</div>
              <div className={`text-xl font-black font-mono tracking-tight ${riskColor}`}>
                {riskScore.toFixed(0)}<span className="text-xs font-normal text-slate-500">/100</span>
              </div>
            </div>
            
            {/* Risk bar */}
            <div className="w-16 bg-slate-800 rounded-full h-1.5 overflow-hidden">
              <div 
                className={`h-full rounded-full ${isCritical ? 'bg-rose-500' : isWarning ? 'bg-amber-400' : 'bg-cyan-400'}`}
                style={{ width: `${Math.min(100, Math.max(5, riskScore))}%` }}
              />
            </div>
          </div>

          {/* Mini Pulse Sparkline */}
          <div className="flex flex-col items-end">
            <span className="text-[9px] font-mono text-slate-400 uppercase">Pulse Trace</span>
            <svg className="w-20 h-6 overflow-visible" viewBox="0 0 100 30">
              <path
                d="M 0 15 L 20 15 L 25 5 L 30 25 L 35 15 L 45 15 L 50 2 L 55 28 L 60 15 L 80 15 L 85 8 L 90 20 L 100 15"
                fill="none"
                stroke={isCritical ? '#f43f5e' : isWarning ? '#f59e0b' : '#22d3ee'}
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </div>

        {/* Vitals Quick Grid */}
        <div className="grid grid-cols-4 gap-1.5 text-center mt-3">
          <div className="bg-space-900/90 p-2 rounded border border-slate-800/80">
            <div className="flex items-center justify-center text-rose-400 mb-0.5">
              <Heart className="w-3 h-3 mr-0.5" />
              <span className="text-[9px] font-mono uppercase text-slate-400">HR</span>
            </div>
            <div className="text-xs font-bold font-mono text-slate-100">
              {vitals.heart_rate?.toFixed(0)} <span className="text-[8px] text-slate-500">bpm</span>
            </div>
          </div>

          <div className="bg-space-900/90 p-2 rounded border border-slate-800/80">
            <div className="flex items-center justify-center text-cyan-400 mb-0.5">
              <Activity className="w-3 h-3 mr-0.5" />
              <span className="text-[9px] font-mono uppercase text-slate-400">SpO2</span>
            </div>
            <div className="text-xs font-bold font-mono text-slate-100">
              {vitals.spo2?.toFixed(1)}<span className="text-[8px] text-slate-500">%</span>
            </div>
          </div>

          <div className="bg-space-900/90 p-2 rounded border border-slate-800/80">
            <div className="flex items-center justify-center text-amber-400 mb-0.5">
              <Thermometer className="w-3 h-3 mr-0.5" />
              <span className="text-[9px] font-mono uppercase text-slate-400">Temp</span>
            </div>
            <div className="text-xs font-bold font-mono text-slate-100">
              {vitals.core_temp?.toFixed(1)}<span className="text-[8px] text-slate-500">°C</span>
            </div>
          </div>

          <div className="bg-space-900/90 p-2 rounded border border-slate-800/80">
            <div className="flex items-center justify-center text-indigo-400 mb-0.5">
              <Wind className="w-3 h-3 mr-0.5" />
              <span className="text-[9px] font-mono uppercase text-slate-400">Stress</span>
            </div>
            <div className="text-xs font-bold font-mono text-slate-100">
              {vitals.stress_index?.toFixed(0)}<span className="text-[8px] text-slate-500">/100</span>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Info: Radiation & Alerts */}
      <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono">
        <div className="text-slate-400">
          Dose: <span className="text-cyan-300 font-bold">{astronaut.radiation_msv?.toFixed(1)} mSv</span>
        </div>
        {alertsCount > 0 ? (
          <span className="flex items-center text-rose-400 font-semibold space-x-1">
            <AlertTriangle className="w-3 h-3" />
            <span>{alertsCount} Alert{alertsCount > 1 ? 's' : ''}</span>
          </span>
        ) : (
          <span className="flex items-center text-emerald-400 space-x-1">
            <ShieldCheck className="w-3 h-3" />
            <span>Nominal</span>
          </span>
        )}
      </div>
    </div>
  );
}
