import React, { useState, useEffect } from 'react';
import { Activity, AlertTriangle, CheckCircle, Database, Server, Zap, X, BrainCircuit, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { getIncidents, explainIncident } from '../services/api';

const MetricCard = ({ title, value, unit, icon: Icon, trend, colorClass }) => (
  <div className="glass-panel p-6 flex flex-col relative overflow-hidden group">
    <div className={`absolute -right-6 -top-6 w-24 h-24 rounded-full opacity-10 ${colorClass} transition-transform group-hover:scale-150 duration-500`}></div>
    <div className="flex justify-between items-start mb-4">
      <div className={`p-3 rounded-xl ${colorClass} bg-opacity-20`}>
        <Icon className={`w-6 h-6 ${colorClass.replace('bg-', 'text-')}`} />
      </div>
      {trend && (
        <span className={`text-sm font-medium px-2 py-1 rounded-full ${trend > 0 ? 'bg-danger/10 text-danger' : 'bg-success/10 text-success'}`}>
          {trend > 0 ? '+' : ''}{trend}%
        </span>
      )}
    </div>
    <h3 className="text-text-muted font-medium text-sm mb-1">{title}</h3>
    <div className="flex items-baseline gap-1">
      <span className="text-3xl font-bold text-text-main">{value}</span>
      {unit && <span className="text-text-muted font-medium">{unit}</span>}
    </div>
  </div>
);

const Dashboard = () => {
  const [incidents, setIncidents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedIncident, setSelectedIncident] = useState(null);
  const [aiAnalysis, setAiAnalysis] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    fetchIncidents();
    const interval = setInterval(fetchIncidents, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchIncidents = async () => {
    try {
      const data = await getIncidents();
      setIncidents(data.anomalies || []);
    } catch (error) {
      console.error("Failed to fetch incidents", error);
    } finally {
      setLoading(false);
    }
  };

  const handleExplain = async (incident) => {
    setSelectedIncident(incident);
    setIsAnalyzing(true);
    setAiAnalysis(null);
    try {
      // Send the incident to the AI core
      const analysis = await explainIncident(incident.service_id, incident.description);
      setAiAnalysis(analysis);
    } catch (error) {
      console.error("AI Analysis failed", error);
      setAiAnalysis({ summary: "Analysis failed to reach AI Core.", root_causes: [], recommendations: [] });
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="space-y-8 z-10 relative">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold tracking-tight mb-2">Platform Overview</h1>
          <p className="text-text-muted">Real-time observability and anomaly detection.</p>
        </div>
        <div className="flex gap-2">
          <div className="px-3 py-1.5 rounded-full bg-success/10 text-success text-sm font-medium border border-success/20 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-success animate-pulse"></span>
            System Healthy
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard title="Total Logs (24h)" value="1.2" unit="M" icon={Database} trend={+12} colorClass="bg-primary" />
        <MetricCard title="Active Anomalies" value={incidents.length.toString()} icon={AlertTriangle} trend={incidents.length > 0 ? +5 : -2} colorClass={incidents.length > 0 ? "bg-danger" : "bg-success"} />
        <MetricCard title="Avg Latency" value="124" unit="ms" icon={Zap} trend={-8} colorClass="bg-warning" />
        <MetricCard title="Monitored Services" value="5" icon={Server} colorClass="bg-primary-light" />
      </div>

      {/* Incidents Table */}
      <div className="glass-panel overflow-hidden">
        <div className="p-6 border-b border-border flex justify-between items-center">
          <h2 className="text-xl font-semibold flex items-center gap-2">
            <Activity className="text-primary-light" />
            Recent Incidents
          </h2>
          <button className="text-sm text-primary hover:text-primary-light font-medium transition-colors" onClick={fetchIncidents}>
            Refresh
          </button>
        </div>
        
        <div className="overflow-x-auto">
          {loading ? (
            <div className="p-8 text-center text-text-muted animate-pulse">Loading real-time telemetry...</div>
          ) : incidents.length === 0 ? (
            <div className="p-12 text-center flex flex-col items-center">
              <CheckCircle className="w-12 h-12 text-success mb-3 opacity-50" />
              <h3 className="text-lg font-medium text-text-main mb-1">No Active Incidents</h3>
              <p className="text-text-muted">All systems are operating normally.</p>
            </div>
          ) : (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-surface/50 text-text-muted text-sm border-b border-border">
                  <th className="px-6 py-4 font-medium">Severity</th>
                  <th className="px-6 py-4 font-medium">Description</th>
                  <th className="px-6 py-4 font-medium">Time Detected</th>
                  <th className="px-6 py-4 font-medium">Action</th>
                </tr>
              </thead>
              <tbody>
                {incidents.slice(0, 5).map((inc) => {
                  const severity = inc.anomaly_score > 0.8 ? 'CRITICAL' : inc.anomaly_score > 0.5 ? 'HIGH' : 'WARNING';
                  return (
                  <tr key={inc.id} className="border-b border-border hover:bg-surface/30 transition-colors">
                    <td className="px-6 py-4">
                      <span className={`px-2.5 py-1 rounded-md text-xs font-medium border ${
                        severity === 'CRITICAL' ? 'bg-danger/10 text-danger border-danger/20' : 
                        severity === 'HIGH' ? 'bg-warning/10 text-warning border-warning/20' : 
                        'bg-primary/10 text-primary border-primary/20'
                      }`}>
                        {severity}
                      </span>
                    </td>
                    <td className="px-6 py-4 font-medium text-text-main max-w-md truncate">
                      {inc.description}
                    </td>
                    <td className="px-6 py-4 text-text-muted text-sm">
                      {new Date(inc.detected_at).toLocaleTimeString()}
                    </td>
                    <td className="px-6 py-4">
                      <button 
                        onClick={() => handleExplain(inc)}
                        className="btn-primary text-sm py-1.5 px-3 flex items-center gap-2"
                      >
                        <BrainCircuit size={14} /> Explain 
                      </button>
                    </td>
                  </tr>
                )})}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* AI Analysis Modal */}
      <AnimatePresence>
        {selectedIncident && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div 
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="absolute inset-0 bg-background/80 backdrop-blur-sm"
              onClick={() => setSelectedIncident(null)}
            />
            
            <motion.div 
              initial={{ scale: 0.95, opacity: 0, y: 20 }}
              animate={{ scale: 1, opacity: 1, y: 0 }}
              exit={{ scale: 0.95, opacity: 0, y: 20 }}
              className="glass-panel w-full max-w-2xl relative z-10 overflow-hidden flex flex-col max-h-[85vh]"
            >
              {/* Modal Header */}
              <div className="p-6 border-b border-border flex justify-between items-start bg-gradient-to-r from-primary/10 to-transparent">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <BrainCircuit className="text-primary-light" />
                    <h2 className="text-xl font-bold">AI Root Cause Analysis</h2>
                  </div>
                  <p className="text-text-muted text-sm">Target: <span className="font-medium text-text-main">{selectedIncident.description}</span></p>
                </div>
                <button onClick={() => setSelectedIncident(null)} className="text-text-muted hover:text-white p-1 rounded-full hover:bg-surface transition-colors">
                  <X size={20} />
                </button>
              </div>

              {/* Modal Body */}
              <div className="p-6 overflow-y-auto">
                {isAnalyzing ? (
                  <div className="flex flex-col items-center justify-center py-12">
                    <Loader2 className="w-10 h-10 text-primary animate-spin mb-4" />
                    <h3 className="text-lg font-medium mb-2">ML Engine Analyzing...</h3>
                    <p className="text-text-muted text-sm text-center max-w-xs">Running Isolation Forest models and deep log embeddings to determine the exact root cause.</p>
                  </div>
                ) : aiAnalysis ? (
                  <div className="space-y-6">
                    <div className="bg-surface/50 border border-border rounded-xl p-5">
                      <h4 className="text-sm font-semibold text-primary-light uppercase tracking-wider mb-2">Summary</h4>
                      <p className="text-text-main">{aiAnalysis.summary}</p>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-semibold flex items-center gap-2 mb-3">
                        <AlertTriangle size={16} className="text-warning" />
                        Probable Root Causes
                      </h4>
                      <ul className="space-y-2">
                        {aiAnalysis.root_causes && aiAnalysis.root_causes.length > 0 ? (
                           aiAnalysis.root_causes.map((cause, idx) => (
                             <li key={idx} className="flex gap-3 text-sm text-text-muted bg-surface/30 p-3 rounded-lg border border-border/50">
                               <span className="w-5 h-5 rounded-full bg-border flex items-center justify-center text-xs font-bold shrink-0">{idx + 1}</span>
                               {cause}
                             </li>
                           ))
                        ) : (
                          <li className="text-text-muted italic text-sm">No specific root causes identified.</li>
                        )}
                      </ul>
                    </div>
                    
                    <div>
                      <h4 className="text-sm font-semibold flex items-center gap-2 mb-3">
                        <CheckCircle size={16} className="text-success" />
                        Recommended Actions
                      </h4>
                      <div className="grid gap-2">
                        {aiAnalysis.recommendations && aiAnalysis.recommendations.length > 0 ? (
                           aiAnalysis.recommendations.map((rec, idx) => (
                             <div key={idx} className="bg-success/5 border border-success/10 rounded-lg p-3 text-sm flex items-start gap-3">
                               <div className="mt-0.5 w-1.5 h-1.5 rounded-full bg-success shrink-0"></div>
                               <span className="text-text-main">{rec}</span>
                             </div>
                           ))
                        ) : (
                          <div className="text-text-muted italic text-sm">No recommendations available.</div>
                        )}
                      </div>
                    </div>
                  </div>
                ) : null}
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Dashboard;
