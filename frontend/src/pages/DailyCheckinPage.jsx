import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { 
  ClipboardCheck, CheckCircle2, Moon, Smile, Battery, 
  Brain, AlertCircle, History, Send
} from 'lucide-react';

export default function DailyCheckinPage() {
  const { user } = useAuth();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submittedSuccess, setSubmittedSuccess] = useState(false);

  // Form fields
  const [sleepHours, setSleepHours] = useState(7.5);
  const [sleepQuality, setSleepQuality] = useState(8);
  const [physicalFatigue, setPhysicalFatigue] = useState(3);
  const [cognitiveFatigue, setCognitiveFatigue] = useState(2);
  const [moodScore, setMoodScore] = useState(8);
  const [muscleSoreness, setMuscleSoreness] = useState(2);
  const [headacheScore, setHeadacheScore] = useState(1);
  const [spaceMotionSickness, setSpaceMotionSickness] = useState(1);
  const [comments, setComments] = useState('');

  const fetchHistory = async () => {
    try {
      const res = await axios.get('/api/checkins?limit=10');
      setHistory(res.data);
    } catch (e) {
      console.error("Failed to load check-ins", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/api/checkins', {
        astronaut_id: user?.astronaut_id || 1,
        sleep_hours: parseFloat(sleepHours),
        sleep_quality_score: parseFloat(sleepQuality),
        physical_fatigue: parseFloat(physicalFatigue),
        cognitive_fatigue: parseFloat(cognitiveFatigue),
        mood_score: parseFloat(moodScore),
        muscle_soreness: parseFloat(muscleSoreness),
        headache_score: parseFloat(headacheScore),
        space_motion_sickness: parseFloat(spaceMotionSickness),
        comments
      });
      setSubmittedSuccess(true);
      setComments('');
      fetchHistory();
      setTimeout(() => setSubmittedSuccess(false), 5000);
    } catch (e) {
      console.error("Check-in submission failed", e);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      
      {/* Header */}
      <div className="hud-panel rounded-2xl p-5 border border-cyan-500/25 bg-space-900/90 relative corner-accent">
        <div className="flex items-center space-x-3 mb-1">
          <ClipboardCheck className="w-6 h-6 text-cyan-400" />
          <div>
            <h1 className="text-xl font-black text-slate-100 tracking-tight">
              ASTRONAUT DAILY SUBJECTIVE WELLBEING CHECK-IN
            </h1>
            <p className="text-xs text-slate-400">
              Sol 142 Protocol • Standardized NASA / ESA crew psychological & somatic monitoring
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Check-in Form */}
        <div className="lg:col-span-2 hud-panel rounded-xl p-6 border border-cyan-500/20">
          
          {submittedSuccess && (
            <div className="mb-4 p-3 bg-emerald-950/80 border border-emerald-500/40 rounded-lg text-emerald-300 text-xs font-mono flex items-center space-x-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              <span>Daily Check-in successfully logged and synchronized with Ground Flight Surgeon record!</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6 text-xs">
            
            {/* Sleep Section */}
            <div className="p-4 bg-space-850 rounded-lg border border-slate-800 space-y-4">
              <div className="flex items-center space-x-2 font-bold text-slate-200">
                <Moon className="w-4 h-4 text-indigo-400" />
                <span>Sleep Architecture & Duration</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-slate-400 font-mono mb-1">
                    Sleep Duration: <strong className="text-cyan-400">{sleepHours} hours</strong>
                  </label>
                  <input
                    type="range"
                    min="3.0"
                    max="10.0"
                    step="0.5"
                    value={sleepHours}
                    onChange={(e) => setSleepHours(e.target.value)}
                    className="w-full accent-cyan-400 cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
                    <span>3h (Deficit)</span>
                    <span>7.5h (Target)</span>
                    <span>10h</span>
                  </div>
                </div>

                <div>
                  <label className="block text-slate-400 font-mono mb-1">
                    Sleep Restfulness / Quality: <strong className="text-cyan-400">{sleepQuality}/10</strong>
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={sleepQuality}
                    onChange={(e) => setSleepQuality(e.target.value)}
                    className="w-full accent-cyan-400 cursor-pointer"
                  />
                  <div className="flex justify-between text-[10px] text-slate-500 font-mono mt-1">
                    <span>1 (Poor)</span>
                    <span>5 (Average)</span>
                    <span>10 (Optimal)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Fatigue & Mood Section */}
            <div className="p-4 bg-space-850 rounded-lg border border-slate-800 space-y-4">
              <div className="flex items-center space-x-2 font-bold text-slate-200">
                <Battery className="w-4 h-4 text-amber-400" />
                <span>Cognitive & Physical Fatigue (1–10 Scales)</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-slate-400 font-mono mb-1">
                    Physical Fatigue: <strong className="text-amber-400">{physicalFatigue}/10</strong>
                  </label>
                  <input
                    type="range" min="1" max="10" value={physicalFatigue}
                    onChange={(e) => setPhysicalFatigue(e.target.value)}
                    className="w-full accent-amber-400 cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-slate-400 font-mono mb-1">
                    Cognitive Fog: <strong className="text-amber-400">{cognitiveFatigue}/10</strong>
                  </label>
                  <input
                    type="range" min="1" max="10" value={cognitiveFatigue}
                    onChange={(e) => setCognitiveFatigue(e.target.value)}
                    className="w-full accent-amber-400 cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-slate-400 font-mono mb-1">
                    Mood / Morale: <strong className="text-emerald-400">{moodScore}/10</strong>
                  </label>
                  <input
                    type="range" min="1" max="10" value={moodScore}
                    onChange={(e) => setMoodScore(e.target.value)}
                    className="w-full accent-emerald-400 cursor-pointer"
                  />
                </div>
              </div>
            </div>

            {/* Somatic Symptoms Section */}
            <div className="p-4 bg-space-850 rounded-lg border border-slate-800 space-y-4">
              <div className="flex items-center space-x-2 font-bold text-slate-200">
                <Brain className="w-4 h-4 text-purple-400" />
                <span>Somatic Symptoms & Microgravity Adaptation</span>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-slate-400 font-mono mb-1">
                    Muscle Soreness: <strong className="text-slate-200">{muscleSoreness}/10</strong>
                  </label>
                  <input
                    type="range" min="1" max="10" value={muscleSoreness}
                    onChange={(e) => setMuscleSoreness(e.target.value)}
                    className="w-full accent-purple-400 cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-slate-400 font-mono mb-1">
                    Headache / ICP Pressure: <strong className="text-rose-400">{headacheScore}/10</strong>
                  </label>
                  <input
                    type="range" min="1" max="10" value={headacheScore}
                    onChange={(e) => setHeadacheScore(e.target.value)}
                    className="w-full accent-rose-400 cursor-pointer"
                  />
                </div>

                <div>
                  <label className="block text-slate-400 font-mono mb-1">
                    Space Motion Sickness: <strong className="text-slate-200">{spaceMotionSickness}/10</strong>
                  </label>
                  <input
                    type="range" min="1" max="10" value={spaceMotionSickness}
                    onChange={(e) => setSpaceMotionSickness(e.target.value)}
                    className="w-full accent-purple-400 cursor-pointer"
                  />
                </div>
              </div>
            </div>

            {/* Qualitative Notes */}
            <div>
              <label className="block text-slate-400 font-mono mb-1">
                Qualitative Self-Report / Symptoms Description
              </label>
              <textarea
                rows={3}
                value={comments}
                onChange={(e) => setComments(e.target.value)}
                placeholder="Describe any vision blur, nasal congestion, fluid fullness in head, or equipment ergonomics concerns..."
                className="w-full bg-space-850 border border-slate-700 rounded-lg p-3 text-xs text-slate-100 outline-none focus:border-cyan-400"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-cyan-600 hover:bg-cyan-500 text-space-950 font-bold font-mono rounded-lg transition-colors flex items-center justify-center space-x-2 shadow-glow-cyan"
            >
              <Send className="w-4 h-4" />
              <span>TRANSMIT DAILY CHECK-IN TO MISSION CONTROL</span>
            </button>
          </form>

        </div>

        {/* Check-in History Feed */}
        <div className="hud-panel rounded-xl p-5 border border-cyan-500/20">
          <div className="flex items-center space-x-2 pb-3 border-b border-slate-800 mb-4">
            <History className="w-4 h-4 text-cyan-400" />
            <h3 className="font-bold text-slate-100 text-sm">PREVIOUS CHECK-IN LOGS</h3>
          </div>

          <div className="space-y-3">
            {history.length === 0 ? (
              <div className="py-6 text-center text-xs text-slate-500 font-mono">No previous check-ins on record.</div>
            ) : (
              history.map(item => (
                <div key={item.id} className="p-3 bg-space-850 rounded-lg border border-slate-800 text-xs font-mono">
                  <div className="flex items-center justify-between text-cyan-400 mb-1">
                    <span className="font-bold">{item.date}</span>
                    <span className="text-[10px] text-slate-400">Sleep: {item.sleep_hours}h (Q: {item.sleep_quality_score}/10)</span>
                  </div>
                  <div className="grid grid-cols-3 gap-1 text-[10px] text-slate-400 my-1">
                    <span>Fatigue: {item.physical_fatigue}/10</span>
                    <span>Mood: {item.mood_score}/10</span>
                    <span>Headache: {item.headache_score}/10</span>
                  </div>
                  {item.comments && (
                    <div className="mt-1 pt-1 border-t border-slate-800/60 text-slate-300 font-sans text-[11px]">
                      "{item.comments}"
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>

      </div>

    </div>
  );
}
