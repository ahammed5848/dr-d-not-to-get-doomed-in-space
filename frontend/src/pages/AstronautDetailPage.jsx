import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useLiveTelemetry } from '../context/WebSocketContext';
import BodySilhouette from '../components/BodySilhouette';
import RiskIndexBreakdown from '../components/RiskIndexBreakdown';
import DrDAdvisorCard from '../components/DrDAdvisorCard';
import { 
  Heart, Activity, Thermometer, Wind, Radio, Shield, 
  ArrowLeft, Clock, TrendingUp, Plus, FileText, CheckCircle2, AlertTriangle, Moon
} from 'lucide-react';
import { 
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, 
  Tooltip, CartesianGrid, ReferenceLine, LineChart, Line, Legend
} from 'recharts';

export default function AstronautDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { isSurgeon, isAdmin, user } = useAuth();
  const { crewTelemetry } = useLiveTelemetry();

  const [astronaut, setAstronaut] = useState(null);
  const [vitalsHistory, setVitalsHistory] = useState([]);
  const [riskData, setRiskData] = useState(null);
  const [forecastData, setForecastData] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [notes, setNotes] = useState([]);
  const [activeMetricTab, setActiveMetricTab] = useState('heart_rate');
  const [loading, setLoading] = useState(true);

  // New Note modal state
  const [showNoteModal, setShowNoteModal] = useState(false);
  const [noteCategory, setNoteCategory] = useState('CLINICAL_OBSERVATION');
  const [noteText, setNoteText] = useState('');

  const fetchDetail = async () => {
    try {
      const [aRes, vRes, rRes, fRes, recRes, nRes] = await Promise.all([
        axios.get(`/api/astronauts/${id}`),
        axios.get(`/api/astronauts/${id}/vitals?limit=40`),
        axios.get(`/api/astronauts/${id}/risk`),
        axios.get(`/api/astronauts/${id}/forecast`),
        axios.get(`/api/astronauts/${id}/advisor`),
        axios.get(`/api/astronauts/${id}/notes`)
      ]);
      setAstronaut(aRes.data);
      setVitalsHistory(vRes.data);
      setRiskData(rRes.data);
      setForecastData(fRes.data);
      setRecommendations(recRes.data.recommendations || []);
      setNotes(nRes.data || []);
    } catch (e) {
      console.error("Failed to load astronaut detail", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetail();
    const interval = setInterval(fetchDetail, 4000);
    return () => clearInterval(interval);
  }, [id]);

  const handleAddNote = async (e) => {
    e.preventDefault();
    if (!noteText.trim()) return;
    try {
      await axios.post(`/api/astronauts/${id}/notes`, {
        category: noteCategory,
        note_text: noteText
      });
      setNoteText('');
      setShowNoteModal(false);
      fetchDetail();
    } catch (e) {
      console.error("Failed to post note", e);
    }
  };

  if (loading || !astronaut) {
    return <div className="p-12 text-center font-mono text-cyan-400">Loading astronaut biometrics telemetry...</div>;
  }

  // Live overrides
  const liveAstro = crewTelemetry[id];
  const currentVitals = liveAstro?.vitals || astronaut.latest_vitals || vitalsHistory[vitalsHistory.length - 1] || {};
  const currentRisk = liveAstro?.risk || riskData;

  // Chart configuration for selected tab
  const metricConfigs = {
    heart_rate: {
      name: 'Heart Rate',
      unit: 'bpm',
      color: '#f43f5e',
      warnHigh: 100,
      critHigh: 125,
      warnLow: 50,
      critLow: 45,
      baseline: astronaut.baseline_hr
    },
    spo2: {
      name: 'Blood Oxygen (SpO2)',
      unit: '%',
      color: '#22d3ee',
      warnLow: 95,
      critLow: 91,
      baseline: astronaut.baseline_spo2
    },
    core_temp: {
      name: 'Core Body Temperature',
      unit: '°C',
      color: '#f59e0b',
      warnHigh: 37.8,
      critHigh: 38.6,
      baseline: astronaut.baseline_temp
    },
    stress_index: {
      name: 'Sympathetic Stress Index',
      unit: '/100',
      color: '#a855f7',
      warnHigh: 65,
      critHigh: 85,
      baseline: 22
    }
  };

  const currentMetricConfig = metricConfigs[activeMetricTab];

  // Format historical chart data
  const chartData = vitalsHistory.map(v => ({
    time: new Date(v.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
    heart_rate: v.heart_rate,
    spo2: v.spo2,
    core_temp: v.core_temp,
    stress_index: v.stress_index,
    bp_sys: v.bp_systolic,
    bp_dia: v.bp_diastolic
  }));

  // Forecast points
  const forecastPoints = forecastData?.metrics?.[activeMetricTab]?.points || [];

  return (
    <div className="space-y-6 pb-12">
      
      {/* Top Navigation & Profile Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center space-x-1.5 text-xs font-mono text-slate-400 hover:text-cyan-300 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>&larr; BACK TO MISSION FLEET</span>
        </button>

        <div className="flex items-center space-x-2">
          <span className="text-[10px] font-mono text-slate-400">TELEMETRY ENCRYPTION: AES-256</span>
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
        </div>
      </div>

      {/* Astronaut Dossier Banner */}
      <div className="hud-panel rounded-2xl p-6 border border-cyan-500/25 bg-space-900/90 relative corner-accent">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          
          <div className="flex items-center space-x-4">
            <img 
              src={astronaut.avatar_url || "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=160"} 
              alt={astronaut.name}
              className="w-20 h-20 rounded-xl object-cover border-2 border-cyan-500/40 shadow-glow-cyan" 
            />
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <h1 className="text-2xl font-black text-slate-100">{astronaut.name}</h1>
                <span className="font-mono text-sm font-bold text-cyan-400 bg-cyan-950/80 px-2 py-0.5 rounded border border-cyan-500/40">
                  CALLSIGN: {astronaut.callsign}
                </span>
                <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border uppercase ${
                  astronaut.status === 'CRITICAL' ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' : astronaut.status === 'WARNING' ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
                }`}>
                  {astronaut.status}
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-amber-500/40 text-amber-400 font-bold">
                  SIMULATED DATA
                </span>
              </div>
              
              <div className="text-xs text-slate-400 mt-1 flex flex-wrap gap-x-4 gap-y-1 font-mono">
                <span>Role: <strong className="text-slate-200">{astronaut.role_title}</strong></span>
                <span>Age: <strong className="text-slate-200">{astronaut.age} yrs</strong></span>
                <span>Blood: <strong className="text-slate-200">{astronaut.blood_type}</strong></span>
                <span>Mission Sol: <strong className="text-cyan-400">142</strong></span>
              </div>
            </div>
          </div>

          {/* Cumulative Radiation Progress */}
          <div className="w-full md:w-64 p-3 bg-space-850 rounded-xl border border-slate-800 text-xs">
            <div className="flex items-center justify-between mb-1.5 font-mono">
              <span className="text-slate-400 flex items-center space-x-1">
                <Radio className="w-3.5 h-3.5 text-purple-400" />
                <span>Radiation Exposure</span>
              </span>
              <span className="text-cyan-300 font-bold">
                {astronaut.radiation_msv?.toFixed(1)} / {astronaut.radiation_limit_msv} mSv
              </span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-cyan-500 via-amber-400 to-purple-500 h-full rounded-full transition-all duration-500"
                style={{ width: `${(astronaut.radiation_msv / astronaut.radiation_limit_msv) * 100}%` }}
              />
            </div>
            <span className="text-[10px] text-slate-500 font-mono mt-1 block text-right">
              {((astronaut.radiation_msv / astronaut.radiation_limit_msv) * 100).toFixed(1)}% of mission career ceiling
            </span>
          </div>

        </div>
      </div>

      {/* Main Telemetry & Line Charts Section with Threshold Bands */}
      <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
        
        {/* Metric Selector Tabs */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between pb-4 border-b border-slate-800 gap-3">
          <div className="flex items-center space-x-2">
            <Activity className="w-5 h-5 text-cyan-400" />
            <h3 className="font-bold text-slate-100 text-sm tracking-wide">
              REAL-TIME PHYSIOLOGICAL STREAM & THRESHOLD BANDS
            </h3>
          </div>

          <div className="flex flex-wrap gap-1 font-mono text-xs">
            {Object.keys(metricConfigs).map(key => {
              const cfg = metricConfigs[key];
              const isActive = activeMetricTab === key;
              return (
                <button
                  key={key}
                  onClick={() => setActiveMetricTab(key)}
                  className={`px-3 py-1 rounded transition-colors ${
                    isActive 
                      ? 'bg-cyan-500 text-space-950 font-bold shadow-glow-cyan' 
                      : 'bg-space-850 text-slate-400 hover:text-white border border-slate-800'
                  }`}
                >
                  {cfg.name}
                </button>
              );
            })}
          </div>
        </div>

        {/* Current Readout & Threshold info */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 my-4 p-3 bg-space-850 rounded-lg border border-slate-800 text-xs font-mono">
          <div>
            <span className="text-slate-500 block uppercase text-[10px]">Current Telemetry</span>
            <span className="text-xl font-black" style={{ color: currentMetricConfig.color }}>
              {currentVitals[activeMetricTab]?.toFixed(1)} {currentMetricConfig.unit}
            </span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase text-[10px]">Personal Baseline</span>
            <span className="text-base font-bold text-slate-300">
              {currentMetricConfig.baseline?.toFixed(1)} {currentMetricConfig.unit}
            </span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase text-[10px]">Warning Band</span>
            <span className="text-base font-bold text-amber-400">
              {currentMetricConfig.warnHigh ? `> ${currentMetricConfig.warnHigh}` : `< ${currentMetricConfig.warnLow}`} {currentMetricConfig.unit}
            </span>
          </div>
          <div>
            <span className="text-slate-500 block uppercase text-[10px]">Critical Threshold</span>
            <span className="text-base font-bold text-rose-400">
              {currentMetricConfig.critHigh ? `> ${currentMetricConfig.critHigh}` : `< ${currentMetricConfig.critLow}`} {currentMetricConfig.unit}
            </span>
          </div>
        </div>

        {/* Recharts Live Line Chart */}
        <div className="h-72 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="metricGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={currentMetricConfig.color} stopOpacity={0.35}/>
                  <stop offset="95%" stopColor={currentMetricConfig.color} stopOpacity={0.0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="time" stroke="#64748b" tick={{ fontSize: 10 }} />
              <YAxis stroke="#64748b" tick={{ fontSize: 10 }} domain={['auto', 'auto']} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#0b132b', borderColor: '#22d3ee', borderRadius: 8, fontSize: 12 }} 
                labelStyle={{ color: '#94a3b8' }}
              />
              
              {/* Threshold Reference Lines */}
              {currentMetricConfig.warnHigh && (
                <ReferenceLine y={currentMetricConfig.warnHigh} stroke="#f59e0b" strokeDasharray="4 4" label={{ value: 'WARNING', fill: '#f59e0b', fontSize: 10 }} />
              )}
              {currentMetricConfig.critHigh && (
                <ReferenceLine y={currentMetricConfig.critHigh} stroke="#f43f5e" strokeDasharray="4 4" label={{ value: 'CRITICAL', fill: '#f43f5e', fontSize: 10 }} />
              )}
              {currentMetricConfig.warnLow && (
                <ReferenceLine y={currentMetricConfig.warnLow} stroke="#f59e0b" strokeDasharray="4 4" label={{ value: 'WARN LOW', fill: '#f59e0b', fontSize: 10 }} />
              )}
              {currentMetricConfig.critLow && (
                <ReferenceLine y={currentMetricConfig.critLow} stroke="#f43f5e" strokeDasharray="4 4" label={{ value: 'CRIT LOW', fill: '#f43f5e', fontSize: 10 }} />
              )}

              <Area 
                type="monotone" 
                dataKey={activeMetricTab} 
                stroke={currentMetricConfig.color} 
                strokeWidth={2.5} 
                fillOpacity={1} 
                fill="url(#metricGradient)" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Predictive Trend Forecast (Next 30 Minutes) */}
        {forecastPoints.length > 0 && (
          <div className="mt-6 pt-4 border-t border-slate-800">
            <div className="flex flex-wrap items-center justify-between mb-2 gap-2">
              <span className="text-xs font-mono uppercase text-cyan-400 font-bold flex items-center space-x-1.5">
                <TrendingUp className="w-4 h-4" />
                <span>30-Minute Predictive Forecast & Horizon Breach Detection</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-purple-500/40 text-purple-300 font-bold ml-2">
                  MODEL-GENERATED OUTPUT
                </span>
              </span>
              <span className="text-[10px] font-mono text-slate-400">
                Algorithm: Linear Dampened Extrapolation & Confidence Cone
              </span>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-6 gap-2">
              {forecastPoints.map((pt, i) => (
                <div 
                  key={i} 
                  className={`p-2 rounded border text-center font-mono ${
                    pt.breach_critical 
                      ? 'bg-rose-950/70 border-rose-500 text-rose-300' 
                      : pt.breach_warning 
                        ? 'bg-amber-950/70 border-amber-500 text-amber-300' 
                        : 'bg-space-850 border-slate-800 text-slate-300'
                  }`}
                >
                  <span className="text-[9px] text-slate-500 block">{pt.timestamp}</span>
                  <span className="text-sm font-bold block">{pt.predicted_value} {currentMetricConfig.unit}</span>
                  <span className="text-[8px] text-slate-500">[{pt.lower_bound} - {pt.upper_bound}]</span>
                  {(pt.breach_warning || pt.breach_critical) && (
                    <span className="block text-[8px] text-rose-400 font-bold mt-0.5">BREACH RISK</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

      </div>

      {/* Anatomical Silhouette & Risk Breakdown Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <BodySilhouette astronaut={astronaut} vitals={currentVitals} riskData={currentRisk} />
        <RiskIndexBreakdown riskData={currentRisk} />
      </div>

      {/* Dr D Advisor AI Recommendations */}
      <DrDAdvisorCard recommendations={recommendations} />

      {/* Flight Surgeon Medical Notes & Observations */}
      <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
        <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5 text-cyan-400" />
            <h3 className="font-bold text-slate-100 text-sm tracking-wide">
              FLIGHT SURGEON CLINICAL NOTES & COUNTERMEASURES
            </h3>
          </div>
          {(isSurgeon || isAdmin) && (
            <button
              onClick={() => setShowNoteModal(true)}
              className="flex items-center space-x-1 px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-space-950 text-xs font-bold font-mono rounded transition-colors shadow-glow-cyan"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>ADD MEDICAL NOTE</span>
            </button>
          )}
        </div>

        <div className="space-y-3">
          {notes.length === 0 ? (
            <div className="py-6 text-center text-xs text-slate-500 font-mono">No medical notes recorded yet.</div>
          ) : (
            notes.map(note => (
              <div key={note.id} className="p-3.5 bg-space-850 rounded-lg border border-slate-800 text-xs">
                <div className="flex items-center justify-between mb-1.5 font-mono">
                  <div className="flex items-center space-x-2">
                    <span className="font-bold text-cyan-400">{note.author_name}</span>
                    <span className="text-[10px] text-slate-400 bg-space-900 px-1.5 py-0.5 rounded border border-slate-700 uppercase">
                      {note.category}
                    </span>
                  </div>
                  <span className="text-slate-500 text-[10px]">
                    {new Date(note.timestamp).toLocaleString()}
                  </span>
                </div>
                <p className="text-slate-300 leading-relaxed font-sans mt-1">
                  {note.note_text}
                </p>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Add Note Modal */}
      {showNoteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-space-950/80 backdrop-blur-sm">
          <div className="hud-panel w-full max-w-lg rounded-xl p-6 border border-cyan-500/30 bg-space-900 shadow-2xl">
            <h3 className="text-base font-bold text-slate-100 mb-3">Add Clinical Medical Note</h3>
            <form onSubmit={handleAddNote} className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">Category</label>
                <select
                  value={noteCategory}
                  onChange={(e) => setNoteCategory(e.target.value)}
                  className="w-full bg-space-850 border border-slate-700 rounded px-3 py-2 text-xs text-slate-200 outline-none"
                >
                  <option value="CLINICAL_OBSERVATION">Clinical Observation</option>
                  <option value="COUNTERMEASURE">Countermeasure Protocol</option>
                  <option value="PHARMACOLOGY">Pharmacology / Supplement</option>
                  <option value="PROTOCOL_UPDATE">Mission Protocol Update</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">Clinical Assessment</label>
                <textarea
                  rows={4}
                  value={noteText}
                  onChange={(e) => setNoteText(e.target.value)}
                  required
                  placeholder="Record physiological observations, fluid shifts, or exercise adjustments..."
                  className="w-full bg-space-850 border border-slate-700 rounded p-3 text-xs text-slate-100 outline-none focus:border-cyan-400"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowNoteModal(false)}
                  className="px-3 py-1.5 text-xs text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-space-950 font-bold text-xs rounded"
                >
                  Save Note
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
