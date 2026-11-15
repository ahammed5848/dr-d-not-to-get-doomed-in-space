import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { 
  AlertTriangle, ShieldAlert, CheckCircle2, Filter, 
  RotateCcw, Search, MessageSquare, Clock, User, BookOpen, ExternalLink, Info, X
} from 'lucide-react';

export default function AlertsCenterPage() {
  const { isSurgeon, isAdmin, user } = useAuth();
  const [alerts, setAlerts] = useState([]);
  const [astronauts, setAstronauts] = useState([]);
  const [selectedAstro, setSelectedAstro] = useState('');
  const [selectedSeverity, setSelectedSeverity] = useState('');
  const [selectedStatus, setSelectedStatus] = useState('');
  const [loading, setLoading] = useState(true);

  // Acknowledge/Resolve Modal state
  const [activeModalAlert, setActiveModalAlert] = useState(null);
  const [actionType, setActionType] = useState('ACKNOWLEDGED');
  const [actionNote, setActionNote] = useState('');

  // Research Context Modal state
  const [activeResearchModal, setActiveResearchModal] = useState(null);

  const fetchAlerts = async () => {
    try {
      let url = '/api/alerts?limit=100';
      if (selectedAstro) url += `&astronaut_id=${selectedAstro}`;
      if (selectedSeverity) url += `&severity=${selectedSeverity}`;
      if (selectedStatus) url += `&status=${selectedStatus}`;

      const [alertsRes, astrosRes] = await Promise.all([
        axios.get(url),
        axios.get('/api/astronauts')
      ]);
      setAlerts(alertsRes.data);
      setAstronauts(astrosRes.data);
    } catch (e) {
      console.error("Failed to fetch alerts", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
    const interval = setInterval(fetchAlerts, 4000);
    return () => clearInterval(interval);
  }, [selectedAstro, selectedSeverity, selectedStatus]);

  const handleUpdateStatus = async (e) => {
    e.preventDefault();
    if (!activeModalAlert) return;
    try {
      await axios.patch(`/api/alerts/${activeModalAlert.id}`, {
        status: actionType,
        notes: actionNote
      });
      setActiveModalAlert(null);
      setActionNote('');
      fetchAlerts();
    } catch (e) {
      console.error("Failed to update alert", e);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      
      {/* Page Header */}
      <div className="hud-panel rounded-2xl p-5 border border-cyan-500/25 bg-space-900/90 relative corner-accent">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-1">
              <AlertTriangle className="w-5 h-5 text-amber-400" />
              <h1 className="text-xl font-black text-slate-100 tracking-tight">
                MISSION ALERTS & INCIDENT MANAGEMENT CENTER
              </h1>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-amber-500/40 text-amber-400 font-bold">
                SIMULATED TELEMETRY
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Audit trail of threshold breaches, acute physiological incidents, and flight surgeon interventions mapped to NASA Human Research Program hazards.
            </p>
          </div>

          <div className="flex items-center space-x-3 text-xs font-mono">
            <span className="px-2.5 py-1 rounded bg-rose-950/80 border border-rose-500/40 text-rose-300">
              {alerts.filter(a => a.status === 'ACTIVE' && a.threshold_level === 'CRITICAL').length} Critical
            </span>
            <span className="px-2.5 py-1 rounded bg-amber-950/80 border border-amber-500/40 text-amber-300">
              {alerts.filter(a => a.status === 'ACTIVE' && a.threshold_level === 'WARNING').length} Warnings
            </span>
            <span className="px-2.5 py-1 rounded bg-slate-800 text-slate-400">
              {alerts.length} Total
            </span>
          </div>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="p-3.5 bg-space-900/80 rounded-xl border border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
        <div className="flex items-center space-x-2 text-slate-400">
          <Filter className="w-4 h-4 text-cyan-400" />
          <span className="font-semibold text-slate-200">Filter Incidents:</span>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Astronaut filter */}
          <div>
            <select
              value={selectedAstro}
              onChange={(e) => setSelectedAstro(e.target.value)}
              className="bg-space-850 border border-slate-700 rounded px-2.5 py-1 text-slate-200 outline-none"
            >
              <option value="">All Crew Members</option>
              {astronauts.map(a => (
                <option key={a.id} value={a.id}>{a.callsign} — {a.name}</option>
              ))}
            </select>
          </div>

          {/* Severity filter */}
          <div>
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="bg-space-850 border border-slate-700 rounded px-2.5 py-1 text-slate-200 outline-none"
            >
              <option value="">All Severities</option>
              <option value="CRITICAL">Critical Only</option>
              <option value="WARNING">Warning Only</option>
            </select>
          </div>

          {/* Status filter */}
          <div>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="bg-space-850 border border-slate-700 rounded px-2.5 py-1 text-slate-200 outline-none"
            >
              <option value="">All Statuses</option>
              <option value="ACTIVE">ACTIVE</option>
              <option value="ACKNOWLEDGED">ACKNOWLEDGED</option>
              <option value="RESOLVED">RESOLVED</option>
            </select>
          </div>

          {(selectedAstro || selectedSeverity || selectedStatus) && (
            <button
              onClick={() => { setSelectedAstro(''); setSelectedSeverity(''); setSelectedStatus(''); }}
              className="px-2 py-1 bg-space-800 text-slate-400 hover:text-white rounded flex items-center space-x-1"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Clear</span>
            </button>
          )}
        </div>
      </div>

      {/* Alerts Table */}
      <div className="hud-panel rounded-xl overflow-hidden border border-cyan-500/20">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-space-850 border-b border-slate-800 text-slate-400 uppercase text-[10px]">
              <tr>
                <th className="px-4 py-3">Timestamp (UTC)</th>
                <th className="px-4 py-3">Severity</th>
                <th className="px-4 py-3">Target Subject</th>
                <th className="px-4 py-3">Metric</th>
                <th className="px-4 py-3">Value</th>
                <th className="px-4 py-3">Clinical Action Protocol</th>
                <th className="px-4 py-3">NASA Research Context</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/80">
              {loading ? (
                <tr>
                  <td colSpan={9} className="p-8 text-center text-slate-400">Loading alerts feed...</td>
                </tr>
              ) : alerts.length === 0 ? (
                <tr>
                  <td colSpan={9} className="p-8 text-center text-slate-500">No matching alerts found for specified filter criteria.</td>
                </tr>
              ) : (
                alerts.map(alert => {
                  const isCrit = alert.threshold_level === 'CRITICAL';
                  const ctx = alert.research_context;
                  return (
                    <tr key={alert.id} className="hover:bg-space-850/50 transition-colors">
                      <td className="px-4 py-3 text-slate-400 whitespace-nowrap">
                        {new Date(alert.timestamp).toLocaleTimeString()}
                      </td>

                      <td className="px-4 py-3">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${
                          isCrit ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' : 'bg-amber-500/20 text-amber-300 border-amber-500/40'
                        }`}>
                          {alert.threshold_level}
                        </span>
                      </td>

                      <td className="px-4 py-3 font-semibold text-slate-200">
                        {alert.astronaut_callsign ? (
                          <span className="text-cyan-400">[{alert.astronaut_callsign}] {alert.astronaut_name}</span>
                        ) : (
                          <span className="text-slate-400">[CABIN] Environmental</span>
                        )}
                      </td>

                      <td className="px-4 py-3 text-slate-300 uppercase">
                        {alert.metric}
                      </td>

                      <td className="px-4 py-3 font-bold text-slate-100">
                        {alert.value.toFixed(1)}
                      </td>

                      <td className="px-4 py-3 text-slate-300 max-w-xs truncate" title={alert.suggested_action}>
                        {alert.suggested_action}
                      </td>

                      {/* NASA Research Context Column */}
                      <td className="px-4 py-3 whitespace-nowrap">
                        {ctx ? (
                          <button
                            onClick={() => setActiveResearchModal({ alert, ctx })}
                            className="flex items-center space-x-1 px-2 py-0.5 rounded bg-space-800 hover:bg-space-700 text-cyan-300 hover:text-cyan-200 border border-cyan-500/30 text-[10px]"
                          >
                            <BookOpen className="w-3 h-3 text-cyan-400" />
                            <span className="truncate max-w-[110px]">{ctx.nasa_hazard}</span>
                          </button>
                        ) : (
                          <span className="text-slate-500 text-[10px]">Reference N/A</span>
                        )}
                      </td>

                      <td className="px-4 py-3 whitespace-nowrap">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          alert.status === 'ACTIVE' 
                            ? 'bg-rose-950 text-rose-400 border border-rose-800' 
                            : alert.status === 'ACKNOWLEDGED' 
                              ? 'bg-amber-950 text-amber-300 border border-amber-800' 
                              : 'bg-emerald-950 text-emerald-400 border border-emerald-800'
                        }`}>
                          {alert.status}
                        </span>
                      </td>

                      <td className="px-4 py-3 text-right whitespace-nowrap">
                        {(isSurgeon || isAdmin) ? (
                          <div className="flex items-center justify-end space-x-1.5">
                            {alert.status === 'ACTIVE' && (
                              <button
                                onClick={() => { setActiveModalAlert(alert); setActionType('ACKNOWLEDGED'); }}
                                className="px-2 py-1 bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 rounded border border-amber-500/30 text-[10px] font-bold"
                              >
                                Ack
                              </button>
                            )}
                            {alert.status !== 'RESOLVED' && (
                              <button
                                onClick={() => { setActiveModalAlert(alert); setActionType('RESOLVED'); }}
                                className="px-2 py-1 bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 rounded border border-emerald-500/30 text-[10px] font-bold"
                              >
                                Resolve
                              </button>
                            )}
                          </div>
                        ) : (
                          <span className="text-slate-500 text-[10px]">Read-only</span>
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

      {/* Dedicated NASA Research Context Modal */}
      {activeResearchModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-space-950/80 backdrop-blur-sm animate-fade-in">
          <div className="hud-panel w-full max-w-xl rounded-xl p-6 border border-cyan-500/40 bg-space-900 shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
              <div className="flex items-center space-x-2">
                <BookOpen className="w-5 h-5 text-cyan-400" />
                <h3 className="text-base font-bold text-slate-100">
                  NASA Research Context & Clinical Evidence
                </h3>
              </div>
              <button
                onClick={() => setActiveResearchModal(null)}
                className="p-1 rounded text-slate-400 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 font-mono text-xs">
              <div className="p-3 bg-space-950 rounded-lg border border-cyan-500/30">
                <div className="text-[10px] text-cyan-400 font-bold uppercase mb-1">Detected Simulated Incident</div>
                <div className="text-slate-100 font-semibold text-sm">{activeResearchModal.ctx.event_name}</div>
                <div className="text-slate-400 text-xs mt-1">{activeResearchModal.alert.message}</div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-space-950 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-slate-400 uppercase font-bold">NASA Spaceflight Hazard</div>
                  <div className="text-slate-200 font-semibold mt-0.5">{activeResearchModal.ctx.nasa_hazard}</div>
                </div>
                <div className="p-3 bg-space-950 rounded-lg border border-slate-800">
                  <div className="text-[10px] text-slate-400 uppercase font-bold">Data Provenance</div>
                  <div className="text-amber-400 font-semibold mt-0.5">{activeResearchModal.ctx.data_source}</div>
                </div>
              </div>

              <div className="p-3 bg-space-950 rounded-lg border border-amber-500/30">
                <div className="text-[10px] text-amber-400 font-bold uppercase mb-1">Potential Health Implications</div>
                <div className="text-slate-300 text-xs leading-relaxed">{activeResearchModal.ctx.potential_implications}</div>
              </div>

              <div className="p-3 bg-space-950 rounded-lg border border-purple-500/30">
                <div className="text-[10px] text-purple-300 font-bold uppercase mb-1">Clinical Evidence & Scientific Reference</div>
                <div className="text-slate-300 text-xs">{activeResearchModal.ctx.research_reference}</div>
                <p className="text-[11px] text-slate-400 mt-1">{activeResearchModal.ctx.clinical_evidence_summary}</p>
                {activeResearchModal.ctx.official_url && (
                  <div className="mt-2 pt-1 border-t border-slate-800 flex justify-end">
                    <a
                      href={activeResearchModal.ctx.official_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-cyan-400 hover:underline flex items-center space-x-1 text-[11px]"
                    >
                      <span>View Official NASA HRP Publication</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  </div>
                )}
              </div>
            </div>

            <div className="mt-5 pt-3 border-t border-slate-800 flex justify-end">
              <button
                onClick={() => setActiveResearchModal(null)}
                className="px-4 py-1.5 bg-space-800 hover:bg-space-700 text-slate-200 rounded font-mono text-xs font-semibold"
              >
                Close Reference
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Acknowledge / Resolve Modal */}
      {activeModalAlert && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-space-950/80 backdrop-blur-sm">
          <div className="hud-panel w-full max-w-md rounded-xl p-5 border border-cyan-500/30 bg-space-900 shadow-2xl">
            <h3 className="text-base font-bold text-slate-100 mb-2">
              {actionType === 'RESOLVED' ? 'Resolve Medical Incident' : 'Acknowledge Telemetry Alert'}
            </h3>
            <p className="text-xs text-slate-400 mb-2 font-mono">
              Alert: {activeModalAlert.message}
            </p>
            {activeModalAlert.research_context && (
              <div className="mb-4 p-2.5 bg-space-950 rounded border border-cyan-500/30 text-[11px] font-mono text-cyan-300">
                <span className="font-bold text-slate-200">NASA Hazard: </span>
                {activeModalAlert.research_context.nasa_hazard}
              </div>
            )}

            <form onSubmit={handleUpdateStatus} className="space-y-4">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">
                  Flight Surgeon Medical Action Notes
                </label>
                <textarea
                  rows={3}
                  value={actionNote}
                  onChange={(e) => setActionNote(e.target.value)}
                  placeholder="Record intervention taken, e.g. oxygen administered, bed rest commanded, scrubber activated..."
                  className="w-full bg-space-850 border border-slate-700 rounded p-2.5 text-xs text-slate-100 outline-none focus:border-cyan-400"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setActiveModalAlert(null)}
                  className="px-3 py-1.5 text-xs text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className={`px-4 py-1.5 font-bold text-xs rounded text-space-950 ${
                    actionType === 'RESOLVED' ? 'bg-emerald-400 hover:bg-emerald-300' : 'bg-amber-400 hover:bg-amber-300'
                  }`}
                >
                  Confirm {actionType}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
