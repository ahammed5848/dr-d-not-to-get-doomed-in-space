import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  BookOpen, Shield, Flame, Activity, Radio, Moon, Droplets, 
  ExternalLink, Search, Filter, Cpu, Layers, GitBranch, Database,
  CheckCircle2, AlertTriangle, Info, Compass, FileText, ArrowRight
} from 'lucide-react';

export default function NasaResearchPage() {
  const [activeTab, setActiveTab] = useState('hazards');
  // Tabs: 'hazards' | 'risks' | 'evidence' | 'architecture' | 'eimo' | 'conditions' | 'sources'
  
  const [summary, setSummary] = useState(null);
  const [hazards, setHazards] = useState([]);
  const [healthRisks, setHealthRisks] = useState([]);
  const [evidenceReports, setEvidenceReports] = useState([]);
  const [architecture, setArchitecture] = useState(null);
  const [eimo, setEimo] = useState(null);
  const [conditions, setConditions] = useState([]);
  const [sources, setSources] = useState([]);
  const [provenance, setProvenance] = useState([]);

  // Search & Filter state
  const [evidenceSearch, setEvidenceSearch] = useState('');
  const [evidenceCategory, setEvidenceCategory] = useState('');
  const [conditionSearch, setConditionSearch] = useState('');
  const [conditionCategory, setConditionCategory] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAllResearch = async () => {
      try {
        const [
          summaryRes,
          hazardsRes,
          risksRes,
          evidenceRes,
          archRes,
          eimoRes,
          condRes,
          sourcesRes,
          provRes
        ] = await Promise.all([
          axios.get('/api/research/summary'),
          axios.get('/api/research/hazards'),
          axios.get('/api/research/risks'),
          axios.get('/api/research/evidence'),
          axios.get('/api/research/architecture'),
          axios.get('/api/research/eimo'),
          axios.get('/api/research/conditions'),
          axios.get('/api/research/sources'),
          axios.get('/api/research/provenance')
        ]);

        setSummary(summaryRes.data);
        setHazards(hazardsRes.data);
        setHealthRisks(risksRes.data);
        setEvidenceReports(evidenceRes.data);
        setArchitecture(archRes.data);
        setEimo(eimoRes.data);
        setConditions(condRes.data);
        setSources(sourcesRes.data);
        setProvenance(provRes.data);
      } catch (e) {
        console.error("Failed to load NASA research repository", e);
      } finally {
        setLoading(false);
      }
    };

    fetchAllResearch();
  }, []);

  const tabButtons = [
    { id: 'hazards', label: '1. Spaceflight Hazards', count: hazards.length },
    { id: 'risks', label: '2. Health Risks Taxonomy', count: healthRisks.length },
    { id: 'evidence', label: '3. Evidence Reports', count: evidenceReports.length },
    { id: 'architecture', label: '4. Decision Support Architecture', count: 5 },
    { id: 'eimo', label: '5. Earth-Independent Operations (EIMO)', count: 4 },
    { id: 'conditions', label: '6. Exploration Conditions (IMPACT 1.0)', count: conditions.length },
    { id: 'sources', label: '7. Sources & Provenance', count: sources.length },
  ];

  const filteredEvidence = evidenceReports.filter(r => {
    const matchesCat = !evidenceCategory || r.category.toLowerCase().includes(evidenceCategory.toLowerCase());
    const s = evidenceSearch.toLowerCase();
    const matchesSearch = !s || (
      r.title.toLowerCase().includes(s) ||
      r.description.toLowerCase().includes(s) ||
      r.physiological_system.toLowerCase().includes(s) ||
      r.dr_d_feature.toLowerCase().includes(s)
    );
    return matchesCat && matchesSearch;
  });

  const filteredConditions = conditions.filter(c => {
    const matchesCat = !conditionCategory || c.category.toLowerCase().includes(conditionCategory.toLowerCase());
    const s = conditionSearch.toLowerCase();
    const matchesSearch = !s || (
      c.name.toLowerCase().includes(s) ||
      c.system.toLowerCase().includes(s) ||
      c.impact_relevance.toLowerCase().includes(s) ||
      c.telemetry_stream.toLowerCase().includes(s)
    );
    return matchesCat && matchesSearch;
  });

  const filteredRisks = healthRisks.filter(r => {
    return !riskFilter || r.status === riskFilter;
  });

  return (
    <div className="space-y-6 pb-16 font-sans">
      
      {/* Header Banner */}
      <div className="hud-panel rounded-2xl p-6 border border-cyan-500/30 bg-space-900/90 relative corner-accent shadow-glow-cyan">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className="p-1.5 rounded-lg bg-cyan-500/20 text-cyan-400 border border-cyan-500/40">
                <BookOpen className="w-5 h-5" />
              </span>
              <span className="text-xs font-mono font-bold tracking-widest text-cyan-400 uppercase">
                ASTRONAUT HEALTH INTELLIGENCE REPOSITORY
              </span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-cyan-500/40 text-cyan-300 font-semibold">
                NASA RESEARCH & EVIDENCE
              </span>
            </div>
            <h1 className="text-2xl font-black text-slate-100 tracking-tight">
              NASA SCIENTIFIC EVIDENCE & CLINICAL KNOWLEDGE BASE
            </h1>
            <p className="text-xs text-slate-400 mt-1 max-w-3xl leading-relaxed">
              Dr D incorporates verified publications from the NASA Human Research Program (HRP) and Exploration Medical Capability (ExMC). 
              This knowledge layer establishes our spaceflight hazard taxonomy, clinical decision support architecture, and medical condition catalogue.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono">
            <div className="p-2.5 rounded-lg bg-space-850 border border-slate-800 text-center">
              <div className="text-[10px] text-slate-400 uppercase">Hazards</div>
              <div className="text-lg font-bold text-cyan-400">5</div>
              <div className="text-[9px] text-slate-500">Core Categories</div>
            </div>
            <div className="p-2.5 rounded-lg bg-space-850 border border-slate-800 text-center">
              <div className="text-[10px] text-slate-400 uppercase">Health Risks</div>
              <div className="text-lg font-bold text-emerald-400">{healthRisks.length}</div>
              <div className="text-[9px] text-slate-500">Mapped Domains</div>
            </div>
            <div className="p-2.5 rounded-lg bg-space-850 border border-slate-800 text-center">
              <div className="text-[10px] text-slate-400 uppercase">ExMC Conditions</div>
              <div className="text-lg font-bold text-amber-400">119</div>
              <div className="text-[9px] text-slate-500">IMPACT 1.0</div>
            </div>
            <div className="p-2.5 rounded-lg bg-space-850 border border-slate-800 text-center">
              <div className="text-[10px] text-slate-400 uppercase">NASA Sources</div>
              <div className="text-lg font-bold text-purple-400">5</div>
              <div className="text-[9px] text-slate-500">Verified Citations</div>
            </div>
          </div>
        </div>

        {/* Mandatory Transparency Callout */}
        <div className="mt-4 p-3 rounded-lg bg-space-950/80 border border-slate-800 flex items-start space-x-2.5 text-xs font-mono">
          <Info className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />
          <div className="text-slate-300">
            <span className="text-cyan-300 font-bold">DATA PROVENANCE & TRANSPARENCY NOTICE: </span>
            The 5 NASA publications below serve as authoritative scientific research references and technical guidelines. 
            Dr D continuously ingests <span className="text-amber-400 font-bold">synthetic astronaut telemetry</span> and simulated cabin life-support readings. 
            No live NASA biometric API or real human subject telemetry is claimed or integrated.
          </div>
        </div>
      </div>

      {/* Navigation Sub-Tabs */}
      <div className="flex items-center space-x-1.5 overflow-x-auto pb-2 border-b border-slate-800 text-xs font-mono">
        {tabButtons.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-3 py-2 rounded-lg font-semibold whitespace-nowrap transition-all flex items-center space-x-1.5 ${
              activeTab === tab.id
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-glow-cyan'
                : 'bg-space-900/60 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            <span>{tab.label}</span>
            <span className="px-1.5 py-0.2 rounded bg-space-950 text-[10px] text-slate-400 font-bold">
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* TAB 1: 5 CORE SPACEFLIGHT HAZARDS */}
      {activeTab === 'hazards' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-slate-200 font-mono uppercase tracking-wider flex items-center space-x-2">
              <Shield className="w-4 h-4 text-cyan-400" />
              <span>NASA Human Research Program — The 5 Hazards of Human Spaceflight</span>
            </h2>
            <span className="text-[11px] font-mono text-slate-400">Source: NASA HRP (https://www.nasa.gov/hrp/risks/)</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {hazards.map((hazard) => (
              <div 
                key={hazard.id}
                className="hud-panel p-5 rounded-xl border border-slate-800 hover:border-cyan-500/40 transition-all flex flex-col justify-between bg-space-900/80"
              >
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="w-8 h-8 rounded-lg bg-cyan-950/80 border border-cyan-500/40 text-cyan-300 font-mono font-bold flex items-center justify-center text-sm">
                      {hazard.acronym}
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 border border-emerald-500/40 text-emerald-300 font-semibold">
                      MONITORED IN DR D
                    </span>
                  </div>

                  <h3 className="font-bold text-slate-100 text-base mb-2">{hazard.name}</h3>
                  <p className="text-xs text-slate-300 leading-relaxed mb-4">{hazard.description}</p>

                  <div className="space-y-2 mb-4 font-mono text-xs">
                    <div>
                      <span className="text-[10px] uppercase text-slate-400 block font-bold">Target Physiological Systems:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {hazard.physiological_systems.map((sys, idx) => (
                          <span key={idx} className="px-2 py-0.5 rounded bg-space-850 text-slate-300 text-[10px] border border-slate-700">
                            {sys}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div>
                      <span className="text-[10px] uppercase text-slate-400 block font-bold">Dr D Telemetry Features:</span>
                      <ul className="list-disc list-inside text-[11px] text-cyan-300 space-y-0.5 mt-1">
                        {hazard.dr_d_features.map((feat, idx) => (
                          <li key={idx} className="truncate">{feat}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-[11px] font-mono">
                  <span className="text-slate-400 truncate max-w-[180px]">{hazard.hrp_reference}</span>
                  <a
                    href={hazard.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 hover:underline flex items-center space-x-1"
                  >
                    <span>NASA HRP</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: ASTRONAUT HEALTH RISKS TAXONOMY */}
      {activeTab === 'risks' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-sm font-bold text-slate-200 font-mono uppercase tracking-wider flex items-center space-x-2">
                <Activity className="w-4 h-4 text-emerald-400" />
                <span>Astronaut Health Risks Taxonomy & Feature Cross-Correlation</span>
              </h2>
              <p className="text-xs text-slate-400">Distinguishes implemented real-time monitoring from research contexts and future scope.</p>
            </div>

            <div className="flex items-center space-x-2 text-xs font-mono">
              <span className="text-slate-400">Filter Status:</span>
              <select
                value={riskFilter}
                onChange={(e) => setRiskFilter(e.target.value)}
                className="bg-space-850 border border-slate-700 rounded px-2.5 py-1 text-slate-200 outline-none"
              >
                <option value="">All Risk Statuses ({healthRisks.length})</option>
                <option value="MONITORED_IN_DR_D">Monitored in Dr D</option>
                <option value="RESEARCH_REFERENCE_ONLY">Research Reference Only</option>
                <option value="FUTURE_FLIGHT_SCOPE">Future Flight Scope</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredRisks.map((risk) => {
              const isMonitored = risk.status === 'MONITORED_IN_DR_D';
              const isFuture = risk.status === 'FUTURE_FLIGHT_SCOPE';

              return (
                <div key={risk.id} className="hud-panel p-5 rounded-xl border border-slate-800 bg-space-900/80 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold border uppercase ${
                        isMonitored 
                          ? 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300' 
                          : isFuture 
                            ? 'bg-purple-950/80 border-purple-500/40 text-purple-300'
                            : 'bg-cyan-950/80 border-cyan-500/40 text-cyan-300'
                      }`}>
                        {risk.status.replace(/_/g, ' ')}
                      </span>
                      <span className="text-[10px] font-mono text-slate-400">NASA HRP Risk</span>
                    </div>

                    <h3 className="font-bold text-slate-100 text-sm mb-2">{risk.name}</h3>
                    <p className="text-xs text-slate-300 leading-relaxed mb-3">{risk.summary}</p>

                    <div className="p-2.5 rounded bg-space-850 border border-slate-800 text-[11px] font-mono space-y-1.5 mb-3">
                      <div>
                        <span className="text-slate-400 font-semibold block text-[10px]">Associated Dr D Capability:</span>
                        <span className="text-cyan-300">{risk.dr_d_module}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 font-semibold block text-[10px]">Monitored Physiological Metrics:</span>
                        <span className="text-slate-200">{risk.monitored_metrics.join(', ')}</span>
                      </div>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-slate-800/80 text-[10px] font-mono text-slate-400">
                    <span>Evidence: {risk.citation}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 3: SCIENTIFIC EVIDENCE REPORTS */}
      {activeTab === 'evidence' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-sm font-bold text-slate-200 font-mono uppercase tracking-wider flex items-center space-x-2">
                <FileText className="w-4 h-4 text-cyan-400" />
                <span>NASA Human Research Roadmap — Scientific Evidence Reports</span>
              </h2>
              <p className="text-xs text-slate-400">Directly mapped to Dr D's biometric alerting boundaries and anomaly thresholds.</p>
            </div>

            <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
              <div className="relative">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
                <input
                  type="text"
                  placeholder="Search evidence reports..."
                  value={evidenceSearch}
                  onChange={(e) => setEvidenceSearch(e.target.value)}
                  className="pl-8 pr-3 py-1 bg-space-850 border border-slate-700 rounded text-slate-200 text-xs outline-none focus:border-cyan-400"
                />
              </div>

              <select
                value={evidenceCategory}
                onChange={(e) => setEvidenceCategory(e.target.value)}
                className="bg-space-850 border border-slate-700 rounded px-2.5 py-1 text-slate-200 outline-none"
              >
                <option value="">All Categories</option>
                <option value="Environmental">Environmental & Life Support</option>
                <option value="Cardiovascular">Cardiovascular Autonomic</option>
                <option value="Behavioral">Behavioral Health (Sleep)</option>
                <option value="Radiation">Space Radiation</option>
                <option value="Sensory">Cross-Cutting (SANS)</option>
                <option value="Clinical">Exploration CDSS</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredEvidence.map((ev, idx) => (
              <div key={idx} className="hud-panel p-5 rounded-xl border border-slate-800 bg-space-900/80 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-850 border border-slate-700 text-slate-300 font-bold uppercase">
                      {ev.category}
                    </span>
                    <span className="text-[10px] font-mono text-cyan-400">Evidence Report</span>
                  </div>

                  <h3 className="font-bold text-slate-100 text-sm mb-2">{ev.title}</h3>
                  <p className="text-xs text-slate-300 leading-relaxed mb-4">{ev.description}</p>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] font-mono mb-3">
                    <div className="p-2 rounded bg-space-850 border border-slate-800">
                      <span className="text-[10px] uppercase text-slate-400 block font-bold">Target System</span>
                      <span className="text-slate-200">{ev.physiological_system}</span>
                    </div>
                    <div className="p-2 rounded bg-space-850 border border-slate-800">
                      <span className="text-[10px] uppercase text-cyan-400 block font-bold">Dr D Implementation</span>
                      <span className="text-cyan-200">{ev.dr_d_feature}</span>
                    </div>
                  </div>
                </div>

                <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-[11px] font-mono">
                  <span className="text-slate-400">{ev.nasa_source}</span>
                  <a
                    href={ev.official_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-cyan-400 hover:underline flex items-center space-x-1"
                  >
                    <span>Read Evidence</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 4: CLINICAL DECISION SUPPORT SYSTEM ARCHITECTURE (HRP-48032 REV. B) */}
      {activeTab === 'architecture' && architecture && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-sm font-bold text-slate-200 font-mono uppercase tracking-wider flex items-center space-x-2">
                <Layers className="w-4 h-4 text-purple-400" />
                <span>NASA ExMC — Clinical Decision Support System Architecture (HRP-48032 Rev. B)</span>
              </h2>
              <p className="text-xs text-slate-400">Comparing Dr D's 4-tier decoupled implementation against NASA ExMC architectural recommendations.</p>
            </div>
            <a
              href={architecture.official_url}
              target="_blank"
              rel="noreferrer"
              className="px-3 py-1 rounded bg-space-850 hover:bg-space-800 border border-purple-500/40 text-purple-300 font-mono text-xs flex items-center space-x-1"
            >
              <span>{architecture.document_id}</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>

          <div className="space-y-3">
            {architecture.core_principles.map((p, idx) => (
              <div key={idx} className="hud-panel p-5 rounded-xl border border-slate-800 bg-space-900/80">
                <div className="flex items-center space-x-3 mb-3">
                  <span className="w-7 h-7 rounded-lg bg-purple-950 border border-purple-500/40 text-purple-300 font-mono font-bold flex items-center justify-center text-xs">
                    0{idx + 1}
                  </span>
                  <h3 className="font-bold text-slate-100 text-sm tracking-wide">{p.layer}</h3>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                  <div className="p-3 rounded-lg bg-space-950 border border-slate-800">
                    <span className="text-[10px] uppercase font-bold text-amber-400 block mb-1">
                      NASA ExMC HRP-48032 Recommendation:
                    </span>
                    <p className="text-slate-300 leading-relaxed">{p.nasa_recommendation}</p>
                  </div>

                  <div className="p-3 rounded-lg bg-space-950 border border-cyan-500/30">
                    <span className="text-[10px] uppercase font-bold text-cyan-400 block mb-1">
                      Dr D Technical Implementation:
                    </span>
                    <p className="text-cyan-100 leading-relaxed">{p.dr_d_implementation}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 rounded-xl bg-space-850 border border-slate-800 text-xs font-mono text-slate-400">
            <span className="text-slate-300 font-bold uppercase block mb-1">Architecture Alignment Disclaimer:</span>
            {architecture.disclaimer}
          </div>
        </div>
      )}

      {/* TAB 5: EARTH-INDEPENDENT MEDICAL OPERATIONS (EIMO, 20240001402) */}
      {activeTab === 'eimo' && eimo && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-sm font-bold text-slate-200 font-mono uppercase tracking-wider flex items-center space-x-2">
                <Compass className="w-4 h-4 text-cyan-400" />
                <span>NASA ExMC — Earth-Independent Medical Operations (EIMO) Concept of Operations</span>
              </h2>
              <p className="text-xs text-slate-400">Guiding clinical autonomy workflows during high interplanetary communication delays.</p>
            </div>
            <a
              href={eimo.official_url}
              target="_blank"
              rel="noreferrer"
              className="px-3 py-1 rounded bg-space-850 hover:bg-space-800 border border-cyan-500/40 text-cyan-300 font-mono text-xs flex items-center space-x-1"
            >
              <span>{eimo.document_id}</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {eimo.operational_pillars.map((pil, idx) => (
              <div key={idx} className="hud-panel p-5 rounded-xl border border-slate-800 bg-space-900/80 flex flex-col justify-between">
                <div>
                  <div className="flex items-center space-x-2.5 mb-2">
                    <span className="w-6 h-6 rounded bg-cyan-950 border border-cyan-500/40 text-cyan-300 font-mono font-bold flex items-center justify-center text-xs">
                      P{idx + 1}
                    </span>
                    <h3 className="font-bold text-slate-100 text-sm">{pil.pillar}</h3>
                  </div>

                  <div className="space-y-3 mt-3 text-xs font-mono">
                    <div className="p-3 rounded bg-space-950 border border-slate-800">
                      <span className="text-[10px] uppercase font-bold text-amber-400 block mb-1">
                        NASA EIMO ConOps Principle:
                      </span>
                      <p className="text-slate-300 leading-relaxed">{pil.eimo_concept}</p>
                    </div>

                    <div className="p-3 rounded bg-space-950 border border-cyan-500/30">
                      <span className="text-[10px] uppercase font-bold text-cyan-400 block mb-1">
                        Dr D Operational Mapping:
                      </span>
                      <p className="text-cyan-100 leading-relaxed">{pil.dr_d_alignment}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 6: EXPLORATION MEDICAL CONDITIONS (IMPACT 1.0) */}
      {activeTab === 'conditions' && (
        <div className="space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <h2 className="text-sm font-bold text-slate-200 font-mono uppercase tracking-wider flex items-center space-x-2">
                <Database className="w-4 h-4 text-amber-400" />
                <span>NASA ExMC Exploration Medical Condition List (IMPACT 1.0, HRP-48036 Rev. B)</span>
              </h2>
              <p className="text-xs text-slate-400">Structured reference catalogue mapping exploration medical conditions to Dr D telemetry streams.</p>
            </div>

            <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
              <div className="relative">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-2.5 top-2.5" />
                <input
                  type="text"
                  placeholder="Search conditions..."
                  value={conditionSearch}
                  onChange={(e) => setConditionSearch(e.target.value)}
                  className="pl-8 pr-3 py-1 bg-space-850 border border-slate-700 rounded text-slate-200 text-xs outline-none focus:border-cyan-400"
                />
              </div>

              <select
                value={conditionCategory}
                onChange={(e) => setConditionCategory(e.target.value)}
                className="bg-space-850 border border-slate-700 rounded px-2.5 py-1 text-slate-200 outline-none"
              >
                <option value="">All Medical Categories</option>
                <option value="Cardiovascular">Cardiovascular</option>
                <option value="Respiratory">Respiratory</option>
                <option value="Environmental">Environmental & Toxic</option>
                <option value="Neuro">Neuro-Psychiatric / Sensory</option>
                <option value="Metabolic">Metabolic & Hemodynamic</option>
                <option value="Musculoskeletal">Musculoskeletal</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredConditions.map((cond) => {
              const isDirect = cond.dr_d_monitoring === 'MONITORED_DIRECTLY';

              return (
                <div key={cond.condition_id} className="hud-panel p-5 rounded-xl border border-slate-800 bg-space-900/80 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-850 border border-slate-700 text-slate-300 font-bold">
                        {cond.condition_id}
                      </span>
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold uppercase border ${
                        isDirect 
                          ? 'bg-emerald-950/80 border-emerald-500/40 text-emerald-300' 
                          : 'bg-cyan-950/80 border-cyan-500/40 text-cyan-300'
                      }`}>
                        {cond.dr_d_monitoring.replace(/_/g, ' ')}
                      </span>
                    </div>

                    <h3 className="font-bold text-slate-100 text-sm mb-1">{cond.name}</h3>
                    <div className="text-[10px] font-mono text-cyan-400 uppercase mb-2">{cond.category} • {cond.system}</div>

                    <p className="text-xs text-slate-300 leading-relaxed mb-3">{cond.impact_relevance}</p>

                    <div className="p-2.5 rounded bg-space-850 border border-slate-800 text-[11px] font-mono space-y-1 mb-3">
                      <span className="text-[10px] text-slate-400 font-bold uppercase block">Associated Telemetry Channel:</span>
                      <span className="text-cyan-300 font-semibold">{cond.telemetry_stream}</span>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-slate-800/80 text-[10px] font-mono text-slate-400">
                    <span className="truncate block">{cond.evidence_source}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 7: NASA SOURCE LIBRARY & DATA PROVENANCE */}
      {activeTab === 'sources' && (
        <div className="space-y-6">
          
          {/* 5 Official Sources */}
          <div>
            <h2 className="text-sm font-bold text-slate-200 font-mono uppercase tracking-wider mb-3 flex items-center space-x-2">
              <BookOpen className="w-4 h-4 text-purple-400" />
              <span>The 5 Official NASA Scientific & Technical Resources Integrated</span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {sources.map((src) => (
                <div key={src.resource_number} className="hud-panel p-5 rounded-xl border border-slate-800 bg-space-900/80 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="px-2 py-0.5 rounded bg-purple-950 border border-purple-500/40 text-purple-300 font-mono text-[10px] font-bold">
                        NASA RESOURCE {src.resource_number}
                      </span>
                      <span className="px-2 py-0.5 rounded bg-space-850 border border-slate-700 text-cyan-300 font-mono text-[10px] font-bold">
                        {src.provenance_tag}
                      </span>
                    </div>

                    <h3 className="font-bold text-slate-100 text-sm mb-1">{src.title}</h3>
                    <div className="text-[10px] font-mono text-slate-400 mb-3">{src.authoring_organization} • {src.document_id}</div>

                    <div className="p-3 rounded bg-space-950 border border-slate-800 text-xs font-mono text-slate-300 mb-3">
                      <span className="text-[10px] text-cyan-400 font-bold uppercase block mb-1">Role in Dr D System:</span>
                      <p className="leading-relaxed">{src.role_in_dr_d}</p>
                    </div>
                  </div>

                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs font-mono">
                    <span className="text-[10px] text-slate-400">{src.data_type}</span>
                    <a
                      href={src.official_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-cyan-400 hover:underline flex items-center space-x-1"
                    >
                      <span>Official NASA Link</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Full Data Provenance Classification Matrix (Part 7) */}
          <div className="hud-panel p-5 rounded-xl border border-slate-800 bg-space-900/80">
            <div className="flex items-center space-x-2 mb-3">
              <Database className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-bold text-slate-100 font-mono uppercase tracking-wider">
                Comprehensive Data Provenance & Transparency Classification Matrix
              </h3>
            </div>
            <p className="text-xs text-slate-400 mb-4 leading-relaxed font-mono">
              To adhere strictly to NASA Space Apps Challenge research guidelines and prevent misconceptions, 
              every information stream inside Dr D is classified into one of the five provenance categories below:
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {provenance.map((item, idx) => (
                <div key={idx} className="p-3.5 rounded-lg bg-space-950 border border-slate-800 text-xs font-mono flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="px-2 py-0.5 rounded font-bold text-[10px] bg-space-900 border border-slate-700 text-amber-400">
                        {item.badge_label}
                      </span>
                      <span className="text-[10px] text-slate-500 font-bold">Cat 0{idx + 1}</span>
                    </div>

                    <h4 className="font-bold text-slate-200 text-sm mb-1">{item.classification}</h4>
                    <div className="text-[10px] text-cyan-400 mb-2">{item.source_name}</div>

                    <p className="text-[11px] text-slate-300 leading-relaxed mb-3">{item.purpose}</p>

                    <div className="p-2 rounded bg-space-900 border border-slate-800 text-[10px] space-y-1 mb-2">
                      <div><span className="text-slate-400 font-bold">Data Nature: </span><span className="text-slate-200">{item.provenance_nature}</span></div>
                      <div><span className="text-slate-400 font-bold">Delivery: </span><span className="text-slate-300">{item.integration_method}</span></div>
                      <div><span className="text-slate-400 font-bold">License: </span><span className="text-slate-300">{item.license_terms}</span></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      )}

    </div>
  );
}
