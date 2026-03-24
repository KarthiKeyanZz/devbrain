import React, { useState, useEffect } from 'react';
import { AlertTriangle, Activity, BrainCircuit, ShieldAlert, CheckCircle2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { getIncidents, explainIncident } from '../services/api';
import AiAnalysisModal from '../components/AiAnalysisModal';

const Incidents = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Modal states
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    fetchIncidents();
  }, []);

  const fetchIncidents = async () => {
    try {
      setLoading(true);
      const data = await getIncidents();
      let anoms = data.anomalies || [];
      // Demo mock data if none
      if(anoms.length === 0) {
        anoms = [
          {
            id: 101,
            service_id: 1,
            anomaly_score: 0.92,
            description: "CRITICAL: Isolation Forest detected anomalous latency spike (>3000ms) paired with database connection drops.",
            detected_at: new Date(Date.now() - 600000).toISOString(),
            status: "pending"
          },
          {
            id: 102,
            service_id: 3,
            anomaly_score: 0.65,
            description: "WARN: Unrecognized log vector sequences in the authentication module.",
            detected_at: new Date(Date.now() - 3600000).toISOString(),
            status: "analyzed"
          }
        ];
      }
      setIncidents(anoms);
    } catch (e) {
      console.error(e);
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

  return (
    <div className="space-y-6 relative h-full flex flex-col">
      <div className="flex justify-between items-end">
        <motion.div initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5 }}>
          <h1 className="text-4xl font-extrabold tracking-tight mb-2 header-glow inline-block text-warning">Incident Intelligence</h1>
          <p className="text-text-muted text-lg">Review detected anomalies and run deep-learning root cause analysis.</p>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 flex-1">
        {/* Statistics Column */}
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5, delay: 0.1 }} className="lg:col-span-1 space-y-6">
          <div className="glass-panel p-8 text-center flex flex-col justify-center border-danger/20 shadow-[0_0_20px_rgba(239,68,68,0.1)]">
            <ShieldAlert className="w-16 h-16 text-danger mx-auto mb-4 opacity-80 animate-pulse-slow" />
            <h3 className="text-text-muted font-bold tracking-widest uppercase mb-2">Pending Criticals</h3>
            <span className="text-6xl font-black text-white">{incidents.filter(i => i.anomaly_score > 0.8).length}</span>
          </div>

          <div className="glass-panel p-6 border-success/20">
            <h3 className="text-text-muted font-bold uppercase tracking-wide mb-4 flex items-center gap-2">
              <CheckCircle2 className="text-success" size={18} /> Resolvability Scope
            </h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-white">AI Confidence Vector</span>
                  <span className="text-primary font-bold">94%</span>
                </div>
                <div className="w-full bg-surface rounded-full h-2">
                  <div className="bg-primary h-2 rounded-full shadow-[0_0_10px_rgba(102,252,241,0.5)]" style={{ width: '94%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-white">Auto-remediation Coverage</span>
                  <span className="text-success font-bold">67%</span>
                </div>
                <div className="w-full bg-surface rounded-full h-2">
                  <div className="bg-success h-2 rounded-full shadow-[0_0_10px_rgba(16,185,129,0.5)]" style={{ width: '67%' }}></div>
                </div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Incidents Feed */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.2 }} className="lg:col-span-2 glass-panel flex flex-col overflow-hidden">
          <div className="p-6 border-b border-border bg-gradient-to-r from-surfaceHighlight to-transparent">
            <h2 className="text-xl font-bold flex items-center gap-3">
              <Activity className="text-primary" /> Active Divergence Feed
            </h2>
          </div>
          
          <div className="flex-1 overflow-y-auto p-2 custom-scrollbar space-y-1">
            {incidents.map((inc) => {
              const critical = inc.anomaly_score > 0.8;
              return (
                <div key={inc.id} className="p-5 border-b border-border/40 hover:bg-surface/60 transition-colors group flex gap-5 items-start">
                  <div className={`mt-1 p-2 rounded-xl ${critical ? 'bg-danger/20 text-danger border border-danger/30 shadow-[0_0_10px_rgba(239,68,68,0.3)]' : 'bg-warning/20 text-warning border border-warning/30 shadow-[0_0_10px_rgba(245,158,11,0.3)]'}`}>
                    <AlertTriangle size={24} />
                  </div>
                  
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <span className={`px-2.5 py-1 rounded text-xs font-bold uppercase tracking-wider ${critical ? 'bg-danger text-white' : 'bg-warning text-background'}`}>
                        {critical ? 'Level 1: Critical' : 'Level 2: Warning'}
                      </span>
                      <span className="text-text-muted text-sm font-mono">{new Date(inc.detected_at).toLocaleString()}</span>
                      <span className="text-text-muted text-sm ml-auto opacity-50">Score: {inc.anomaly_score.toFixed(2)}</span>
                    </div>
                    
                    <p className="text-white font-medium mb-3 text-lg leading-snug">{inc.description}</p>
                    
                    <div className="flex items-center gap-3">
                      <button 
                        onClick={() => handleExplain(inc)}
                        className="bg-primary/10 hover:bg-primary/20 border border-primary/30 text-primary hover:text-white px-5 py-2 rounded-lg font-bold text-sm flex items-center gap-2 transition-all shadow-[0_0_10px_rgba(102,252,241,0.1)] active:scale-95"
                      >
                        <BrainCircuit size={16} /> Execute Neural Analysis
                      </button>
                      <button className="text-text-muted hover:text-white text-sm px-4 py-2 transition-colors">Acknowledge</button>
                    </div>
                  </div>
                </div>
              )
            })}
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

export default Incidents;
