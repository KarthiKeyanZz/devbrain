import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BrainCircuit, X, Loader2, AlertTriangle, CheckCircle } from 'lucide-react';

const AiAnalysisModal = ({ isOpen, onClose, selectedIncident, isAnalyzing, aiAnalysis }) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        <motion.div 
          initial={{ opacity: 0 }} 
          animate={{ opacity: 1 }} 
          exit={{ opacity: 0 }}
          className="absolute inset-0 bg-background/80 backdrop-blur-sm"
          onClick={onClose}
        />
        
        <motion.div 
          initial={{ scale: 0.95, opacity: 0, y: 30 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.95, opacity: 0, y: 30 }}
          transition={{ type: "spring", stiffness: 300, damping: 25 }}
          className="glass-panel w-full max-w-3xl relative z-10 overflow-hidden flex flex-col max-h-[85vh] border-primary/40 shadow-[0_0_50px_rgba(102,252,241,0.15)]"
        >
          {/* Header */}
          <div className="p-6 border-b border-border flex justify-between items-start bg-gradient-to-r from-primary/10 to-transparent relative">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary via-secondary to-primary"></div>
            <div>
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/40">
                  <BrainCircuit className="text-primary" />
                </div>
                <h2 className="text-2xl font-bold header-glow">AI Core Analysis</h2>
              </div>
              <p className="text-text-muted text-sm ml-13">Incident Target: <span className="font-medium text-white">{selectedIncident?.description || "Unknown Anomaly"}</span></p>
            </div>
            <button 
              onClick={onClose} 
              className="text-text-muted hover:text-white p-2 rounded-full hover:bg-surfaceHighlight transition-colors"
            >
              <X size={20} />
            </button>
          </div>

          {/* Body */}
          <div className="p-8 overflow-y-auto custom-scrollbar bg-surface/30">
            {isAnalyzing ? (
              <div className="flex flex-col items-center justify-center py-16">
                <div className="relative mb-6">
                  <div className="absolute inset-0 bg-primary/30 rounded-full blur-xl animate-pulse-slow"></div>
                  <Loader2 className="w-14 h-14 text-primary animate-spin relative z-10" />
                </div>
                <h3 className="text-xl font-bold mb-3 header-glow">Deep Learning Pipeline Active</h3>
                <p className="text-text-muted text-sm text-center max-w-sm">Generating embeddings and computing anomaly vectors through the Isolation Forest to determine root cause...</p>
              </div>
            ) : aiAnalysis ? (
              <div className="space-y-8 animate-in fade-in duration-700">
                {/* Summary */}
                <div className="bg-surface border border-border rounded-xl p-6 shadow-inner relative overflow-hidden">
                  <div className="absolute left-0 top-0 bottom-0 w-1 bg-primary"></div>
                  <h4 className="text-xs font-bold text-primary uppercase tracking-widest mb-3">Executive Summary</h4>
                  <p className="text-text-main leading-relaxed">{aiAnalysis.summary}</p>
                </div>
                
                {/* Root Causes */}
                <div>
                  <h4 className="text-sm font-bold flex items-center gap-2 mb-4 text-warning">
                    <AlertTriangle size={18} />
                    Probable Root Vectors
                  </h4>
                  <ul className="space-y-3">
                    {aiAnalysis.root_causes && aiAnalysis.root_causes.length > 0 ? (
                        aiAnalysis.root_causes.map((cause, idx) => (
                          <li key={idx} className="flex gap-4 text-sm text-text-muted bg-background/50 p-4 rounded-xl border border-border hover:border-warning/30 transition-colors">
                            <span className="w-6 h-6 rounded-full bg-warning/10 border border-warning/20 flex items-center justify-center text-xs font-bold shrink-0 text-warning">{idx + 1}</span>
                            <span className="mt-0.5">{cause}</span>
                          </li>
                        ))
                    ) : (
                      <li className="text-text-muted italic text-sm p-4 bg-background/50 rounded-xl border border-border">No specific divergent vectors identified.</li>
                    )}
                  </ul>
                </div>
                
                {/* Recommendations */}
                <div>
                  <h4 className="text-sm font-bold flex items-center gap-2 mb-4 text-success">
                    <CheckCircle size={18} />
                    Remediation Protocol
                  </h4>
                  <div className="grid gap-3">
                    {aiAnalysis.recommendations && aiAnalysis.recommendations.length > 0 ? (
                        aiAnalysis.recommendations.map((rec, idx) => (
                          <div key={idx} className="bg-success/5 border border-success/20 rounded-xl p-4 text-sm flex items-start gap-4 hover:bg-success/10 transition-colors">
                            <div className="mt-1 w-2 h-2 rounded-full bg-success shrink-0 shadow-[0_0_8px_rgba(16,185,129,0.8)]"></div>
                            <span className="text-text-main leading-relaxed">{rec}</span>
                          </div>
                        ))
                    ) : (
                      <div className="text-text-muted italic text-sm p-4 bg-background/50 rounded-xl border border-border">No automated remediation available.</div>
                    )}
                  </div>
                </div>
              </div>
            ) : null}
          </div>
          
          {/* Footer */}
          {!isAnalyzing && aiAnalysis && (
            <div className="p-5 border-t border-border/50 bg-surface/80 flex justify-end gap-3">
              <button className="btn-secondary text-sm py-2 px-4" onClick={onClose}>Dismiss</button>
              <button className="btn-primary text-sm py-2 px-4 shadow-[0_0_10px_rgba(102,252,241,0.3)]">Deploy Fix</button>
            </div>
          )}
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

export default AiAnalysisModal;
