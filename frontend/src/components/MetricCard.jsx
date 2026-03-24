import React from 'react';
import { motion } from 'framer-motion';

const MetricCard = ({ title, value, unit, icon: Icon, trend, colorClass = "primary" }) => {
  // Map color words to tailwind colors for inline styles or classes
  const colorMap = {
    primary: 'var(--tw-colors-primary-DEFAULT)',
    secondary: 'var(--tw-colors-secondary-DEFAULT)',
    success: 'var(--tw-colors-success)',
    warning: 'var(--tw-colors-warning)',
    danger: 'var(--tw-colors-danger)',
  };

  const cssColor = colorMap[colorClass] || colorMap.primary;

  return (
    <motion.div 
      whileHover={{ y: -5, scale: 1.02 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
      className="glass-panel p-6 flex flex-col relative overflow-hidden group cursor-pointer"
    >
      {/* Background glowing orb */}
      <div 
        className="absolute -right-6 -top-6 w-32 h-32 rounded-full opacity-20 blur-2xl transition-transform group-hover:scale-150 duration-700"
        style={{ backgroundColor: cssColor }}
      ></div>
      
      {/* Shine effect on hover */}
      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 bg-gradient-to-tr from-white/0 via-white/5 to-white/0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000"></div>

      <div className="flex justify-between items-start mb-6 relative z-10">
        <div 
          className="p-3.5 rounded-2xl bg-surface/80 border border-white/5 shadow-md group-hover:shadow-[0_0_15px_rgba(255,255,255,0.1)] transition-all duration-300"
          style={{ 
            boxShadow: `inset 0 0 15px ${cssColor}20`,
            borderColor: `${cssColor}40`
          }}
        >
          <Icon size={24} style={{ color: cssColor }} className="drop-shadow-md" />
        </div>
        {trend !== undefined && (
          <div className={`flex items-center gap-1 font-bold text-sm px-3 py-1.5 rounded-full backdrop-blur-md border ${trend > 0 ? 'bg-danger/10 text-danger border-danger/20 shadow-[0_0_10px_rgba(239,68,68,0.2)]' : trend < 0 ? 'bg-success/10 text-success border-success/20 shadow-[0_0_10px_rgba(16,185,129,0.2)]' : 'bg-surface text-text-muted border-border'}`}>
             {trend > 0 ? '+' : ''}{trend}%
          </div>
        )}
      </div>
      
      <div className="relative z-10 flex-col flex">
        <h3 className="text-text-muted font-medium text-sm mb-2 uppercase tracking-wider">{title}</h3>
        <div className="flex items-baseline gap-1">
          <span className="text-4xl font-extrabold text-white tracking-tight drop-shadow-md">{value}</span>
          {unit && <span className="text-text-muted font-bold ml-1">{unit}</span>}
        </div>
      </div>
    </motion.div>
  );
};

export default MetricCard;
