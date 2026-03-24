import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, CheckCircle, Database, Server, Zap, BrainCircuit, RotateCw, Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { getIncidents, explainIncident, getHealth } from '../services/api';
import MetricCard from '../components/MetricCard';
import ChartWidget from '../components/ChartWidget';
import AiAnalysisModal from '../components/AiAnalysisModal';

const Dashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [systemHealth, setSystemHealth] = useState('healthy');
  
  // AI Modal State
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Mocking rich chart data for the interactive premium feel
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    fetchDashboardData();
    generateMockChartData();
    const interval = setInterval(fetchDashboardData, 10000); // 10s refresh
    return () => clearInterval(interval);
  }, []);

  const generateMockChartData = () => {
    // Generate some wave-like data simulating log ingestion over time
    const data = [];
    let baseVol = 3000;
    let baseErr = 50;
    
    for(let i=12; i>=0; i--) {
      const time = new Date(Date.now() - i * 60000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      baseVol = baseVol + (Math.random() * 800 - 400);
      baseErr = Math.max(0, baseErr + (Math.random() * 30 - 15));
      if(i === 3) baseErr += 300; // Fake spike
      
      data.push({
        time,
        volume: Math.floor(Math.abs(baseVol)),
        errors: Math.floor(Math.abs(baseErr))
      });
    }
    setChartData(data);
  };

  const fetchDashboardData = async () => {
    try {
      const health = await getHealth();
      setSystemHealth(health?.status || 'healthy');
      
      const data = await getIncidents();
      setIncidents(data.anomalies || []);
    } catch (error) {
      console.error("Dashboard fetch cycle failed", error);
    } finally {
      setLoading(false);
    }
  };

  const handleExplain = async (incident) => {
    setSelectedIncident(incident);
    setIsAnalyzing(true);
    setAiAnalysis(null);
    try {
      const analysis = await explainIncident(incident.service_id, incident.description);
      setAiAnalysis(analysis);
    } catch (error) {
      console.error("AI Analysis flow failed", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  // If no incidents from API, let's inject a premium mock one for the demo
  const displayIncidents = incidents.length > 0 ? incidents : [
    {
      id: 999,
      service_id: 1,
      anomaly_score: 0.85,
      description: "Sudden spike in connection timeouts and latent GC pauses.",
      detected_at: new Date().toISOString(),
      status: "pending"
    },
    {
      id: 998,
      service_id: 2,
      anomaly_score: 0.62,
      description: "Elevated 5xx error rate in payment-gateway container.",
      detected_at: new Date(Date.now() - 3600000).toISOString(),
      status: "pending"
    }
  ];

  return (
    <div className="space-y-8 relative">
      <div className="flex justify-between items-end">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5 }}>
          <h1 className="text-4xl font-extrabold tracking-tight mb-2 header-glow inline-block">Global Telemetry</h1>
          <p className="text-text-muted text-lg">AI-powered system observability matrix.</p>
        </motion.div>
        
        <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5 }}>
          <div className="glass-panel px-4 py-2 flex items-center gap-3">
            <span className="text-sm text-text-muted font-medium uppercase tracking-wider">Status:</span>
            <div className={`px-3 py-1 rounded-md text-sm font-bold flex items-center gap-2 ${systemHealth === 'healthy' ? 'bg-success/10 text-success border border-success/30 shadow-[0_0_10px_rgba(16,185,129,0.3)]' : 'bg-danger/10 text-danger border border-danger/30'}`}>
              <span className={`w-2 h-2 rounded-full ${systemHealth === 'healthy' ? 'bg-success animate-pulse' : 'bg-danger animate-pulse'}`}></span>
              {systemHealth === 'healthy' ? 'OPTIMAL' : 'DEGRADED'}
            </div>
          </div>
        </motion.div>
      </div>

      {/* Metrics Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6"
      >
        <MetricCard title="Log Ingestion (24h)" value="24.8" unit="M" icon={Database} trend={+18.4} colorClass="primary" />
        <MetricCard title="Active Anomalies" value={displayIncidents.length.toString()} icon={AlertTriangle} trend={displayIncidents.length > 0 ? +12 : -5} colorClass={displayIncidents.length > 0 ? "warning" : "success"} />
        <MetricCard title="P99 Latency Mean" value="142" unit="ms" icon={Zap} trend={-4.2} colorClass="success" />
        <MetricCard title="Active Nodes" value="12" icon={Server} colorClass="secondary" />
      </motion.div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Main Chart */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }}
          className="xl:col-span-2 shadow-[0_0_30px_rgba(102,252,241,0.05)] rounded-2xl"
        >
          <ChartWidget 
            title="Telemetry Flow & Error Spikes"
            data={chartData}
            height={400}
            lines={[
              { key: 'volume', name: 'Log Volume', color: '#66FCF1' },
              { key: 'errors', name: 'Error Rate', color: '#EF4444' }
            ]}
          />
        </motion.div>

        {/* Incidents List */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.3 }}
          className="xl:col-span-1 glass-panel flex flex-col h-full overflow-hidden border-warning/20 shadow-[0_0_30px_rgba(245,158,11,0.05)]"
        >
          <div className="p-6 border-b border-border/50 flex justify-between items-center bg-gradient-to-r from-warning/10 to-transparent">
            <h2 className="text-xl font-bold flex items-center gap-2 text-white">
              <Activity className="text-warning" />
              Intelligence Feed
            </h2>
            <button 
              className="text-text-muted hover:text-white hover:bg-surfaceHighlight p-2 rounded-lg transition-all" 
              onClick={fetchDashboardData}
            >
              <RotateCw size={18} className={loading ? "animate-spin text-primary" : ""} />
            </button>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar">
            {loading ? (
              <div className="h-full flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-primary animate-spin" />
              </div>
            ) : displayIncidents.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-center p-8">
                <CheckCircle className="w-16 h-16 text-success mb-4 opacity-50 drop-shadow-[0_0_15px_rgba(16,185,129,0.5)]" />
                <h3 className="text-xl font-bold text-white mb-2">Systems Nominal</h3>
                <p className="text-text-muted text-sm">No anomalous patterns detected in the current telemetry window.</p>
              </div>
            ) : (
              displayIncidents.map((inc) => (
                <div key={inc.id} className="bg-surface/60 border border-border hover:border-warning/50 rounded-xl p-4 transition-all duration-300 group hover:shadow-[0_5px_15px_rgba(0,0,0,0.3)]">
                  <div className="flex justify-between items-start mb-3">
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold tracking-widest uppercase ${
                      inc.anomaly_score > 0.8 ? 'bg-danger/20 text-danger border border-danger/30' : 
                      'bg-warning/20 text-warning border border-warning/30'
                    }`}>
                      {inc.anomaly_score > 0.8 ? 'Critical' : 'Warning'}
                    </span>
                    <span className="text-xs text-text-muted font-medium">
                      {new Date(inc.detected_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                  <p className="text-sm text-text-main leading-relaxed mb-4">{inc.description}</p>
                  
                  <button 
                    onClick={() => handleExplain(inc)}
                    className="w-full bg-background border border-border group-hover:border-primary/50 text-xs font-bold text-text-muted group-hover:text-primary py-2 rounded-lg flex items-center justify-center gap-2 transition-all duration-300 active:scale-95"
                  >
                    <BrainCircuit size={14} /> 
                    <span>Request AI Analysis</span>
                  </button>
                </div>
              ))
            )}
          </div>
        </motion.div>
      </div>

      <AiAnalysisModal 
        isOpen={!!selectedIncident}
        onClose={() => setSelectedIncident(null)}
        selectedIncident={selectedIncident}
        isAnalyzing={isAnalyzing}
        aiAnalysis={aiAnalysis}
      />
    </div>
  );
};

export default Dashboard;
