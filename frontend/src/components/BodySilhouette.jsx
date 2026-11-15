import React, { useState } from 'react';
import { Activity, Heart, Wind, Brain, Bone, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function BodySilhouette({ astronaut, vitals, riskData }) {
  const [selectedSystem, setSelectedSystem] = useState('cardio');

  const hr = vitals?.heart_rate || 70;
  const spo2 = vitals?.spo2 || 98.5;
  const temp = vitals?.core_temp || 36.8;
  const bpSys = vitals?.bp_systolic || 120;
  const bpDia = vitals?.bp_diastolic || 80;
  const stress = vitals?.stress_index || 20;
  const fluidShift = vitals?.fluid_shift_score || astronaut.fluid_shift_score || 18;
  const boneLoss = astronaut.bone_density_loss_pct || 2.4;
  const muscleIndex = astronaut.muscle_mass_index || 94.2;

  // Determine system health flags
  const isCardioWarn = hr > 100 || hr < 50 || bpSys > 135;
  const isRespWarn = spo2 < 95.0 || vitals?.respiratory_rate > 20;
  const isNeuroWarn = stress > 65 || fluidShift > 25;
  const isMusculoWarn = boneLoss > 3.0 || muscleIndex < 90;

  const systems = [
    {
      id: 'cardio',
      name: 'Cardiovascular Loop',
      icon: Heart,
      status: isCardioWarn ? 'WARNING' : 'NOMINAL',
      color: isCardioWarn ? '#f43f5e' : '#22d3ee',
      details: [
        { label: 'Heart Rate', val: `${hr.toFixed(0)} bpm`, normal: '60 - 100 bpm' },
        { label: 'Blood Pressure', val: `${bpSys.toFixed(0)}/${bpDia.toFixed(0)} mmHg`, normal: '110-125 / 70-80' },
        { label: 'HRV (RMSSD)', val: `${(vitals?.hrv || 65).toFixed(0)} ms`, normal: '> 45 ms' },
      ]
    },
    {
      id: 'resp',
      name: 'Pulmonary Exchange',
      icon: Wind,
      status: isRespWarn ? 'WARNING' : 'NOMINAL',
      color: isRespWarn ? '#fbbf24' : '#34d399',
      details: [
        { label: 'SpO2 Saturation', val: `${spo2.toFixed(1)}%`, normal: '96% - 100%' },
        { label: 'Resp Rate', val: `${(vitals?.respiratory_rate || 14).toFixed(0)} br/min`, normal: '12 - 18 br/min' },
        { label: 'Alveolar Diffusion', val: '99.2%', normal: '> 95%' },
      ]
    },
    {
      id: 'neuro',
      name: 'Neuro-Cranial & ICP',
      icon: Brain,
      status: isNeuroWarn ? 'WARNING' : 'NOMINAL',
      color: isNeuroWarn ? '#a855f7' : '#06b6d4',
      details: [
        { label: 'Fluid Shift / ICP Risk', val: `${fluidShift.toFixed(0)} / 100`, normal: '< 25 / 100' },
        { label: 'Sympathetic Stress', val: `${stress.toFixed(0)} / 100`, normal: '< 50 / 100' },
        { label: 'Circadian Disruption', val: `${(vitals?.circadian_disruption_score || 14).toFixed(0)} / 100`, normal: '< 30' },
      ]
    },
    {
      id: 'musculo',
      name: 'Musculoskeletal Matrix',
      icon: Bone,
      status: isMusculoWarn ? 'WARNING' : 'NOMINAL',
      color: isMusculoWarn ? '#f59e0b' : '#38bdf8',
      details: [
        { label: 'Bone Density Loss', val: `-${boneLoss.toFixed(1)}%`, normal: '< 3.5% mission sol' },
        { label: 'Muscle Mass Index', val: `${muscleIndex.toFixed(1)}%`, normal: '> 90%' },
        { label: 'Daily ARED Load', val: '100% adherence', normal: '2.5 hrs/sol' },
      ]
    }
  ];

  const currentSys = systems.find(s => s.id === selectedSystem) || systems[0];

  return (
    <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div className="flex items-center space-x-2">
          <Activity className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-slate-100 text-sm tracking-wide">
            PHYSIOLOGICAL SUBSYSTEM SILHOUETTE
          </h3>
        </div>
        <span className="text-[10px] font-mono text-cyan-400 uppercase bg-cyan-950 px-2 py-0.5 rounded border border-cyan-500/30">
          Interactive Anatomy HUD
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
        
        {/* SVG Anatomical Silhouette with Hotspots */}
        <div className="relative flex justify-center py-2 bg-space-900/60 rounded-xl border border-slate-800/80">
          <svg className="w-48 h-80 drop-shadow-[0_0_15px_rgba(6,182,212,0.15)]" viewBox="0 0 200 360">
            {/* Ambient Body Contour */}
            <path
              d="M 100 25 C 85 25 80 40 80 55 C 80 70 88 80 90 85 C 75 90 55 105 45 130 C 35 155 30 190 28 220 C 27 235 38 238 42 225 C 48 200 55 160 62 145 L 60 210 L 65 330 C 66 345 80 345 82 330 L 92 230 L 100 230 L 108 230 L 118 330 C 120 345 134 345 135 330 L 140 210 L 138 145 C 145 160 152 200 158 225 C 162 238 173 235 172 220 C 170 190 165 155 155 130 C 145 105 125 90 110 85 C 112 80 120 70 120 55 C 120 40 115 25 100 25 Z"
              fill="#0b132b"
              stroke="#1c2e5c"
              strokeWidth="2"
            />

            {/* Neuro hotspot (Head) */}
            <g onClick={() => setSelectedSystem('neuro')} className="cursor-pointer group">
              <circle 
                cx="100" cy="52" r="16" 
                fill={isNeuroWarn ? 'rgba(168, 85, 247, 0.25)' : 'rgba(6, 182, 212, 0.15)'} 
                stroke={isNeuroWarn ? '#a855f7' : '#06b6d4'}
                strokeWidth={selectedSystem === 'neuro' ? 2.5 : 1}
                className={isNeuroWarn ? 'animate-pulse' : ''}
              />
              <circle cx="100" cy="52" r="4" fill={isNeuroWarn ? '#a855f7' : '#22d3ee'} />
            </g>

            {/* Pulmonary / Lungs hotspot */}
            <g onClick={() => setSelectedSystem('resp')} className="cursor-pointer group">
              <ellipse 
                cx="88" cy="115" rx="12" ry="16" 
                fill={isRespWarn ? 'rgba(251, 191, 36, 0.25)' : 'rgba(52, 211, 153, 0.15)'} 
                stroke={isRespWarn ? '#fbbf24' : '#34d399'}
                strokeWidth={selectedSystem === 'resp' ? 2.5 : 1}
                className={isRespWarn ? 'animate-pulse' : ''}
              />
              <ellipse 
                cx="112" cy="115" rx="12" ry="16" 
                fill={isRespWarn ? 'rgba(251, 191, 36, 0.25)' : 'rgba(52, 211, 153, 0.15)'} 
                stroke={isRespWarn ? '#fbbf24' : '#34d399'}
                strokeWidth={selectedSystem === 'resp' ? 2.5 : 1}
                className={isRespWarn ? 'animate-pulse' : ''}
              />
            </g>

            {/* Cardio hotspot (Heart) */}
            <g onClick={() => setSelectedSystem('cardio')} className="cursor-pointer group">
              <circle 
                cx="102" cy="120" r="11" 
                fill={isCardioWarn ? 'rgba(244, 63, 94, 0.35)' : 'rgba(6, 182, 212, 0.25)'} 
                stroke={isCardioWarn ? '#f43f5e' : '#22d3ee'}
                strokeWidth={selectedSystem === 'cardio' ? 3 : 1.5}
                className={isCardioWarn ? 'animate-ping' : 'animate-pulse'}
              />
              <circle cx="102" cy="120" r="4" fill={isCardioWarn ? '#f43f5e' : '#22d3ee'} />
            </g>

            {/* Spine & Musculoskeletal hotspot */}
            <g onClick={() => setSelectedSystem('musculo')} className="cursor-pointer group">
              <line 
                x1="100" y1="135" x2="100" y2="215" 
                stroke={isMusculoWarn ? '#f59e0b' : '#38bdf8'} 
                strokeWidth={selectedSystem === 'musculo' ? 4 : 2} 
                strokeDasharray="4 2"
              />
              <circle cx="85" cy="275" r="5" fill={isMusculoWarn ? '#f59e0b' : '#38bdf8'} />
              <circle cx="115" cy="275" r="5" fill={isMusculoWarn ? '#f59e0b' : '#38bdf8'} />
            </g>
          </svg>

          {/* Quick Hotspot Pills */}
          <div className="absolute bottom-2 left-2 right-2 flex justify-center space-x-1">
            {systems.map(s => (
              <button
                key={s.id}
                onClick={() => setSelectedSystem(s.id)}
                className={`px-2 py-0.5 rounded text-[9px] font-mono transition-colors ${
                  selectedSystem === s.id 
                    ? 'bg-cyan-500 text-space-950 font-bold' 
                    : 'bg-space-800 text-slate-400 hover:text-white'
                }`}
              >
                {s.name.split(' ')[0]}
              </button>
            ))}
          </div>
        </div>

        {/* Selected Subsystem Detail Readout */}
        <div className="space-y-4">
          <div className="p-3.5 bg-space-850 rounded-lg border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center space-x-2">
                <currentSys.icon className="w-5 h-5 text-cyan-400" />
                <span className="font-bold text-slate-100 text-sm">{currentSys.name}</span>
              </div>
              <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border uppercase ${
                currentSys.status === 'WARNING' 
                  ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                  : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
              }`}>
                {currentSys.status}
              </span>
            </div>

            <div className="divide-y divide-slate-800/80">
              {currentSys.details.map((d, i) => (
                <div key={i} className="py-2 flex items-center justify-between text-xs">
                  <div>
                    <span className="text-slate-400">{d.label}</span>
                    <span className="block text-[10px] font-mono text-slate-500">Ref: {d.normal}</span>
                  </div>
                  <span className="font-mono font-bold text-slate-200">{d.val}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="p-3 bg-cyan-950/40 border border-cyan-500/20 rounded-lg text-xs text-slate-300">
            <span className="text-cyan-400 font-bold font-mono">Telemetry Correlation: </span>
            {selectedSystem === 'cardio' && "Vascular dynamics show typical microgravity adaptation with cephalad blood volume redistribution."}
            {selectedSystem === 'resp' && "Ventilation parameters tracking cabin oxygen partial pressure. No signs of hypercapnia."}
            {selectedSystem === 'neuro' && "Circadian marker stable. Facial edema fluid shift score within tolerable threshold for Sol 142."}
            {selectedSystem === 'musculo' && "Countermeasure resistive exercises mitigating bone demineralization trajectory on track."}
          </div>
        </div>

      </div>
    </div>
  );
}
