import React from 'react';
import { LayoutDashboard, AlertCircle, Settings, FileText, Bell, Search, ActivitySquare } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';

const SidebarItem = ({ icon: Icon, label, path }) => {
  const location = useLocation();
  const active = location.pathname === path;
  
  return (
    <Link to={path} className={`relative flex items-center gap-4 px-5 py-3.5 rounded-xl cursor-pointer transition-all duration-300 group overflow-hidden ${active ? 'text-primary' : 'text-text-muted hover:text-white'}`}>
      {active && (
        <motion.div 
          layoutId="activeTab"
          className="absolute inset-0 bg-primary/10 border border-primary/20 rounded-xl"
          transition={{ type: "spring", stiffness: 300, damping: 30 }}
        />
      )}
      <Icon className={`w-5 h-5 relative z-10 transition-transform duration-300 ${active ? 'scale-110 drop-shadow-[0_0_8px_rgba(102,252,241,0.8)]' : 'group-hover:scale-110'}`} />
      <span className={`font-medium relative z-10 ${active ? 'drop-shadow-[0_0_8px_rgba(102,252,241,0.5)]' : ''}`}>{label}</span>
      
      {/* Hover glow effect background */}
      {!active && <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-xl"></div>}
    </Link>
  );
};

const DashboardLayout = ({ children }) => {
  return (
    <div className="flex h-screen bg-transparent text-text-main overflow-hidden relative">
      <div className="absolute top-[-100px] left-[-100px] w-96 h-96 bg-primary/20 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-100px] right-[-100px] w-96 h-96 bg-secondary/20 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Sidebar */}
      <aside className="w-72 glass-panel border-r border-border flex flex-col h-[calc(100vh-2rem)] my-4 ml-4 hidden md:flex relative z-20">
        <div className="p-8 border-b border-border/50">
          <Link to="/" className="flex items-center gap-3 text-white font-bold text-2xl tracking-tight group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center text-background shadow-[0_0_15px_rgba(102,252,241,0.5)] group-hover:shadow-[0_0_25px_rgba(102,252,241,0.8)] transition-all duration-300">
              <ActivitySquare size={22} />
            </div>
            DevBrain<span className="text-primary">.ai</span>
          </Link>
        </div>
        
        <div className="flex-1 overflow-y-auto py-8 px-5 space-y-2">
          <SidebarItem icon={LayoutDashboard} label="Dashboard" path="/" />
          <SidebarItem icon={FileText} label="Logs Explorer" path="/logs" />
          <SidebarItem icon={AlertCircle} label="Incidents Feed" path="/incidents" />
          <SidebarItem icon={Settings} label="Settings" path="/settings" />
        </div>
        
        <div className="p-6 border-t border-border/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-primary to-secondary p-[2px]">
              <div className="w-full h-full bg-background rounded-full border-2 border-transparent"></div>
            </div>
            <div>
              <p className="text-sm font-semibold text-white">System Admin</p>
              <p className="text-xs text-primary">Connected</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen relative z-10 w-full overflow-hidden">
        {/* Header */}
        <header className="h-24 flex items-center justify-between px-10 relative z-30">
          <div className="flex items-center gap-4 glass-panel px-5 py-3 w-96 group focus-within:border-primary/50 focus-within:shadow-[0_0_15px_rgba(102,252,241,0.2)] transition-all duration-300">
            <Search size={18} className="text-text-muted group-focus-within:text-primary transition-colors" />
            <input 
              type="text" 
              placeholder="Query logs, search anomalies..." 
              className="bg-transparent border-none outline-none text-sm w-full text-text-main placeholder-text-muted/70 selection:bg-primary/50"
            />
          </div>
          
          <div className="flex items-center gap-5">
            <button className="relative w-12 h-12 rounded-xl glass-panel-interactive flex items-center justify-center text-text-muted hover:text-white transition-colors">
              <Bell size={20} />
              <span className="absolute top-3 right-3 w-2.5 h-2.5 rounded-full bg-danger animate-pulse shadow-[0_0_10px_rgba(239,68,68,0.8)] border-2 border-surface"></span>
            </button>
            <button className="btn-primary text-sm shadow-md">
              Deploy Model
            </button>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-y-auto px-10 pb-10 relative scroll-smooth">
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
