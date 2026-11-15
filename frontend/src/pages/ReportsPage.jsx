import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { 
  FileText, Download, Calendar, User, Clock, Shield, 
  Activity, AlertTriangle, CheckCircle2, Heart, Thermometer,
  Radio, RefreshCw, Eye
} from 'lucide-react';

export default function ReportsPage() {
  const { user, isAstronaut, isSurgeon, isAdmin } = useAuth();
  const [astronauts, setAstronauts] = useState([]);
  const [selectedAstroId, setSelectedAstroId] = useState('');
  const [timeRangeHours, setTimeRangeHours] = useState(24);
  const [previewAstro, setPreviewAstro] = useState(null);
  const [vitalsSample, setVitalsSample] = useState([]);
  const [alertsSample, setAlertsSample] = useState([]);
  const [loading, setLoading] = useState(true);
  const [downloading, setDownloading] = useState(false);

  useEffect(() => {
    const fetchAstronauts = async () => {
      try {
        const res = await axios.get('/api/astronauts');
        setAstronauts(res.data);
        if (isAstronaut && user?.astronaut_id) {
          setSelectedAstroId(user.astronaut_id);
        } else if (res.data.length > 0) {
          setSelectedAstroId(res.data[0].id);
        }
      } catch (e) {
        console.error("Failed to load astronauts", e);
      } finally {
        setLoading(false);
      }
    };
    fetchAstronauts();
  }, [isAstronaut, user]);

  useEffect(() => {
    if (!selectedAstroId) return;
    const fetchPreview = async () => {
      try {
        const [astroRes, vitalsRes, alertsRes] = await Promise.all([
          axios.get(`/api/astronauts/${selectedAstroId}`),
          axios.get(`/api/astronauts/${selectedAstroId}/vitals?limit=20`),
          axios.get(`/api/alerts?astronaut_id=${selectedAstroId}&limit=10`)
        ]);
        setPreviewAstro(astroRes.data);
        setVitalsSample(vitalsRes.data);
        setAlertsSample(alertsRes.data);
      } catch (e) {
        console.error("Preview load error", e);
      }
    };
    fetchPreview();
  }, [selectedAstroId, timeRangeHours]);

  const handleDownload = async (format) => {
    if (!selectedAstroId) return;
    setDownloading(true);
    try {
      const response = await axios.get(`/api/reports/${selectedAstroId}?format=${format}&hours=${timeRangeHours}`, {
        responseType: 'blob'
      });
      const blob = new Blob([response.data], {
        type: format === 'pdf' ? 'application/pdf' : 'text/csv'
      });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      const astroName = previewAstro?.callsign || `astro_${selectedAstroId}`;
      link.href = url;
      link.setAttribute('download', `dr_d_health_report_${astroName.toLowerCase()}_${timeRangeHours}h.${format}`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (e) {
      console.error("Export download error", e);
      alert("Failed to generate report export.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header Banner */}
      <div className="hud-panel rounded-2xl p-5 border border-cyan-500/25 bg-space-900/90 relative corner-accent">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <FileText className="w-5 h-5 text-cyan-400" />
              <h1 className="text-xl font-black text-slate-100 tracking-tight">
                MISSION CLINICAL TELEMETRY REPORTS & ARCHIVAL EXPORT
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-amber-500/40 text-amber-400 font-bold">
                SIMULATED DATA
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Generate standardized flight surgeon health summaries, physiological time-series records, and anomaly logs in PDF or CSV format.
            </p>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-mono text-cyan-400 bg-cyan-950/80 px-2.5 py-1 rounded border border-cyan-500/30">
              ARES-V FLIGHT SURGEON PROTOCOL #44
            </span>
          </div>
        </div>
      </div>

      {/* Control Configuration Bar */}
      <div className="hud-panel rounded-xl p-5 border border-cyan-500/20 bg-space-850/80">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 items-end">
          
          {/* Astronaut Selector */}
          <div>
            <label className="block text-xs font-mono text-slate-400 mb-1.5 uppercase">
              Select Crew Member
            </label>
            <select
              value={selectedAstroId}
              onChange={(e) => setSelectedAstroId(Number(e.target.value))}
              disabled={isAstronaut && user?.astronaut_id}
              className="w-full bg-space-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:border-cyan-400 outline-none font-medium"
            >
              {astronauts.map(a => (
                <option key={a.id} value={a.id}>
                  {a.name} ({a.callsign}) — {a.role_title}
                </option>
              ))}
            </select>
          </div>

          {/* Time Window */}
          <div>
            <label className="block text-xs font-mono text-slate-400 mb-1.5 uppercase">
              Time Window Duration
            </label>
            <select
              value={timeRangeHours}
              onChange={(e) => setTimeRangeHours(Number(e.target.value))}
              className="w-full bg-space-900 border border-slate-700 rounded-lg px-3 py-2 text-sm text-slate-200 focus:border-cyan-400 outline-none font-medium"
            >
              <option value={6}>Last 6 Hours (Post-EVA window)</option>
              <option value={24}>Last 24 Hours (Daily Flight Surgeon Sol)</option>
              <option value={72}>Last 72 Hours (Multi-sol trend)</option>
              <option value={168}>Last 7 Sols (Weekly comprehensive)</option>
            </select>
          </div>

          {/* Export Buttons */}
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleDownload('pdf')}
              disabled={downloading}
              className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-space-950 font-bold rounded-lg text-xs font-mono transition-all shadow-glow-cyan disabled:opacity-50"
            >
              <Download className="w-4 h-4" />
              <span>EXPORT PDF</span>
            </button>

            <button
              onClick={() => handleDownload('csv')}
              disabled={downloading}
              className="flex-1 flex items-center justify-center space-x-2 px-4 py-2 bg-space-800 hover:bg-space-700 border border-slate-700 hover:border-slate-600 text-slate-200 font-bold rounded-lg text-xs font-mono transition-all disabled:opacity-50"
            >
              <Download className="w-4 h-4 text-slate-400" />
              <span>EXPORT CSV</span>
            </button>
          </div>

        </div>
      </div>

      {/* Report Document Preview */}
      <div className="hud-panel rounded-xl p-6 border border-cyan-500/20 bg-space-900/90 relative">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-6">
          <div className="flex items-center space-x-2">
            <Eye className="w-4 h-4 text-cyan-400" />
            <h3 className="font-bold text-slate-100 text-sm tracking-wider uppercase font-mono">
              DOCUMENT PREVIEW — DR D FLIGHT SURGEON DOSSIER
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-400">
            Window: Past {timeRangeHours} Hours
          </span>
        </div>

        {previewAstro ? (
          <div className="space-y-6">
            
            {/* Subject Overview Card */}
            <div className="p-4 rounded-xl bg-space-850/80 border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div className="flex items-center space-x-4">
                <img
                  src={previewAstro.avatar_url || "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=120"}
                  alt={previewAstro.name}
                  className="w-16 h-16 rounded-xl object-cover border border-slate-700 shadow-md"
                />
                <div>
                  <div className="flex items-center space-x-2">
                    <h2 className="text-lg font-bold text-slate-100">{previewAstro.name}</h2>
                    <span className="text-xs font-mono font-bold text-cyan-400 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-500/30">
                      "{previewAstro.callsign}"
                    </span>
                  </div>
                  <p className="text-xs text-slate-400">{previewAstro.role_title}</p>
                  <div className="flex items-center space-x-3 text-[11px] font-mono text-slate-400 mt-1">
                    <span>Age: {previewAstro.age} yrs</span>
                    <span>•</span>
                    <span>Blood: {previewAstro.blood_type}</span>
                    <span>•</span>
                    <span className="text-cyan-300">Status: {previewAstro.status}</span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs font-mono text-right">
                <div className="bg-space-900 p-2 rounded border border-slate-800">
                  <span className="text-slate-500 text-[10px] block uppercase">Cumulative Dose</span>
                  <span className="text-sm font-bold text-purple-400">
                    {previewAstro.radiation_msv?.toFixed(1)} / {previewAstro.radiation_limit_msv} mSv
                  </span>
                </div>
                <div className="bg-space-900 p-2 rounded border border-slate-800">
                  <span className="text-slate-500 text-[10px] block uppercase">Risk Index</span>
                  <span className="text-sm font-bold text-cyan-400">
                    {previewAstro.current_risk_score ?? 16} / 100
                  </span>
                </div>
              </div>
            </div>

            {/* Physiological Baseline Comparison */}
            <div>
              <h4 className="text-xs font-mono uppercase text-cyan-400 font-semibold mb-2">
                1. Physiological Baseline & Parameter Window (Mean Sample)
              </h4>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
                <div className="p-3 rounded-lg bg-space-850 border border-slate-800">
                  <span className="text-slate-400 text-[10px] uppercase block">Heart Rate</span>
                  <span className="text-base font-bold text-rose-400">
                    {vitalsSample.length > 0 ? (vitalsSample.reduce((a, b) => a + b.heart_rate, 0) / vitalsSample.length).toFixed(1) : previewAstro.baseline_hr} bpm
                  </span>
                  <span className="text-[10px] text-slate-500 block">Baseline: {previewAstro.baseline_hr} bpm</span>
                </div>

                <div className="p-3 rounded-lg bg-space-850 border border-slate-800">
                  <span className="text-slate-400 text-[10px] uppercase block">Oxygen SpO2</span>
                  <span className="text-base font-bold text-cyan-400">
                    {vitalsSample.length > 0 ? (vitalsSample.reduce((a, b) => a + b.spo2, 0) / vitalsSample.length).toFixed(1) : previewAstro.baseline_spo2}%
                  </span>
                  <span className="text-[10px] text-slate-500 block">Baseline: {previewAstro.baseline_spo2}%</span>
                </div>

                <div className="p-3 rounded-lg bg-space-850 border border-slate-800">
                  <span className="text-slate-400 text-[10px] uppercase block">Core Body Temp</span>
                  <span className="text-base font-bold text-amber-400">
                    {vitalsSample.length > 0 ? (vitalsSample.reduce((a, b) => a + b.core_temp, 0) / vitalsSample.length).toFixed(2) : previewAstro.baseline_temp} °C
                  </span>
                  <span className="text-[10px] text-slate-500 block">Baseline: {previewAstro.baseline_temp} °C</span>
                </div>

                <div className="p-3 rounded-lg bg-space-850 border border-slate-800">
                  <span className="text-slate-400 text-[10px] uppercase block">Blood Pressure</span>
                  <span className="text-base font-bold text-emerald-400">
                    {previewAstro.baseline_bp_sys?.toFixed(0)} / {previewAstro.baseline_bp_dia?.toFixed(0)} mmHg
                  </span>
                  <span className="text-[10px] text-slate-500 block">Arterial Mean OK</span>
                </div>
              </div>
            </div>

            {/* Recent Recorded Telemetry Readings Sample Table */}
            <div>
              <h4 className="text-xs font-mono uppercase text-cyan-400 font-semibold mb-2">
                2. Telemetry Ingestion Series Sample ({vitalsSample.length} data points)
              </h4>
              <div className="overflow-x-auto rounded-lg border border-slate-800">
                <table className="w-full text-left text-xs font-mono">
                  <thead className="bg-space-850 text-slate-400 uppercase text-[10px]">
                    <tr>
                      <th className="p-2.5">Time (UTC)</th>
                      <th className="p-2.5">HR (bpm)</th>
                      <th className="p-2.5">HRV (ms)</th>
                      <th className="p-2.5">SpO2 (%)</th>
                      <th className="p-2.5">BP (mmHg)</th>
                      <th className="p-2.5">Temp (°C)</th>
                      <th className="p-2.5">Stress (/100)</th>
                      <th className="p-2.5">Activity</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/80 bg-space-900/60 text-slate-300">
                    {vitalsSample.slice(0, 6).map((v, idx) => (
                      <tr key={idx} className="hover:bg-space-800/40">
                        <td className="p-2.5 text-slate-400">{new Date(v.timestamp).toLocaleTimeString()}</td>
                        <td className="p-2.5 font-bold text-slate-200">{v.heart_rate?.toFixed(0)}</td>
                        <td className="p-2.5">{v.hrv?.toFixed(0)}</td>
                        <td className="p-2.5 text-cyan-400">{v.spo2?.toFixed(1)}</td>
                        <td className="p-2.5">{v.bp_systolic?.toFixed(0)}/{v.bp_diastolic?.toFixed(0)}</td>
                        <td className="p-2.5 text-amber-400">{v.core_temp?.toFixed(2)}</td>
                        <td className="p-2.5">{v.stress_index?.toFixed(0)}</td>
                        <td className="p-2.5">
                          <span className="px-1.5 py-0.5 rounded text-[10px] bg-space-800 text-slate-300">
                            {v.activity_level}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Logged Alerts In Scope */}
            <div>
              <h4 className="text-xs font-mono uppercase text-cyan-400 font-semibold mb-2">
                3. Alert Log & Interventions in Time Window ({alertsSample.length} events)
              </h4>
              <div className="space-y-2">
                {alertsSample.length === 0 ? (
                  <div className="p-3 bg-space-850/60 rounded border border-slate-800 text-xs text-slate-400 font-mono">
                    No active or warning alerts logged for this astronaut during the selected timeframe.
                  </div>
                ) : (
                  alertsSample.map((al, idx) => (
                    <div key={idx} className="p-3 bg-space-850/80 rounded-lg border border-slate-800 text-xs font-mono flex items-start justify-between">
                      <div>
                        <div className="flex items-center space-x-2 mb-1">
                          <span className={`text-[9px] uppercase font-bold px-1.5 py-0.5 rounded ${
                            al.threshold_level === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'
                          }`}>
                            {al.threshold_level}
                          </span>
                          <span className="font-semibold text-slate-200">{al.message}</span>
                        </div>
                        <span className="text-[11px] text-slate-400 block">
                          Suggested Action: {al.suggested_action}
                        </span>
                        {al.notes && (
                          <span className="text-[10px] text-cyan-300 mt-1 block">
                            Flight Surgeon Note: {al.notes}
                          </span>
                        )}
                      </div>
                      <span className="text-[10px] text-slate-500">
                        {new Date(al.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  ))
                )}
              </div>
            </div>

          </div>
        ) : (
          <div className="p-8 text-center text-slate-500 font-mono text-xs">
            Loading preview dossier...
          </div>
        )}
      </div>

    </div>
  );
}
