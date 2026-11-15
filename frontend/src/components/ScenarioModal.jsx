import React, { useState } from 'react';
import axios from 'axios';
import { useLiveTelemetry } from '../context/WebSocketContext';
import { 
  X, AlertTriangle, Activity, Zap, Radio, Moon, Droplets, 
  Cpu, RotateCcw, ShieldCheck, Flame, CheckCircle, Upload, FileSpreadsheet,
  BookOpen, ChevronDown, ChevronUp, ExternalLink, Info
} from 'lucide-react';

export default function ScenarioModal({ onClose }) {
  const { triggerScenario, resetSimulation, activeScenarios, simulationSpeed, setSpeed } = useLiveTelemetry();
  const [activeTab, setActiveTab] = useState('scenarios'); // 'scenarios' | 'csv'
  const [selectedAstro, setSelectedAstro] = useState(1);
  const [severity, setSeverity] = useState('moderate');
  const [lastActionStatus, setLastActionStatus] = useState('');
  const [expandedResearch, setExpandedResearch] = useState({});
  
  // CSV Import State
  const [csvUploading, setCsvUploading] = useState(false);

  const toggleResearch = (id) => {
    setExpandedResearch(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const scenarios = [
    {
      id: 'co2_spike',
      title: 'Cabin CO2 Spike',
      category: 'Environmental Life Support',
      icon: Flame,
      color: 'text-amber-400 border-amber-500/30 bg-amber-500/10',
      description: 'CO2 removal scrubber failure elevates cabin CO2 to 2100 ppm, inducing crew headache, compensatory tachycardia, and hypoxia risk.',
      target: 'Spacecraft Cabin / All Crew',
      nasaHazard: 'Hostile and Closed Environments',
      researchReference: 'NASA HRP Evidence Report on Hostile Spacecraft Cabin Atmosphere; NASA STD-3001',
      implications: 'Elevated CO2 impairs cognitive executive function, causes cerebral vasodilation, and drives compensatory hyperventilation in microgravity.',
      officialUrl: 'https://humanresearchroadmap.nasa.gov/evidence/'
    },
    {
      id: 'eva_cardiac_stress',
      title: 'EVA Cardiac Strain & Tachycardia',
      category: 'Cardiovascular Emergency',
      icon: Activity,
      color: 'text-rose-400 border-rose-500/30 bg-rose-500/10',
      description: 'High metabolic exertion during spacewalk pushes heart rate to 142 bpm, blood pressure to 154/96, with autonomic fatigue.',
      target: 'Specific Astronaut (Elena / Sarah)',
      nasaHazard: 'Altered Gravity Fields & Hostile Environments',
      researchReference: 'NASA HRP Cardiovascular Evidence Report; Human Factors in EVA Workload',
      implications: 'Rigid pressurized spacesuits demand extreme caloric expenditure (>300 kcal/hr), elevating risks of heat strain and acute cardiac exhaustion.',
      officialUrl: 'https://humanresearchroadmap.nasa.gov/evidence/'
    },
    {
      id: 'radiation_storm',
      title: 'Solar Particle Event (SPE)',
      category: 'Radiation Storm',
      icon: Radio,
      color: 'text-purple-400 border-purple-500/30 bg-purple-500/10',
      description: 'Coronal Mass Ejection causes ionizing radiation spike (+45 mSv dose accumulation), triggering crew shelter protocol.',
      target: 'Entire Crew',
      nasaHazard: 'Space Radiation',
      researchReference: 'NASA Human Research Program – Space Radiation Element; Permissible Exposure Limits',
      implications: 'Solar proton fluxes beyond Low Earth Orbit can cause acute prodromal sickness, lymphocyte depression, and elevated lifetime cancer risk.',
      officialUrl: 'https://www.nasa.gov/hrp/risks/'
    },
    {
      id: 'sleep_deprivation',
      title: 'Circadian Collapse & Sleep Deficit',
      category: 'Neuro-Cognitive',
      icon: Moon,
      color: 'text-indigo-400 border-indigo-500/30 bg-indigo-500/10',
      description: '3 consecutive sols of fragmented sleep (<4.5 hrs) collapses HRV, spikes sympathetic stress index to 84/100.',
      target: 'Specific Astronaut',
      nasaHazard: 'Isolation and Confinement',
      researchReference: 'NASA HRP Behavioral Health & Performance (BHP) Evidence Report on Sleep & Circadian Adaptation',
      implications: 'Absence of natural sunlight, acoustic noise, and mission task overload degrade slow-wave sleep, increasing psychomotor lapse frequency.',
      officialUrl: 'https://humanresearchroadmap.nasa.gov/evidence/'
    },
    {
      id: 'dehydration',
      title: 'Dehydration & Orthostatic Shift',
      category: 'Hemodynamic',
      icon: Droplets,
      color: 'text-cyan-400 border-cyan-500/30 bg-cyan-500/10',
      description: 'Negative fluid balance causes blood pressure dip, compensatory HR rise, and cephalad fluid shift reduction.',
      target: 'Specific Astronaut',
      nasaHazard: 'Altered Gravity Fields',
      researchReference: 'NASA HRP Cardiovascular and Renal Stone Evidence Reports',
      implications: 'Microgravity diuresis leads to 10-15% plasma volume contraction; inadequate hydration triggers hypotension and nephrolithiasis risks.',
      officialUrl: 'https://humanresearchroadmap.nasa.gov/evidence/'
    },
    {
      id: 'sensor_failure',
      title: 'Biosensor Telemetry Dropout',
      category: 'System Artifact',
      icon: Cpu,
      color: 'text-yellow-400 border-yellow-500/30 bg-yellow-500/10',
      description: 'Optical pulse-oximeter sensor disconnects or produces high artifact noise (simulates hardware failure).',
      target: 'Specific Astronaut',
      nasaHazard: 'Distance from Earth (Autonomous Diagnostics)',
      researchReference: 'NASA ExMC HRP-48032 Rev. B Clinical Decision Support Architecture Recommendation',
      implications: 'Clinical decision systems in deep space must distinguish biological deterioration from hardware sensor disconnects.',
      officialUrl: 'https://ntrs.nasa.gov/citations/20220017869'
    }
  ];

  const handleTrigger = async (scenarioId) => {
    setLastActionStatus(`Triggering ${scenarioId}...`);
    const res = await triggerScenario(scenarioId, selectedAstro, severity);
    setLastActionStatus(`Active: ${scenarioId.toUpperCase()} (simulated with auto-recovery)`);
  };

  const handleReset = async () => {
    setLastActionStatus('Resetting all telemetry to nominal baseline...');
    await resetSimulation();
    setLastActionStatus('Reset complete: All vitals and environment nominal.');
  };

  const sampleCsvContent = {
    cardiac_stress: `astronaut_id,heart_rate,hrv,spo2,bp_systolic,bp_diastolic,core_temp,skin_temp,respiratory_rate,stress_index,activity_level
${selectedAstro},138.0,28.0,97.2,148.0,94.0,37.6,34.2,22.0,78.0,EXERCISE
${selectedAstro},142.5,24.0,96.8,152.0,96.0,37.8,34.5,24.0,84.0,EXERCISE
${selectedAstro},132.0,32.0,97.5,142.0,90.0,37.4,34.1,20.0,68.0,REST`,
    hypoxia: `astronaut_id,heart_rate,hrv,spo2,bp_systolic,bp_diastolic,core_temp,skin_temp,respiratory_rate,stress_index,activity_level
${selectedAstro},98.0,42.0,91.2,126.0,82.0,36.8,33.4,22.0,65.0,REST
${selectedAstro},104.0,38.0,89.5,130.0,85.0,36.9,33.2,24.0,72.0,REST
${selectedAstro},112.0,34.0,88.2,134.0,88.0,37.0,33.0,26.0,80.0,REST`
  };

  const handleImportSampleCsv = async (sampleKey) => {
    setCsvUploading(true);
    try {
      const csvStr = sampleCsvContent[sampleKey];
      const blob = new Blob([csvStr], { type: 'text/csv' });
      const formData = new FormData();
      formData.append('file', blob, `sample_${sampleKey}.csv`);
      formData.append('astronaut_id', selectedAstro);

      const res = await axios.post('/api/simulation/import-csv', formData);
      setLastActionStatus(`Imported ${res.data.readings_ingested} biometric records successfully! Check Astronaut Detail.`);
    } catch (e) {
      setLastActionStatus('Error uploading CSV sample.');
    } finally {
      setCsvUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-space-950/80 backdrop-blur-md animate-fade-in">
      <div className="relative w-full max-w-4xl max-h-[90vh] overflow-y-auto bg-space-900 border border-amber-500/40 rounded-2xl p-6 shadow-glow-amber">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-5">
          <div className="flex items-center space-x-3">
            <div className="p-2 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400">
              <Zap className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-lg font-black text-slate-100 tracking-tight">
                  MISSION SIMULATION & CRISIS INJECTION ENGINE
                </h2>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-amber-500/40 text-amber-400 font-bold">
                  SIMULATED TELEMETRY
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Trigger 6 calibrated aerospace medical contingencies grounded in NASA Human Research Program hazards.
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-space-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Selection */}
        <div className="flex items-center space-x-2 mb-4 border-b border-slate-800 pb-2">
          <button
            onClick={() => setActiveTab('scenarios')}
            className={`px-3 py-1.5 rounded-md font-mono text-xs font-semibold transition-all ${
              activeTab === 'scenarios' 
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            Scenarios & Crisis Injection
          </button>
          <button
            onClick={() => setActiveTab('csv')}
            className={`px-3 py-1.5 rounded-md font-mono text-xs font-semibold transition-all ${
              activeTab === 'csv' 
                ? 'bg-amber-500/20 text-amber-300 border border-amber-500/40' 
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            CSV Telemetry Ingestion (External Data)
          </button>
        </div>

        {/* Target Astronaut & Controls Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 p-3 bg-space-850 rounded-xl border border-slate-800 mb-5 text-xs">
          <div>
            <label className="block text-slate-400 mb-1 font-mono uppercase">Target Crew Member</label>
            <select
              value={selectedAstro}
              onChange={(e) => setSelectedAstro(parseInt(e.target.value))}
              className="w-full bg-space-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 focus:border-cyan-400 outline-none"
            >
              <option value={1}>Sarah Chen (Commander)</option>
              <option value={2}>Marcus Vance (Science Lead)</option>
              <option value={3}>Elena Rostova (Flight Eng - EVA)</option>
              <option value={4}>Alex Rivera (Medical Specialist)</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-400 mb-1 font-mono uppercase">Severity Level</label>
            <select
              value={severity}
              onChange={(e) => setSeverity(e.target.value)}
              className="w-full bg-space-900 border border-slate-700 rounded px-2.5 py-1.5 text-slate-200 focus:border-cyan-400 outline-none"
            >
              <option value="mild">Mild (Subtle physiological drift)</option>
              <option value="moderate">Moderate (Standard warning thresholds)</option>
              <option value="severe">Severe (Critical emergency triage)</option>
            </select>
          </div>

          <div>
            <label className="block text-slate-400 mb-1 font-mono uppercase">Clock Multiplier</label>
            <div className="flex space-x-1">
              {[1, 10, 60].map(s => (
                <button
                  key={s}
                  onClick={() => setSpeed(s)}
                  className={`flex-1 py-1.5 rounded font-mono font-bold transition-colors ${
                    simulationSpeed === s ? 'bg-cyan-500 text-space-950' : 'bg-space-900 text-slate-400 hover:text-white border border-slate-700'
                  }`}
                >
                  {s}x
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Action Status Notification */}
        {lastActionStatus && (
          <div className="mb-4 px-3 py-2 bg-cyan-950/60 border border-cyan-500/30 rounded text-xs text-cyan-300 font-mono flex items-center space-x-2">
            <CheckCircle className="w-4 h-4 text-cyan-400 shrink-0" />
            <span>{lastActionStatus}</span>
          </div>
        )}

        {/* TAB 1: Scenarios Grid */}
        {activeTab === 'scenarios' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-6">
            {scenarios.map(sc => {
              const Icon = sc.icon;
              const isExpanded = expandedResearch[sc.id];
              return (
                <div 
                  key={sc.id}
                  className="p-3.5 rounded-lg bg-space-850/80 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between"
                >
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <div className="flex items-center space-x-2">
                        <div className={`p-1.5 rounded ${sc.color}`}>
                          <Icon className="w-4 h-4" />
                        </div>
                        <span className="font-semibold text-slate-200 text-sm">{sc.title}</span>
                      </div>
                      <span className="text-[10px] font-mono text-slate-400 uppercase">{sc.category}</span>
                    </div>
                    <p className="text-xs text-slate-400 leading-relaxed mb-2">
                      {sc.description}
                    </p>

                    {/* Collapsible NASA Research Context */}
                    <div className="mb-3">
                      <button
                        onClick={() => toggleResearch(sc.id)}
                        className="text-[11px] font-mono text-cyan-400 hover:text-cyan-300 flex items-center space-x-1"
                      >
                        <BookOpen className="w-3 h-3" />
                        <span>NASA Research Rationale</span>
                        {isExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                      </button>

                      {isExpanded && (
                        <div className="mt-2 p-2.5 rounded bg-space-950/90 border border-cyan-500/30 text-[10px] font-mono space-y-1.5">
                          <div>
                            <span className="text-cyan-300 font-bold">NASA Hazard: </span>
                            <span className="text-slate-200">{sc.nasaHazard}</span>
                          </div>
                          <div>
                            <span className="text-amber-400 font-bold">Clinical Impact: </span>
                            <span className="text-slate-300">{sc.implications}</span>
                          </div>
                          <div className="pt-1 border-t border-slate-800 flex items-center justify-between text-slate-400">
                            <span className="truncate max-w-[200px]">{sc.researchReference}</span>
                            <a 
                              href={sc.officialUrl} 
                              target="_blank" 
                              rel="noreferrer"
                              className="text-cyan-400 hover:underline flex items-center space-x-0.5 shrink-0"
                            >
                              <span>Official Link</span>
                              <ExternalLink className="w-2.5 h-2.5" />
                            </a>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
                    <span className="text-[10px] font-mono text-cyan-400/80">Scope: {sc.target}</span>
                    <button
                      onClick={() => handleTrigger(sc.id)}
                      className="px-3 py-1 bg-space-700 hover:bg-cyan-600 hover:text-space-950 text-cyan-300 font-mono text-xs font-bold rounded transition-colors"
                    >
                      INJECT &rarr;
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* TAB 2: CSV Import */}
        {activeTab === 'csv' && (
          <div className="space-y-4 mb-6">
            <div className="p-4 bg-space-850 rounded-xl border border-slate-800 text-xs">
              <h3 className="font-bold text-slate-200 text-sm mb-1 flex items-center space-x-2">
                <FileSpreadsheet className="w-4 h-4 text-cyan-400" />
                <span>Simulate Ingestion of External Recorded Vitals (CSV)</span>
              </h3>
              <p className="text-slate-400 text-xs mb-4">
                Test how Dr D processes raw biometric series from external telemetry devices, smart garments, or emergency log archives.
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="p-3 bg-space-900 rounded-lg border border-slate-700 flex flex-col justify-between">
                  <div>
                    <span className="font-semibold text-rose-300">Preset A: Acute Exertional Tachycardia</span>
                    <p className="text-[11px] text-slate-400 mt-1">
                      Simulates 3 minutes of high heart rate (138-142 bpm) and elevated blood pressure.
                    </p>
                  </div>
                  <button
                    disabled={csvUploading}
                    onClick={() => handleImportSampleCsv('cardiac_stress')}
                    className="mt-3 px-3 py-1.5 bg-rose-950 hover:bg-rose-900 border border-rose-500/40 text-rose-300 rounded font-mono text-xs font-semibold flex items-center justify-center space-x-1.5"
                  >
                    <Upload className="w-3.5 h-3.5" />
                    <span>Load Cardiac CSV Sample</span>
                  </button>
                </div>

                <div className="p-3 bg-space-900 rounded-lg border border-slate-700 flex flex-col justify-between">
                  <div>
                    <span className="font-semibold text-cyan-300">Preset B: Hypoxia & Respiratory Desaturation</span>
                    <p className="text-[11px] text-slate-400 mt-1">
                      Simulates acute drop in SpO2 (91% down to 88%) with compensatory tachypnea.
                    </p>
                  </div>
                  <button
                    disabled={csvUploading}
                    onClick={() => handleImportSampleCsv('hypoxia')}
                    className="mt-3 px-3 py-1.5 bg-cyan-950 hover:bg-cyan-900 border border-cyan-500/40 text-cyan-300 rounded font-mono text-xs font-semibold flex items-center justify-center space-x-1.5"
                  >
                    <Upload className="w-3.5 h-3.5" />
                    <span>Load Hypoxia CSV Sample</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Modal Footer Controls */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-slate-800">
          <div className="flex items-center space-x-2 text-xs font-mono text-slate-400">
            <Info className="w-4 h-4 text-amber-400 shrink-0" />
            <span>All scenarios automatically resolve over 60-120 seconds, or can be reset immediately.</span>
          </div>

          <button
            onClick={handleReset}
            className="flex items-center space-x-1.5 px-4 py-2 bg-space-800 hover:bg-space-700 text-slate-300 hover:text-white rounded-lg font-mono text-xs font-bold border border-slate-700 transition-colors"
          >
            <RotateCcw className="w-4 h-4 text-cyan-400" />
            <span>RESET ALL TO NOMINAL</span>
          </button>
        </div>

      </div>
    </div>
  );
}
