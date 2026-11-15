import React, { useState } from 'react';
import { AlertCircle, X, ShieldAlert, CheckCircle2, BookOpen, ChevronDown, ChevronUp, ExternalLink, Activity } from 'lucide-react';
import { useLiveTelemetry } from '../context/WebSocketContext';
import axios from 'axios';

export default function AlertBanner() {
  const { latestAlertBanner, setLatestAlertBanner } = useLiveTelemetry();
  const [showResearchContext, setShowResearchContext] = useState(false);

  if (!latestAlertBanner) return null;

  const isCritical = latestAlertBanner.threshold_level === 'CRITICAL';
  const ctx = latestAlertBanner.research_context;

  const handleAcknowledge = async () => {
    try {
      await axios.patch(`/api/alerts/${latestAlertBanner.id}`, {
        status: 'ACKNOWLEDGED',
        notes: 'Quick acknowledged from telemetry banner.'
      });
      setLatestAlertBanner(null);
    } catch (e) {
      setLatestAlertBanner(null);
    }
  };

  return (
    <div className={`relative px-4 py-2.5 transition-all duration-300 z-30 ${
      isCritical 
        ? 'bg-rose-950/95 border-b-2 border-rose-500 text-rose-100 shadow-glow-rose' 
        : 'bg-amber-950/95 border-b border-amber-500 text-amber-100 shadow-glow-amber'
    }`}>
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-start sm:items-center space-x-3">
          <div className={`p-1.5 rounded shrink-0 ${isCritical ? 'bg-rose-500/20 text-rose-400' : 'bg-amber-500/20 text-amber-400'}`}>
            <ShieldAlert className="w-5 h-5 animate-bounce" />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <span className={`text-[10px] uppercase font-mono font-bold px-1.5 py-0.5 rounded ${
                isCritical ? 'bg-rose-600 text-white' : 'bg-amber-600 text-white'
              }`}>
                {latestAlertBanner.threshold_level} ALERT
              </span>
              <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-space-950/80 border border-slate-700 text-amber-400 font-semibold">
                SIMULATED DATA
              </span>
              <span className="text-xs font-semibold text-white">
                {latestAlertBanner.astronaut_callsign ? `[${latestAlertBanner.astronaut_callsign}]` : '[CABIN]'} {latestAlertBanner.message}
              </span>
            </div>
            <div className="text-[11px] text-slate-300 mt-1">
              <span className="text-cyan-300 font-medium">Protocol: </span>
              {latestAlertBanner.suggested_action}
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2 shrink-0">
          {ctx && (
            <button
              onClick={() => setShowResearchContext(prev => !prev)}
              className="flex items-center space-x-1 px-2.5 py-1 bg-space-900 hover:bg-space-850 text-cyan-300 hover:text-cyan-200 text-xs font-mono rounded border border-cyan-500/40 transition-colors"
            >
              <BookOpen className="w-3.5 h-3.5" />
              <span>RESEARCH CONTEXT</span>
              {showResearchContext ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
            </button>
          )}

          <button
            onClick={handleAcknowledge}
            className="flex items-center space-x-1 px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-slate-950 text-xs font-bold rounded transition-colors shadow-glow-cyan"
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>ACKNOWLEDGE</span>
          </button>
          <button
            onClick={() => setLatestAlertBanner(null)}
            className="p-1 text-slate-400 hover:text-white rounded"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Expandable NASA Research Context Panel */}
      {showResearchContext && ctx && (
        <div className="max-w-7xl mx-auto mt-3 pt-3 border-t border-slate-800/80 grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
          <div className="bg-space-950/90 p-2.5 rounded border border-cyan-500/30">
            <div className="text-[10px] text-cyan-400 font-bold uppercase tracking-wider mb-0.5">NASA Spaceflight Hazard</div>
            <div className="text-slate-100 font-semibold">{ctx.nasa_hazard}</div>
            <div className="text-[10px] text-slate-400 mt-1">Detected: {ctx.detected_condition}</div>
          </div>

          <div className="bg-space-950/90 p-2.5 rounded border border-amber-500/30">
            <div className="text-[10px] text-amber-400 font-bold uppercase tracking-wider mb-0.5">Potential Health Implications</div>
            <div className="text-slate-200 text-[11px]">{ctx.potential_implications}</div>
            <div className="text-[10px] text-slate-400 mt-1">Clinical evidence from NASA Human Research Program</div>
          </div>

          <div className="bg-space-950/90 p-2.5 rounded border border-purple-500/30 flex flex-col justify-between">
            <div>
              <div className="text-[10px] text-purple-300 font-bold uppercase tracking-wider mb-0.5">Scientific Citation & Provenance</div>
              <div className="text-[11px] text-slate-200 line-clamp-2">{ctx.research_reference}</div>
            </div>
            <div className="flex items-center justify-between mt-2 pt-1 border-t border-slate-800 text-[10px]">
              <span className="text-amber-400 font-bold">Provenance: {ctx.data_source}</span>
              {ctx.official_url && (
                <a 
                  href={ctx.official_url} 
                  target="_blank" 
                  rel="noreferrer"
                  className="text-cyan-400 hover:underline flex items-center space-x-0.5"
                >
                  <span>NASA HRP</span>
                  <ExternalLink className="w-2.5 h-2.5" />
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
