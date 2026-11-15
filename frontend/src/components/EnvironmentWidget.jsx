import React from 'react';
import { Wind, Gauge, Droplet, Volume2, Thermometer, ShieldAlert, CheckCircle2 } from 'lucide-react';

export default function EnvironmentWidget({ environment }) {
  const env = environment || {
    co2_ppm: 520,
    o2_pct: 21.2,
    cabin_temp_c: 22.4,
    humidity_pct: 44.0,
    cabin_pressure_kpa: 101.3,
    noise_db: 58.2
  };

  const isCo2Crit = env.co2_ppm > 1800;
  const isCo2Warn = env.co2_ppm > 1000 && !isCo2Crit;

  const isPressureWarn = env.cabin_pressure_kpa < 95.0 || env.cabin_pressure_kpa > 105.0;
  const isO2Warn = env.o2_pct < 19.5 || env.o2_pct > 23.5;

  const metrics = [
    {
      label: 'Cabin CO2',
      val: env.co2_ppm.toFixed(0),
      unit: 'ppm',
      limit: '< 1000 ppm',
      status: isCo2Crit ? 'CRITICAL' : isCo2Warn ? 'WARNING' : 'NOMINAL',
      color: isCo2Crit ? 'text-rose-400' : isCo2Warn ? 'text-amber-400' : 'text-cyan-400',
      icon: Wind
    },
    {
      label: 'Oxygen (O2)',
      val: env.o2_pct.toFixed(1),
      unit: '%',
      limit: '19.5 - 23.5%',
      status: isO2Warn ? 'WARNING' : 'NOMINAL',
      color: isO2Warn ? 'text-amber-400' : 'text-emerald-400',
      icon: Gauge
    },
    {
      label: 'Cabin Pressure',
      val: env.cabin_pressure_kpa.toFixed(1),
      unit: 'kPa',
      limit: '95 - 105 kPa',
      status: isPressureWarn ? 'WARNING' : 'NOMINAL',
      color: isPressureWarn ? 'text-amber-400' : 'text-cyan-400',
      icon: Gauge
    },
    {
      label: 'Cabin Temp',
      val: env.cabin_temp_c.toFixed(1),
      unit: '°C',
      limit: '18 - 26 °C',
      status: 'NOMINAL',
      color: 'text-cyan-400',
      icon: Thermometer
    },
    {
      label: 'Humidity',
      val: env.humidity_pct.toFixed(0),
      unit: '%',
      limit: '35 - 60%',
      status: 'NOMINAL',
      color: 'text-cyan-400',
      icon: Droplet
    },
    {
      label: 'Acoustic Noise',
      val: env.noise_db.toFixed(0),
      unit: 'dB',
      limit: '< 65 dB',
      status: 'NOMINAL',
      color: 'text-slate-300',
      icon: Volume2
    }
  ];

  return (
    <div className={`hud-panel rounded-xl p-5 border ${isCo2Crit ? 'border-rose-500/50 shadow-glow-rose' : 'border-cyan-500/20'}`}>
      <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
        <div className="flex items-center space-x-2">
          <Wind className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-slate-100 text-sm tracking-wide">
            HABITATION MODULE ENVIRONMENTAL TELEMETRY
          </h3>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-space-950 border border-amber-500/40 text-amber-400 font-bold">
            SIMULATED ECLSS
          </span>
          <span className="text-[10px] font-mono text-slate-400 uppercase">Ares-V Hab-1</span>
          <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded border uppercase ${
            isCo2Crit ? 'bg-rose-500/20 text-rose-300 border-rose-500/40' : isCo2Warn ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' : 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30'
          }`}>
            {isCo2Crit ? 'CRITICAL CO2' : isCo2Warn ? 'ELEVATED CO2' : 'LIFE SUPPORT NOMINAL'}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {metrics.map((m, i) => {
          const Icon = m.icon;
          return (
            <div key={i} className="bg-space-850 p-3 rounded-lg border border-slate-800 flex flex-col justify-between">
              <div className="flex items-center justify-between text-slate-400 mb-1">
                <span className="text-[10px] font-mono uppercase">{m.label}</span>
                <Icon className="w-3.5 h-3.5 text-cyan-400/80" />
              </div>
              <div className="my-1">
                <span className={`text-xl font-mono font-bold ${m.color}`}>
                  {m.val}
                </span>
                <span className="text-xs font-mono text-slate-400 ml-1">{m.unit}</span>
              </div>
              <div className="text-[9px] font-mono text-slate-500">
                Safe: {m.limit}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
