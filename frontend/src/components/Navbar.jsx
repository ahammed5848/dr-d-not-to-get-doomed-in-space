import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLiveTelemetry } from '../context/WebSocketContext';
import { 
  Activity, Shield, AlertTriangle, Wind, TrendingUp, 
  ClipboardCheck, Sliders, FileText, Zap, LogOut, Radio, User, BookOpen, Menu, X
} from 'lucide-react';
import ScenarioModal from './ScenarioModal';

export default function Navbar() {
  const { user, logout, isSurgeon, isAdmin, isAstronaut } = useAuth();
  const { isConnected, simulationSpeed, setSpeed, activeScenarios } = useLiveTelemetry();
  const [showScenarioModal, setShowScenarioModal] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const location = useLocation();

  const navLinks = [
    { to: '/dashboard', label: 'Mission Control', icon: Activity, show: true },
    { to: '/alerts', label: 'Alerts Center', icon: AlertTriangle, show: true },
    { to: '/environment', label: 'Cabin Environment', icon: Wind, show: true },
    { to: '/trends', label: 'Mission Trends', icon: TrendingUp, show: true },
    { to: '/checkin', label: 'Daily Check-in', icon: ClipboardCheck, show: isAstronaut },
    { to: '/admin/thresholds', label: 'Thresholds', icon: Sliders, show: isAdmin || isSurgeon },
    { to: '/reports', label: 'Reports', icon: FileText, show: true },
    { to: '/research', label: 'NASA Research', icon: BookOpen, show: true },
  ];

  return (
    <>
      <header className="sticky top-0 z-40 bg-space-900/90 backdrop-blur-md border-b border-cyan-500/20 px-4 lg:px-8 py-2.5">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          
          {/* Brand & Mission Status */}
          <div className="flex items-center space-x-4">
            <Link to="/dashboard" className="flex items-center space-x-2.5 group">
              <div className="w-9 h-9 rounded-lg bg-space-950 border border-cyan-400/50 p-1 shadow-glow-cyan flex items-center justify-center">
                <svg viewBox="0 0 32 32" className="w-6 h-6" fill="none">
                  <path d="M7 6h7a9 9 0 0 1 9 9v2a9 9 0 0 1-9 9H7V6z" stroke="#06b6d4" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
                  <path d="M3 16h4l2-4 3 8 2.5-5 1.5 2h4" stroke="#22d3ee" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
              <div>
                <span className="font-extrabold text-xl tracking-wider text-cyan-400 group-hover:text-cyan-300 transition-colors">
                  Dr D
                </span>
                <span className="hidden sm:inline-block ml-2 text-[10px] tracking-widest text-slate-400 uppercase font-mono bg-space-800 px-1.5 py-0.5 rounded border border-slate-700">
                  ARES-V • SOL 142
                </span>
              </div>
            </Link>

            {/* Live WS Status */}
            <div className="hidden md:flex items-center space-x-1.5 bg-space-850 px-2.5 py-1 rounded-full border border-slate-800 text-xs font-mono">
              <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'}`} />
              <span className={isConnected ? 'text-emerald-400' : 'text-rose-400'}>
                {isConnected ? 'LIVE TELEMETRY' : 'OFFLINE'}
              </span>
            </div>
          </div>

          {/* Nav Links */}
          <nav className="hidden lg:flex items-center space-x-1">
            {navLinks.filter(l => l.show).map(link => {
              const Icon = link.icon;
              const isActive = location.pathname === link.to;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                    isActive 
                      ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-glow-cyan' 
                      : 'text-slate-300 hover:text-cyan-300 hover:bg-space-800/60'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{link.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Right Controls: Demo Mode, Speed, User */}
          <div className="flex items-center space-x-3">
            
            {/* Speed Multiplier */}
            <div className="hidden sm:flex items-center bg-space-850 rounded border border-slate-700 text-xs font-mono">
              {[1, 10, 60].map(s => (
                <button
                  key={s}
                  onClick={() => setSpeed(s)}
                  className={`px-2 py-1 transition-colors ${
                    simulationSpeed === s
                      ? 'bg-cyan-500 text-space-950 font-bold'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                  title={`${s}x Simulation Speed`}
                >
                  {s}x
                </button>
              ))}
            </div>

            {/* Demo Scenarios Button */}
            <button
              onClick={() => setShowScenarioModal(true)}
              className="relative flex items-center space-x-1.5 bg-gradient-to-r from-amber-500/20 to-rose-500/20 hover:from-amber-500/30 hover:to-rose-500/30 border border-amber-500/40 text-amber-300 px-3 py-1.5 rounded text-xs font-medium transition-all shadow-glow-amber"
            >
              <Zap className="w-3.5 h-3.5 text-amber-400 animate-bounce" />
              <span className="font-semibold">DEMO SCENARIOS</span>
              {activeScenarios.length > 0 && (
                <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping absolute -top-1 -right-1" />
              )}
            </button>

            {/* User Profile & Role */}
            <div className="flex items-center space-x-2 pl-2 border-l border-slate-800">
              <div className="text-right hidden md:block">
                <div className="text-xs font-semibold text-slate-200">{user?.full_name}</div>
                <div className="text-[10px] text-cyan-400 uppercase font-mono tracking-wider">{user?.role}</div>
              </div>
              <button
                onClick={logout}
                title="Sign Out"
                className="p-1.5 rounded hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>

              {/* Mobile Menu Hamburger */}
              <button
                onClick={() => setMobileMenuOpen(prev => !prev)}
                className="p-1.5 lg:hidden rounded bg-space-850 border border-slate-700 text-slate-300 hover:text-white"
                title="Toggle Menu"
              >
                {mobileMenuOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
              </button>
            </div>

          </div>
        </div>

        {/* Mobile Navigation Dropdown */}
        {mobileMenuOpen && (
          <nav className="lg:hidden mt-2 pt-2 border-t border-slate-800 grid grid-cols-2 gap-1 pb-1">
            {navLinks.filter(l => l.show).map(link => {
              const Icon = link.icon;
              const isActive = location.pathname === link.to;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center space-x-1.5 px-3 py-2 rounded-md text-xs font-medium transition-all ${
                    isActive 
                      ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30' 
                      : 'text-slate-300 hover:text-cyan-300 hover:bg-space-800/60'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5 shrink-0" />
                  <span className="truncate">{link.label}</span>
                </Link>
              );
            })}
          </nav>
        )}
      </header>

      {/* Scenario Injection Modal */}
      {showScenarioModal && (
        <ScenarioModal onClose={() => setShowScenarioModal(false)} />
      )}
    </>
  );
}
