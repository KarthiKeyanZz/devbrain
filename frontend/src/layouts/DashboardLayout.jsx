import React from 'react';
import { LayoutDashboard, AlertCircle, Settings, FileText, Bell, Search } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const SidebarItem = ({ icon: Icon, label, path }) => {
  const location = useLocation();
  const active = location.pathname === path;
  
  return (
    <Link to={path} className={`flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer transition-colors ${active ? 'bg-primary/20 text-primary-light' : 'text-text-muted hover:bg-surface hover:text-text-main'}`}>
      <Icon className="w-5 h-5" />
      <span className="font-medium">{label}</span>
    </Link>
  );
};

const DashboardLayout = ({ children }) => {
  return (
    <div className="flex h-screen bg-background text-text-main overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-surface flex flex-col h-full hidden md:flex">
        <div className="p-6 border-b border-border">
          <div className="flex items-center gap-2 text-primary-light font-bold text-xl tracking-tight">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-white">
              <LayoutDashboard size={18} />
            </div>
            DevBrain
          </div>
        </div>
        
        <div className="flex-1 overflow-y-auto py-6 px-4 space-y-2">
          <SidebarItem icon={LayoutDashboard} label="Dashboard" path="/" />
          <SidebarItem icon={FileText} label="Logs Viewer" path="/logs" />
          <SidebarItem icon={AlertCircle} label="Incidents" path="/incidents" />
          <SidebarItem icon={Settings} label="Settings" path="/settings" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full relative">
        {/* Header */}
        <header className="h-16 border-b border-border bg-background/80 backdrop-blur-md flex items-center justify-between px-8 z-10">
          <div className="flex items-center gap-4 bg-surface border border-border rounded-lg px-4 py-2 w-96">
            <Search size={18} className="text-text-muted" />
            <input 
              type="text" 
              placeholder="Search logs, anomalies, or services..." 
              className="bg-transparent border-none outline-none text-sm w-full text-text-main placeholder-text-muted"
            />
          </div>
          
          <div className="flex items-center gap-4">
            <button className="relative p-2 rounded-full hover:bg-surface text-text-muted hover:text-text-main transition-colors">
              <Bell size={20} />
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-danger animate-pulse-slow"></span>
            </button>
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary to-primary-light border-2 border-border cursor-pointer"></div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-y-auto p-8 relative">
          {/* Subtle background glow effect */}
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-primary/5 rounded-full blur-[100px] pointer-events-none"></div>
          {children}
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
