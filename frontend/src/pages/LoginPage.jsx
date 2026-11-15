import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Shield, Lock, User, ArrowRight, Sparkles, CheckCircle2 } from 'lucide-react';

export default function LoginPage() {
  const [username, setUsername] = useState('surgeon');
  const [password, setPassword] = useState('Password123!');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e?.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Authentication failed. Check credentials.');
    } finally {
      setLoading(false);
    }
  };

  const quickLogin = async (u, p) => {
    setUsername(u);
    setPassword(p);
    setError('');
    setLoading(true);
    try {
      await login(u, p);
      navigate('/dashboard');
    } catch (err) {
      setError('Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 bg-space-950 relative overflow-hidden">
      {/* Ambient background glows */}
      <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none" />

      <div className="w-full max-w-md z-10">
        
        {/* Brand Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-space-900 border border-cyan-400/50 p-2 shadow-glow-cyan mb-3">
            <svg viewBox="0 0 32 32" className="w-10 h-10" fill="none">
              <path d="M7 6h7a9 9 0 0 1 9 9v2a9 9 0 0 1-9 9H7V6z" stroke="#06b6d4" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M3 16h4l2-4 3 8 2.5-5 1.5 2h4" stroke="#22d3ee" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <h1 className="text-3xl font-extrabold tracking-wider text-slate-100 flex items-center justify-center space-x-2">
            <span>Dr D</span>
          </h1>
          <p className="text-cyan-400 font-medium text-xs tracking-widest uppercase mt-1">
            Your health guardian beyond Earth.
          </p>
          <p className="text-slate-400 text-xs mt-2 max-w-sm mx-auto">
            Deep Space Autonomous Astronaut Health Monitoring & Early-Warning Platform
          </p>
        </div>

        {/* Login Panel */}
        <div className="hud-panel rounded-2xl p-7 border border-cyan-500/30 bg-space-900/90 shadow-2xl relative corner-accent">
          
          <form onSubmit={handleLogin} className="space-y-4">
            {error && (
              <div className="p-3 bg-rose-950/80 border border-rose-500/40 rounded-lg text-rose-300 text-xs font-mono">
                {error}
              </div>
            )}

            <div>
              <label className="block text-xs font-mono uppercase text-slate-300 mb-1.5">
                Operator Callsign / Username
              </label>
              <div className="relative">
                <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  className="w-full bg-space-850 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-slate-100 focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 outline-none transition-all"
                  placeholder="e.g. surgeon or schen"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-mono uppercase text-slate-300 mb-1.5">
                Security Passcode
              </label>
              <div className="relative">
                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full bg-space-850 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-slate-100 focus:border-cyan-400 focus:ring-1 focus:ring-cyan-400 outline-none transition-all"
                  placeholder="••••••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 mt-2 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-space-950 font-bold rounded-lg transition-all shadow-glow-cyan flex items-center justify-center space-x-2 text-sm"
            >
              <span>{loading ? 'AUTHENTICATING...' : 'ACCESS MISSION CONTROL'}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Quick Demo Logins for Hackathon Judges */}
          <div className="mt-6 pt-5 border-t border-slate-800">
            <div className="flex items-center justify-between mb-3">
              <span className="text-[11px] font-mono uppercase text-cyan-400 flex items-center space-x-1 font-semibold">
                <Sparkles className="w-3.5 h-3.5" />
                <span>1-Click Hackathon Demo Roles</span>
              </span>
              <span className="text-[10px] text-slate-500 font-mono">Password123!</span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs">
              <button
                type="button"
                onClick={() => quickLogin('surgeon', 'Password123!')}
                className="p-2 rounded bg-space-850 hover:bg-space-800 border border-slate-700 hover:border-cyan-500/50 text-left transition-colors"
              >
                <div className="font-bold text-slate-200">👨‍⚕️ Flight Surgeon</div>
                <div className="text-[10px] text-slate-400 font-mono">Full Fleet Overview</div>
              </button>

              <button
                type="button"
                onClick={() => quickLogin('schen', 'Password123!')}
                className="p-2 rounded bg-space-850 hover:bg-space-800 border border-slate-700 hover:border-cyan-500/50 text-left transition-colors"
              >
                <div className="font-bold text-slate-200">🚀 Cmdr. Sarah Chen</div>
                <div className="text-[10px] text-slate-400 font-mono">Astronaut Portal</div>
              </button>

              <button
                type="button"
                onClick={() => quickLogin('erostova', 'Password123!')}
                className="p-2 rounded bg-space-850 hover:bg-space-800 border border-slate-700 hover:border-cyan-500/50 text-left transition-colors"
              >
                <div className="font-bold text-slate-200">🛠️ Elena Rostova</div>
                <div className="text-[10px] text-slate-400 font-mono">EVA Systems Lead</div>
              </button>

              <button
                type="button"
                onClick={() => quickLogin('admin', 'Password123!')}
                className="p-2 rounded bg-space-850 hover:bg-space-800 border border-slate-700 hover:border-cyan-500/50 text-left transition-colors"
              >
                <div className="font-bold text-slate-200">⚙️ Mission Admin</div>
                <div className="text-[10px] text-slate-400 font-mono">Configure Thresholds</div>
              </button>
            </div>
          </div>

        </div>

        {/* Footer info */}
        <div className="text-center mt-6 text-[11px] text-slate-500 font-mono">
          Dr D Ares-V Mission Control • Autonomous Bio-Telemetry Suite 1.0
        </div>

      </div>
    </div>
  );
}
