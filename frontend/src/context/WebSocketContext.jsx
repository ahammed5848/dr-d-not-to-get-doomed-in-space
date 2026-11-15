import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import axios from 'axios';

const WebSocketContext = createContext(null);

export const WebSocketProvider = ({ children }) => {
  const [isConnected, setIsConnected] = useState(false);
  const [crewTelemetry, setCrewTelemetry] = useState({});
  const [environment, setEnvironment] = useState({
    co2_ppm: 520.0,
    o2_pct: 21.2,
    cabin_temp_c: 22.4,
    humidity_pct: 44.0,
    cabin_pressure_kpa: 101.3,
    noise_db: 58.2
  });
  const [activeScenarios, setActiveScenarios] = useState([]);
  const [simulationSpeed, setSimulationSpeed] = useState(1);
  const [latestAlertBanner, setLatestAlertBanner] = useState(null);
  const wsRef = useRef(null);

  useEffect(() => {
    let reconnectTimeout = null;
    let isUnmounted = false;

    const getWsUrl = () => {
      // 1. Explicit WebSocket URL override if configured
      if (import.meta.env.VITE_WS_URL) {
        return import.meta.env.VITE_WS_URL;
      }
      // 2. Derive from VITE_API_BASE_URL if configured (e.g. https://dr-d-backend.onrender.com)
      const apiBase = import.meta.env.VITE_API_BASE_URL;
      if (apiBase) {
        const isSecure = apiBase.startsWith('https:');
        const wsProto = isSecure ? 'wss:' : 'ws:';
        const cleanHost = apiBase.replace(/^https?:\/\//, '').replace(/\/api\/?$/, '').replace(/\/+$/, '');
        return `${wsProto}//${cleanHost}/ws/live`;
      }
      // 3. Local dev fallback using current browser origin
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const host = window.location.host;
      return `${protocol}//${host}/ws/live`;
    };

    const connectWs = () => {
      const wsUrl = getWsUrl();
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        if (!isUnmounted) setIsConnected(true);
      };

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'TELEMETRY_UPDATE') {
            if (data.environment) setEnvironment(data.environment);
            if (data.active_scenarios) setActiveScenarios(data.active_scenarios);
            if (data.simulation_speed) setSimulationSpeed(data.simulation_speed);

            if (data.crew && Array.isArray(data.crew)) {
              setCrewTelemetry(prev => {
                const next = { ...prev };
                data.crew.forEach(member => {
                  next[member.astronaut_id] = member;
                });
                return next;
              });
            }

            if (data.new_alerts_count > 0) {
              // Trigger audio/visual alert banner
              fetchLatestAlert();
            }
          }
        } catch (e) {
          console.error("WS parse error", e);
        }
      };

      ws.onclose = () => {
        if (!isUnmounted) {
          setIsConnected(false);
          reconnectTimeout = setTimeout(connectWs, 2000);
        }
      };

      ws.onerror = () => {
        ws.close();
      };
    };

    connectWs();

    return () => {
      isUnmounted = true;
      if (reconnectTimeout) clearTimeout(reconnectTimeout);
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  const fetchLatestAlert = async () => {
    try {
      const res = await axios.get('/api/alerts?limit=1');
      if (res.data && res.data.length > 0) {
        const top = res.data[0];
        if (top.status === 'ACTIVE') {
          setLatestAlertBanner(top);
        }
      }
    } catch (e) {}
  };

  const triggerScenario = async (scenarioType, astronautId = null, severity = "moderate") => {
    try {
      const res = await axios.post('/api/simulation/scenario', {
        scenario_type: scenarioType,
        astronaut_id: astronautId,
        severity
      });
      fetchLatestAlert();
      return res.data;
    } catch (e) {
      console.error("Trigger scenario failed", e);
    }
  };

  const setSpeed = async (speed) => {
    try {
      const res = await axios.post('/api/simulation/speed', { speed });
      setSimulationSpeed(speed);
      return res.data;
    } catch (e) {
      console.error("Set speed failed", e);
    }
  };

  const resetSimulation = async () => {
    try {
      const res = await axios.post('/api/simulation/reset');
      setLatestAlertBanner(null);
      return res.data;
    } catch (e) {
      console.error("Reset simulation failed", e);
    }
  };

  return (
    <WebSocketContext.Provider value={{
      isConnected,
      crewTelemetry,
      environment,
      activeScenarios,
      simulationSpeed,
      latestAlertBanner,
      setLatestAlertBanner,
      triggerScenario,
      setSpeed,
      resetSimulation
    }}>
      {children}
    </WebSocketContext.Provider>
  );
};

export const useLiveTelemetry = () => useContext(WebSocketContext);
