import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="glass-panel p-4 text-sm font-medium shadow-[0_0_15px_rgba(102,252,241,0.2)] border-primary/30">
        <p className="text-text-muted mb-2 border-b border-border/50 pb-2">{label}</p>
        {payload.map((entry, index) => (
          <div key={index} className="flex items-center gap-3 mt-1">
            <div className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: entry.color }}></div>
            <p className="text-white capitalize">{entry.name}: <span className="font-bold text-primary">{entry.value}</span></p>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

const ChartWidget = ({ title, data, dataKey = "value", lines = [], height = 300 }) => {
  return (
    <div className="glass-panel p-6 flex flex-col h-full w-full">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-bold text-white flex items-center gap-2">
          {title}
          <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
        </h3>
      </div>
      
      <div className="flex-1 w-full" style={{ height: height }}>
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <defs>
              {lines.map((line, idx) => (
                <linearGradient key={`colorUv${idx}`} id={`colorUv${idx}`} x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor={line.color} stopOpacity={0.4}/>
                  <stop offset="95%" stopColor={line.color} stopOpacity={0}/>
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(197, 198, 199, 0.1)" vertical={false} />
            <XAxis 
              dataKey="time" 
              stroke="#A1A1AA" 
              fontSize={12} 
              tickLine={false} 
              axisLine={false}
              dy={10}
            />
            <YAxis 
              stroke="#A1A1AA" 
              fontSize={12} 
              tickLine={false} 
              axisLine={false} 
              tickFormatter={(value) => value >= 1000 ? `${(value / 1000).toFixed(1)}k` : value}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ stroke: 'rgba(102, 252, 241, 0.2)', strokeWidth: 1, strokeDasharray: '4 4' }} />
            
            {lines.map((line, idx) => (
              <Area 
                key={idx}
                type="monotone" 
                dataKey={line.key} 
                name={line.name}
                stroke={line.color} 
                strokeWidth={3}
                fillOpacity={1} 
                fill={`url(#colorUv${idx})`} 
                activeDot={{ r: 6, fill: line.color, stroke: '#0B0C10', strokeWidth: 2, className: "drop-shadow-[0_0_8px_rgba(102,252,241,0.8)]" }}
              />
            ))}
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default ChartWidget;
