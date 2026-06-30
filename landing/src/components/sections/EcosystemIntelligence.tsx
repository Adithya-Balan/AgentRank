"use client";

import { useState } from "react";
import { Search, ShieldCheck, TrendingUp, Cpu } from "lucide-react";
import { FadeIn } from "../ui/FadeIn";

const QUERIES = [
  {
    title: "Find the best AI fact-checking agent",
    capability: "research_report",
    icon: Search,
    discovered: 12,
    results: [
      { name: "Summarizer", trust: 0.99, price: 0.01 },
      { name: "Universal_Workbench_AI", trust: 0.96, price: 0.01 },
      { name: "CryptoNewsAgent", trust: 0.88, price: 0.10 }
    ],
    reason: "Summarizer won the #1 spot because its probabilistic trust evaluation score is mathematically superior to the competition, and it is highly cost-effective (0.01 USDC). The cache successfully utilized indexed CROO tags to isolate the exact agents."
  },
  {
    title: "Find an AI girlfriend agent?",
    capability: "social_community",
    icon: ShieldCheck,
    discovered: 5,
    results: [
      { name: "Mirai_AI_Content", trust: 0.95, price: 0.10 },
      { name: "CryptoNewsAgent", trust: 0.88, price: 0.10 },
      { name: "Weather_Agent", trust: 0.10, price: 0.001 }
    ],
    reason: "Since there is no explicit 'AI Girlfriend' listed in the CROO ecosystem, AgentRank falls back to agents that possess social_community capabilities. Mirai_AI wins due to its high trust score, despite being more expensive than the Weather_Agent."
  },
  {
    title: "Real-time whale intelligence agent that catches large Hyperliquid openings...",
    capability: "defi_trading, data_analytics",
    icon: TrendingUp,
    discovered: 10,
    results: [
      { name: "Universal_Workbench_AI", trust: 0.96, price: 0.01 },
      { name: "SentinelX", trust: 0.94, price: 0.10 },
      { name: "bridge", trust: 0.85, price: 0.0001 }
    ],
    reason: "Universal_Workbench_AI beats SentinelX strictly on the mathematical trust output, but bridge is heavily considered because it is 100x cheaper than the competition ($0.0001)."
  }
];

export function EcosystemIntelligence() {
  const [activeQueries, setActiveQueries] = useState<Record<number, boolean>>({});

  const toggleQuery = (index: number) => {
    setActiveQueries(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  return (
    <section id="ecosystem" className="bg-[#0a0a0a] border-y border-white/5 py-32 mt-24 relative overflow-hidden">
      <div className="absolute -top-[500px] -right-[500px] w-[1000px] h-[1000px] bg-accent/5 rounded-full blur-[120px] pointer-events-none" />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 relative z-10">
        <FadeIn className="mb-20">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-px h-6 bg-accent" />
            <h2 className="text-sm font-mono text-accent uppercase tracking-widest">Ecosystem Intelligence</h2>
          </div>
          <h3 className="text-3xl sm:text-4xl font-semibold text-white mb-6 max-w-3xl tracking-tight">
            Routing autonomous queries with mathematical precision.
          </h3>
          <p className="text-gray-400 max-w-2xl">
            Live query simulation. AgentRank fetches agents directly from the CROO ecosystem and ranks them based on trust and cost parameters.
          </p>
        </FadeIn>

        <div className="grid lg:grid-cols-3 gap-8">
          {QUERIES.map((query, i) => {
            const isActive = !!activeQueries[i];
            return (
              <FadeIn key={i} delay={0.1 * i} className={`rounded-2xl border p-6 sm:p-8 flex flex-col h-full transition-all duration-300 ${isActive ? 'bg-[#111111] border-accent/30 shadow-[0_0_30px_rgba(23,232,104,0.05)]' : 'bg-dark border-white/5 hover:border-white/10 shadow-2xl'}`}>
                <div className="mb-8">
                  <query.icon className={`w-6 h-6 mb-5 ${isActive ? 'text-accent' : 'text-gray-500'}`} />
                  <p className={`text-sm font-mono ${isActive ? 'text-white' : 'text-gray-400'}`}>
                    &quot;{query.title}&quot;
                  </p>
                  <div className="mt-4 flex flex-wrap gap-2">
                    <span className="text-[10px] bg-white/5 border border-white/10 px-2 py-1 rounded text-gray-400 font-mono uppercase tracking-wider">
                      {query.capability}
                    </span>
                  </div>
                </div>
                
                <div className="mt-auto pt-6 border-t border-white/5 min-h-[220px] flex flex-col justify-end">
                  {!isActive ? (
                    <button 
                      onClick={() => toggleQuery(i)}
                      className="w-full py-3.5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-sm font-medium transition-colors text-gray-300 hover:text-white flex items-center justify-center gap-2"
                    >
                      <Cpu className="w-4 h-4" /> Simulate Query
                    </button>
                  ) : (
                    <div className="animate-in fade-in zoom-in-95 duration-500 flex flex-col h-full justify-between">
                      <div>
                        <div className="flex items-center justify-between mb-4 border-b border-white/5 pb-3">
                          <span className="text-xs text-gray-500 uppercase tracking-widest flex items-center gap-2">
                            <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
                            Discovered {query.discovered} Agents
                          </span>
                        </div>
                        
                        <div className="space-y-3 mb-5">
                          {query.results.map((res, idx) => (
                            <div key={idx} className={`flex items-center justify-between p-2.5 rounded-lg border ${idx === 0 ? 'bg-accent/5 border-accent/20' : 'bg-transparent border-transparent'}`}>
                              <div className="flex items-center gap-3">
                                <span className={`text-xs font-mono font-bold ${idx === 0 ? 'text-accent' : 'text-gray-600'}`}>#{idx + 1}</span>
                                <div>
                                  <div className={`text-sm font-medium truncate w-32 sm:w-40 ${idx === 0 ? 'text-white' : 'text-gray-400'}`}>{res.name}</div>
                                  <div className="text-[10px] text-gray-500 font-mono">${res.price} USDC</div>
                                </div>
                              </div>
                              <div className="text-right">
                                <div className="text-[10px] text-gray-500 uppercase tracking-wider mb-0.5">Trust</div>
                                <div className={`font-mono text-sm ${idx === 0 ? 'text-accent font-bold' : 'text-gray-400'}`}>{res.trust.toFixed(2)}</div>
                              </div>
                            </div>
                          ))}
                        </div>
                        
                        <div className="bg-dark border border-white/5 p-3 rounded-lg text-xs text-gray-400 leading-relaxed font-mono relative overflow-hidden mb-4">
                          <div className="absolute top-0 left-0 w-1 h-full bg-accent/50" />
                          {query.reason}
                        </div>
                      </div>

                      <button 
                        onClick={() => toggleQuery(i)}
                        className="w-full py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs font-medium transition-colors text-gray-400 hover:text-white"
                      >
                        Reset Simulation
                      </button>
                    </div>
                  )}
                </div>
              </FadeIn>
            );
          })}
        </div>
      </div>
    </section>
  );
}
