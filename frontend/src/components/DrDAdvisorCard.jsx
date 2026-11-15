import React from 'react';
import { Bot, Sparkles, CheckCircle2, Clock, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function DrDAdvisorCard({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null;

  return (
    <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
      
      {/* Title */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div className="flex items-center space-x-2">
          <div className="p-1.5 rounded bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
            <Sparkles className="w-4 h-4" />
          </div>
          <div>
            <h3 className="font-bold text-slate-100 text-sm tracking-wide">
              DR D ADVISOR — CLINICAL RECOMMENDATIONS
            </h3>
            <span className="text-[10px] text-slate-400">Rule-based physiological expert engine with modular LLM interface</span>
          </div>
        </div>
        <span className="text-[10px] font-mono uppercase bg-cyan-950 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30">
          AI Co-Pilot Active
        </span>
      </div>

      {/* Recommendations List */}
      <div className="space-y-3">
        {recommendations.map((rec, i) => {
          let badgeColor = 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30';
          let borderHighlight = 'border-slate-800';

          if (rec.priority === 'CRITICAL') {
            badgeColor = 'bg-rose-500/20 text-rose-300 border-rose-500/40 shadow-glow-rose';
            borderHighlight = 'border-rose-500/40 bg-rose-950/20';
          } else if (rec.priority === 'HIGH') {
            badgeColor = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
            borderHighlight = 'border-amber-500/30 bg-amber-950/20';
          }

          return (
            <div 
              key={i} 
              className={`p-3.5 rounded-lg border ${borderHighlight} bg-space-850/80 transition-all text-xs`}
            >
              <div className="flex items-start justify-between mb-2">
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-slate-100 text-sm">{rec.title}</span>
                    <span className={`text-[9px] font-mono uppercase font-bold px-1.5 py-0.2 rounded border ${badgeColor}`}>
                      {rec.priority}
                    </span>
                  </div>
                  <span className="text-[10px] font-mono text-cyan-400/80 uppercase">
                    Protocol: {rec.category}
                  </span>
                </div>
              </div>

              <div className="text-slate-300 mb-2">
                <span className="text-slate-400 font-medium">Finding: </span>
                {rec.observation}
              </div>

              <div className="bg-space-900/90 p-2.5 rounded border border-slate-800 mb-2 text-cyan-200">
                <span className="text-cyan-400 font-semibold block mb-0.5">Recommended Countermeasure:</span>
                {rec.action}
              </div>

              <div className="flex items-center space-x-1.5 text-[10px] font-mono text-slate-400">
                <Clock className="w-3 h-3 text-slate-400" />
                <span>Expected Recovery Time: {rec.expected_recovery}</span>
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}
