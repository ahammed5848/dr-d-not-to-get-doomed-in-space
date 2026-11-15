import React from 'react';
import { ShieldCheck, AlertCircle, AlertTriangle, Info, CheckCircle2 } from 'lucide-react';

export default function RiskIndexBreakdown({ riskData }) {
  if (!riskData) return null;

  const score = riskData.composite_risk_score ?? 15.0;
  const level = riskData.risk_level || 'NOMINAL';
  const factors = riskData.factors || [];

  let levelColor = 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30';
  let gaugeColor = '#10b981';
  if (level === 'SEVERE' || score >= 75) {
    levelColor = 'text-rose-400 bg-rose-500/20 border-rose-500/40 shadow-glow-rose';
    gaugeColor = '#f43f5e';
  } else if (level === 'HIGH' || score >= 50) {
    levelColor = 'text-amber-400 bg-amber-500/20 border-amber-500/40 shadow-glow-amber';
    gaugeColor = '#f59e0b';
  } else if (level === 'ELEVATED' || score >= 25) {
    levelColor = 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30';
    gaugeColor = '#06b6d4';
  }

  return (
    <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
      
      {/* Title Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-800 mb-4 gap-2">
        <div>
          <div className="flex items-center space-x-2">
            <h3 className="font-bold text-slate-100 text-sm tracking-wide">
              HEALTH RISK INDEX (HRI) & EXPLAINABILITY
            </h3>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-purple-500/40 text-purple-300 font-bold">
              MODEL-GENERATED OUTPUT
            </span>
          </div>
          <span className="text-[11px] text-slate-400">Multi-variable isolation forest & autonomic load modeling (Simulated research metric)</span>
        </div>
        <span className={`text-xs font-mono font-bold px-2.5 py-1 rounded border uppercase self-start sm:self-auto ${levelColor}`}>
          {level} RISK
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
        
        {/* Gauge & Main Score */}
        <div className="flex flex-col items-center justify-center p-4 bg-space-900/60 rounded-xl border border-slate-800">
          <div className="relative w-32 h-32 flex items-center justify-center">
            {/* SVG circular progress */}
            <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
              <circle
                cx="50" cy="50" r="42"
                stroke="#1e293b"
                strokeWidth="8"
                fill="none"
              />
              <circle
                cx="50" cy="50" r="42"
                stroke={gaugeColor}
                strokeWidth="8"
                strokeDasharray={264}
                strokeDashoffset={264 - (264 * Math.min(100, Math.max(0, score))) / 100}
                strokeLinecap="round"
                fill="none"
                className="transition-all duration-700 ease-out"
              />
            </svg>
            <div className="absolute flex flex-col items-center">
              <span className="text-3xl font-extrabold font-mono tracking-tight text-slate-100">
                {score.toFixed(0)}
              </span>
              <span className="text-[10px] font-mono text-slate-400 uppercase">/100 Index</span>
            </div>
          </div>

          <div className="text-center mt-3">
            <span className="text-xs font-semibold text-slate-300">Predictive Risk Level</span>
            <p className="text-[11px] text-slate-400 mt-0.5">
              {score < 25 ? 'Normal physiological homeostasis' : score < 50 ? 'Mild compensatory physiological stress' : 'Significant physiological anomaly detected'}
            </p>
          </div>
        </div>

        {/* Contributing Factors Breakdown */}
        <div className="lg:col-span-2 space-y-3">
          <h4 className="text-xs font-mono uppercase text-slate-400 tracking-wider">
            Contributing Factor Breakdown
          </h4>

          <div className="space-y-2.5">
            {factors.map((f, i) => {
              const fScore = f.score || 0;
              let barColor = 'bg-cyan-500';
              let impactColor = 'text-cyan-400';
              if (f.impact === 'CRITICAL' || fScore >= 60) {
                barColor = 'bg-rose-500';
                impactColor = 'text-rose-400 font-bold';
              } else if (f.impact === 'HIGH' || fScore >= 35) {
                barColor = 'bg-amber-400';
                impactColor = 'text-amber-400 font-semibold';
              } else if (f.impact === 'MEDIUM' || fScore >= 15) {
                barColor = 'bg-cyan-400';
                impactColor = 'text-cyan-300';
              } else {
                barColor = 'bg-slate-600';
                impactColor = 'text-slate-400';
              }

              return (
                <div key={i} className="p-2.5 bg-space-850 rounded-lg border border-slate-800 text-xs">
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="font-semibold text-slate-200">{f.name}</span>
                    <div className="flex items-center space-x-2">
                      <span className={`text-[10px] font-mono uppercase ${impactColor}`}>
                        {f.impact}
                      </span>
                      <span className="font-mono font-bold text-slate-100">{fScore.toFixed(0)}/100</span>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden mb-1">
                    <div 
                      className={`h-full rounded-full transition-all duration-500 ${barColor}`} 
                      style={{ width: `${Math.min(100, Math.max(3, fScore))}%` }}
                    />
                  </div>

                  <div className="text-[10px] font-mono text-slate-400">
                    {f.detail}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* Explainability Callout Box */}
      <div className="mt-4 p-3.5 bg-space-850 rounded-lg border border-slate-800 flex items-start space-x-3 text-xs">
        <Info className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />
        <div>
          <div className="font-bold text-cyan-300 mb-0.5">Clinical Explanation:</div>
          <div className="text-slate-300">{riskData.summary_explanation}</div>
          <div className="text-slate-400 mt-1">
            <span className="text-amber-400 font-semibold">Suggested Protocol: </span>
            {riskData.recommended_action}
          </div>
        </div>
      </div>

    </div>
  );
}
