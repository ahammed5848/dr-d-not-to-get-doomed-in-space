import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useLiveTelemetry } from '../context/WebSocketContext';
import { Sliders, Save, CheckCircle2, ShieldAlert, Cpu, RotateCcw } from 'lucide-react';

export default function AdminThresholdsPage() {
  const { isAdmin } = useAuth();
  const { simulationSpeed, setSpeed, resetSimulation, isConnected } = useLiveTelemetry();
  const [thresholds, setThresholds] = useState([]);
  const [editedValues, setEditedValues] = useState({});
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchThresholds = async () => {
    try {
      const res = await axios.get('/api/thresholds');
      setThresholds(res.data);
      const initialMap = {};
      res.data.forEach(t => {
        initialMap[t.metric] = {
          warning_low: t.warning_low ?? '',
          warning_high: t.warning_high ?? '',
          critical_low: t.critical_low ?? '',
          critical_high: t.critical_high ?? '',
        };
      });
      setEditedValues(initialMap);
    } catch (e) {
      console.error("Failed to load thresholds", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchThresholds();
  }, []);

  const handleFieldChange = (metric, field, value) => {
    setEditedValues(prev => ({
      ...prev,
      [metric]: {
        ...prev[metric],
        [field]: value
      }
    }));
  };

  const handleSaveThreshold = async (metric) => {
    try {
      const payload = {
        warning_low: editedValues[metric].warning_low !== '' ? parseFloat(editedValues[metric].warning_low) : null,
        warning_high: editedValues[metric].warning_high !== '' ? parseFloat(editedValues[metric].warning_high) : null,
        critical_low: editedValues[metric].critical_low !== '' ? parseFloat(editedValues[metric].critical_low) : null,
        critical_high: editedValues[metric].critical_high !== '' ? parseFloat(editedValues[metric].critical_high) : null,
      };
      await axios.put(`/api/thresholds/${metric}`, payload);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 3000);
      fetchThresholds();
    } catch (e) {
      console.error("Failed to update threshold", e);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="hud-panel rounded-2xl p-5 border border-cyan-500/25 bg-space-900/90 relative corner-accent">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2 mb-1">
              <Sliders className="w-5 h-5 text-cyan-400" />
              <h1 className="text-xl font-black text-slate-100 tracking-tight">
                ADMINISTRATION & THRESHOLD CALIBRATION MATRIX
              </h1>
            </div>
            <p className="text-xs text-slate-400">
              Configure Normal, Warning, and Critical boundaries for autonomic vitals & spacecraft cabin parameters.
            </p>
          </div>

          {savedSuccess && (
            <div className="px-3 py-1.5 bg-emerald-950/80 border border-emerald-500/40 rounded text-emerald-300 text-xs font-mono flex items-center space-x-1.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Threshold successfully updated!</span>
            </div>
          )}
        </div>
      </div>

      {/* Thresholds Table */}
      <div className="hud-panel rounded-xl overflow-hidden border border-cyan-500/20">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-space-850 border-b border-slate-800 text-slate-400 uppercase text-[10px]">
              <tr>
                <th className="px-4 py-3">Metric Name</th>
                <th className="px-4 py-3">Unit</th>
                <th className="px-4 py-3">Crit Low</th>
                <th className="px-4 py-3">Warn Low</th>
                <th className="px-4 py-3">Warn High</th>
                <th className="px-4 py-3">Crit High</th>
                <th className="px-4 py-3">Clinical Context</th>
                <th className="px-4 py-3 text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80">
              {loading ? (
                <tr>
                  <td colSpan={8} className="p-8 text-center text-slate-400">Loading thresholds...</td>
                </tr>
              ) : (
                thresholds.map(t => {
                  const ev = editedValues[t.metric] || {};
                  return (
                    <tr key={t.id} className="hover:bg-space-850/50 transition-colors">
                      <td className="px-4 py-3 font-semibold text-slate-200">
                        {t.name}
                        <span className="block text-[10px] text-slate-500 font-normal">{t.metric}</span>
                      </td>

                      <td className="px-4 py-3 text-cyan-400 font-bold">
                        {t.unit}
                      </td>

                      {/* Crit Low */}
                      <td className="px-4 py-3">
                        <input
                          type="number"
                          step="any"
                          value={ev.critical_low ?? ''}
                          disabled={!isAdmin}
                          onChange={(e) => handleFieldChange(t.metric, 'critical_low', e.target.value)}
                          className="w-20 bg-space-900 border border-slate-700 rounded px-2 py-1 text-rose-400 focus:border-rose-400 outline-none text-xs"
                          placeholder="—"
                        />
                      </td>

                      {/* Warn Low */}
                      <td className="px-4 py-3">
                        <input
                          type="number"
                          step="any"
                          value={ev.warning_low ?? ''}
                          disabled={!isAdmin}
                          onChange={(e) => handleFieldChange(t.metric, 'warning_low', e.target.value)}
                          className="w-20 bg-space-900 border border-slate-700 rounded px-2 py-1 text-amber-400 focus:border-amber-400 outline-none text-xs"
                          placeholder="—"
                        />
                      </td>

                      {/* Warn High */}
                      <td className="px-4 py-3">
                        <input
                          type="number"
                          step="any"
                          value={ev.warning_high ?? ''}
                          disabled={!isAdmin}
                          onChange={(e) => handleFieldChange(t.metric, 'warning_high', e.target.value)}
                          className="w-20 bg-space-900 border border-slate-700 rounded px-2 py-1 text-amber-400 focus:border-amber-400 outline-none text-xs"
                          placeholder="—"
                        />
                      </td>

                      {/* Crit High */}
                      <td className="px-4 py-3">
                        <input
                          type="number"
                          step="any"
                          value={ev.critical_high ?? ''}
                          disabled={!isAdmin}
                          onChange={(e) => handleFieldChange(t.metric, 'critical_high', e.target.value)}
                          className="w-20 bg-space-900 border border-slate-700 rounded px-2 py-1 text-rose-400 focus:border-rose-400 outline-none text-xs"
                          placeholder="—"
                        />
                      </td>

                      <td className="px-4 py-3 text-slate-400 text-[11px] font-sans max-w-xs truncate" title={t.description}>
                        {t.description}
                      </td>

                      <td className="px-4 py-3 text-right">
                        {isAdmin ? (
                          <button
                            onClick={() => handleSaveThreshold(t.metric)}
                            className="px-3 py-1 bg-cyan-600 hover:bg-cyan-500 text-space-950 font-bold text-[10px] rounded transition-colors"
                          >
                            Save
                          </button>
                        ) : (
                          <span className="text-slate-500 text-[10px]">Locked</span>
                        )}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
