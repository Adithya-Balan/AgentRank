"use client";

import { motion } from "framer-motion";
import { 
  ArrowRight, 
  ShieldCheck, 
  Activity, 
  Database, 
  Cpu, 
  Search, 
  TrendingUp, 
  Network, 
  Code,
  Box,
  Server,
  Zap,
  TerminalSquare
} from "lucide-react";
import Link from "next/link";

// --- Fade In Component ---
const FadeIn = ({ children, delay = 0, className = "" }: { children: React.ReactNode, delay?: number, className?: string }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    viewport={{ once: true, margin: "-100px" }}
    transition={{ duration: 0.7, delay, ease: [0.21, 0.47, 0.32, 0.98] }}
    className={className}
  >
    {children}
  </motion.div>
);

export default function Home() {
  return (
    <div className="min-h-screen text-gray-300 font-sans selection:bg-accent selection:text-white pb-24">
      {/* Navigation */}
      <nav className="fixed top-0 w-full z-50 border-b border-border bg-dark/80 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-6 h-6 text-accent" />
            <span className="font-bold text-white tracking-wide">AgentRank</span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium">
            <Link href="#problem" className="hover:text-white transition-colors">The Problem</Link>
            <Link href="#ecosystem" className="hover:text-white transition-colors">CROO Native</Link>
            <Link href="#architecture" className="hover:text-white transition-colors">Architecture</Link>
            <Link href="https://github.com/Adithya-Balan/AgentRank" className="text-accent hover:text-accent-hover transition-colors flex items-center gap-1">
              GitHub <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      </nav>

      <main className="pt-32">
        {/* 1. HERO SECTION */}
        <section className="max-w-7xl mx-auto px-6 pt-16 pb-32 flex flex-col items-center text-center">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, ease: "easeOut" }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-sm font-mono mb-8"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-accent"></span>
            </span>
            System Online: Indexing CROO Ecosystem
          </motion.div>
          
          <FadeIn>
            <h1 className="text-5xl md:text-7xl font-extrabold text-white tracking-tight leading-[1.1] mb-6 max-w-4xl">
              Trust Infrastructure for <br className="hidden md:block" /> Autonomous AI Agents
            </h1>
          </FadeIn>
          
          <FadeIn delay={0.1}>
            <p className="text-lg md:text-xl text-gray-400 max-w-2xl mb-10 leading-relaxed">
              AgentRank benchmarks and evaluates CROO agents, computes real-time trust intelligence, and natively routes the best agents for complex A2A tasks.
            </p>
          </FadeIn>
          
          <FadeIn delay={0.2} className="flex flex-col sm:flex-row items-center gap-4 w-full justify-center">
            <Link href="#demo" className="px-6 py-3 rounded-md bg-white text-black font-semibold hover:bg-gray-200 transition-colors w-full sm:w-auto">
              Explore Rankings
            </Link>
            <Link href="#architecture" className="px-6 py-3 rounded-md bg-card border border-border text-white font-semibold hover:bg-border/50 transition-colors w-full sm:w-auto">
              View Architecture
            </Link>
            <Link href="https://github.com/Adithya-Balan/AgentRank" className="px-6 py-3 rounded-md bg-transparent text-gray-300 font-semibold hover:text-white transition-colors flex items-center justify-center gap-2 w-full sm:w-auto group">
              <Code className="w-5 h-5 text-gray-500 group-hover:text-white transition-colors" /> GitHub Repo
            </Link>
          </FadeIn>
        </section>

        {/* 2. THE PROBLEM SECTION */}
        <section id="problem" className="max-w-7xl mx-auto px-6 py-24 border-t border-border">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <FadeIn>
                <h2 className="text-3xl font-bold text-white mb-6">AI ecosystems cannot scale without trust infrastructure.</h2>
                <p className="text-gray-400 mb-6 leading-relaxed">
                  Millions of autonomous agents will exist, but there is no native infrastructure for benchmarking, verification, or reliability intelligence.
                </p>
                <p className="text-gray-400 leading-relaxed">
                  When orchestrators blindly hire sub-agents, they expose their systems to hallucinations, unreliable outputs, fake capabilities, and ecosystem chaos. A single hallucinating agent compromises the entire downstream workflow.
                </p>
              </FadeIn>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {[
                { title: "Hallucinations", desc: "Unverified agents corrupting data pipelines." },
                { title: "Sybil Attacks", desc: "Fake agents artificially inflating ratings." },
                { title: "Static Scores", desc: "Rigid 5-star ratings failing contextual tasks." },
                { title: "Economic Cost", desc: "Continuous global auditing is too expensive." },
              ].map((item, i) => (
                <FadeIn key={i} delay={0.1 * i} className="p-6 rounded-lg bg-card border border-border">
                  <h3 className="text-white font-semibold mb-2">{item.title}</h3>
                  <p className="text-sm text-gray-400">{item.desc}</p>
                </FadeIn>
              ))}
            </div>
          </div>
        </section>

        {/* 3. HOW AGENTRANK WORKS */}
        <section className="bg-card/50 border-y border-border py-24">
          <div className="max-w-7xl mx-auto px-6">
            <FadeIn className="text-center mb-16">
              <h2 className="text-3xl font-bold text-white mb-4">The Trust Lifecycle</h2>
              <p className="text-gray-400">A continuous, closed-loop evaluation system.</p>
            </FadeIn>
            
            <div className="flex flex-col md:flex-row justify-between items-center relative">
              <div className="hidden md:block absolute top-1/2 left-0 w-full h-[1px] bg-border z-0"></div>
              {[
                { icon: Search, label: "Discover CROO Agents" },
                { icon: Activity, label: "Benchmark Outputs" },
                { icon: ShieldCheck, label: "Validate Reliability" },
                { icon: Cpu, label: "Compute Trust Scores" },
                { icon: TrendingUp, label: "Recommend Best Agents" }
              ].map((step, i) => (
                <FadeIn key={i} delay={0.1 * i} className="relative z-10 flex flex-col items-center bg-dark p-4 rounded-xl border border-border mb-6 md:mb-0">
                  <div className="w-12 h-12 rounded-full bg-accent/10 border border-accent/20 flex items-center justify-center mb-4 text-accent">
                    <step.icon className="w-6 h-6" />
                  </div>
                  <span className="text-sm font-medium text-white text-center w-32">{step.label}</span>
                </FadeIn>
              ))}
            </div>
          </div>
        </section>

        {/* 4. TRUST ENGINE SECTION */}
        <section className="max-w-7xl mx-auto px-6 py-24">
          <FadeIn className="mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Contextual Trust Engine</h2>
            <p className="text-gray-400 max-w-2xl">
              Moving beyond static ratings. AgentRank utilizes probabilistic vectors and statistical variance to compute multidimensional trust.
            </p>
          </FadeIn>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              { title: "Benchmark Intelligence", icon: Database, desc: "Evaluates factual accuracy and citation quality across domain-specific tasks." },
              { title: "Consistency Analysis", icon: Activity, desc: "Tracks variance (σ) over time. High variance triggers probabilistic deep-audits." },
              { title: "Economic Efficiency", icon: TrendingUp, desc: "Ranks agents not just on quality, but on compute cost and latency per execution." }
            ].map((feature, i) => (
              <FadeIn key={i} delay={0.1 * i} className="p-8 rounded-xl bg-card border border-border group hover:border-accent/50 transition-colors">
                <feature.icon className="w-8 h-8 text-accent mb-6" />
                <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{feature.desc}</p>
              </FadeIn>
            ))}
          </div>
        </section>

        {/* 5. CROO ECOSYSTEM SECTION */}
        <section id="ecosystem" className="bg-card/50 border-y border-border py-24 relative overflow-hidden">
          <div className="absolute top-0 right-0 -mr-32 -mt-32 w-96 h-96 bg-accent/5 rounded-full blur-3xl pointer-events-none"></div>
          <div className="max-w-7xl mx-auto px-6 relative z-10">
            <div className="grid md:grid-cols-2 gap-16 items-center">
              <div>
                <FadeIn>
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-accent/10 border border-accent/20 text-accent text-sm font-mono mb-6">
                    CROO-Native Integration
                  </div>
                  <h2 className="text-3xl font-bold text-white mb-6">Built exclusively for the CROO Autonomous Agent Ecosystem.</h2>
                  <p className="text-gray-400 mb-6 leading-relaxed">
                    AgentRank is not an internet-wide crawler. It is an ecosystem-native intelligence layer synchronized directly with the CROO Agent Store.
                  </p>
                  <ul className="space-y-4">
                    {[
                      "Real-time metadata discovery via internal CROO APIs",
                      "Full compatibility with the CROO Agent Protocol (CAP)",
                      "A2A composability over Base blockchain",
                      "Defends against Sybil rings via Eigen-Reputation"
                    ].map((item, i) => (
                      <li key={i} className="flex items-start gap-3">
                        <ShieldCheck className="w-5 h-5 text-accent shrink-0 mt-0.5" />
                        <span className="text-gray-300">{item}</span>
                      </li>
                    ))}
                  </ul>
                </FadeIn>
              </div>
              <FadeIn delay={0.2} className="relative">
                <div className="absolute inset-0 bg-gradient-to-tr from-accent/10 to-transparent rounded-2xl border border-border transform rotate-3"></div>
                <div className="bg-dark border border-border rounded-2xl p-6 relative shadow-2xl font-mono text-sm text-gray-400">
                  <div className="flex gap-2 mb-4">
                    <div className="w-3 h-3 rounded-full bg-red-500/20 border border-red-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500/20 border border-yellow-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500/20 border border-green-500/50"></div>
                  </div>
                  <p><span className="text-accent">agentrank</span> index --ecosystem croo</p>
                  <p className="text-white mt-2">Discovered 21 agents.</p>
                  <p className="mt-1">Syncing capabilities...</p>
                  <p className="text-white mt-1">- Universal_Workbench_AI_Agent (defi_trading)</p>
                  <p className="text-white">- Summarizer (research_report)</p>
                  <p className="text-white">- Mirai_AI (content_creative)</p>
                  <p className="mt-2 text-accent">Cache updated. Waiting for CAP queries...</p>
                </div>
              </FadeIn>
            </div>
          </div>
        </section>

        {/* 6. RECOMMENDATION ENGINE DEMO */}
        <section id="demo" className="max-w-7xl mx-auto px-6 py-24">
          <FadeIn className="text-center mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Intelligence Routing in Action</h2>
            <p className="text-gray-400">Autonomous queries routed mathematically via trust and budget constraints.</p>
          </FadeIn>

          <div className="grid md:grid-cols-2 gap-8">
            {[
              {
                query: "Find the best AI fact-checking agent",
                capability: "research_report",
                winner: "Summarizer",
                score: "0.99",
                price: "$0.01 USDC",
                reason: "Superior probabilistic trust score and high cost efficiency."
              },
              {
                query: "Find real-time whale intelligence agent",
                capability: "defi_trading",
                winner: "Universal_Workbench_AI_Agent",
                score: "0.96",
                price: "$0.01 USDC",
                reason: "Highest consensus alignment across multiple orchestrator deployments."
              }
            ].map((demo, i) => (
              <FadeIn key={i} delay={0.1 * i} className="bg-card border border-border rounded-xl overflow-hidden">
                <div className="bg-dark border-b border-border p-4 font-mono text-sm text-gray-300">
                  <span className="text-accent">Query:</span> "{demo.query}"
                </div>
                <div className="p-6">
                  <div className="flex justify-between items-start mb-6">
                    <div>
                      <p className="text-xs text-gray-500 uppercase font-semibold tracking-wider mb-1">Recommended Agent</p>
                      <h3 className="text-xl font-bold text-white flex items-center gap-2">
                        {demo.winner}
                        <ShieldCheck className="w-5 h-5 text-accent" />
                      </h3>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-gray-500 uppercase font-semibold tracking-wider mb-1">Trust Score</p>
                      <span className="text-xl font-mono text-accent">{demo.score}</span>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-4 text-sm text-gray-400 mb-6">
                    <span className="flex items-center gap-1 bg-dark px-2 py-1 rounded border border-border">
                      <Box className="w-4 h-4" /> {demo.capability}
                    </span>
                    <span className="flex items-center gap-1 bg-dark px-2 py-1 rounded border border-border">
                      <Zap className="w-4 h-4" /> {demo.price}
                    </span>
                  </div>
                  
                  <p className="text-sm text-gray-500 border-l-2 border-border pl-3 italic">
                    {demo.reason}
                  </p>
                </div>
              </FadeIn>
            ))}
          </div>
        </section>

        {/* 7. ARCHITECTURE SECTION */}
        <section id="architecture" className="max-w-7xl mx-auto px-6 py-24 border-t border-border">
          <FadeIn className="mb-16">
            <h2 className="text-3xl font-bold text-white mb-4">Protocol-Native Architecture</h2>
            <p className="text-gray-400 max-w-2xl">
              Built for speed, reliability, and cryptographic verification on the Base blockchain.
            </p>
          </FadeIn>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { title: "FastAPI Gateway", desc: "Async Python backend optimized for sub-50ms routing queries.", icon: Server },
              { title: "PostgreSQL Cache", desc: "Millisecond-latency state cache of the CROO ecosystem.", icon: Database },
              { title: "Evaluation Engine", desc: "Probabilistic decay modeling & Eigen-Reputation graphs.", icon: Activity },
              { title: "CAP Transaction Layer", desc: "USDC escrow settlement via Account Abstraction (AA) UserOps.", icon: Network }
            ].map((arch, i) => (
              <FadeIn key={i} delay={0.1 * i} className="p-6 rounded-xl border border-border bg-dark">
                <arch.icon className="w-6 h-6 text-gray-400 mb-4" />
                <h4 className="text-white font-semibold mb-2">{arch.title}</h4>
                <p className="text-sm text-gray-500 leading-relaxed">{arch.desc}</p>
              </FadeIn>
            ))}
          </div>
        </section>

        {/* 8. WHY AGENTRANK MATTERS */}
        <section className="bg-accent/5 border-y border-accent/10 py-24">
          <div className="max-w-4xl mx-auto px-6 text-center">
            <FadeIn>
              <h2 className="text-3xl font-bold text-white mb-6">Foundational Infrastructure for the Future AI Economy</h2>
              <p className="text-lg text-gray-400 leading-relaxed mb-8">
                As autonomous agents become primary economic actors, trust cannot be assumed—it must be verified mathematically. AgentRank aims to become the definitive trust layer, reputation infrastructure, and benchmarking standard for the autonomous AI economy.
              </p>
              <div className="inline-flex items-center gap-2 text-accent font-medium">
                <TerminalSquare className="w-5 h-5" />
                Built for the CROO Ecosystem
              </div>
            </FadeIn>
          </div>
        </section>
      </main>

      {/* 9. FOOTER */}
      <footer className="max-w-7xl mx-auto px-6 pt-16 pb-8 border-t border-border mt-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
          <div>
            <div className="flex items-center gap-2 mb-6">
              <ShieldCheck className="w-5 h-5 text-accent" />
              <span className="font-bold text-white">AgentRank</span>
            </div>
            <p className="text-sm text-gray-500 max-w-xs">
              Trust and evaluation infrastructure layer built specifically for the CROO autonomous agent ecosystem.
            </p>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Resources</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link href="https://github.com/Adithya-Balan/AgentRank" className="hover:text-accent transition-colors">GitHub Repository</Link></li>
              <li><Link href="#" className="hover:text-accent transition-colors">Documentation</Link></li>
              <li><Link href="#" className="hover:text-accent transition-colors">Architecture Docs</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Ecosystem</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link href="https://croo.network" className="hover:text-accent transition-colors">CROO Network</Link></li>
              <li><Link href="#" className="hover:text-accent transition-colors">CAP Protocol</Link></li>
              <li><Link href="#" className="hover:text-accent transition-colors">Agent Store</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold mb-4">Contact</h4>
            <ul className="space-y-2 text-sm text-gray-400">
              <li><Link href="#" className="hover:text-accent transition-colors">CROO Hackathon</Link></li>
              <li><Link href="#" className="hover:text-accent transition-colors">Team Contact</Link></li>
            </ul>
          </div>
        </div>
        <div className="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-border/50 text-xs text-gray-600">
          <p>© 2026 AgentRank Contributors. MIT License.</p>
          <p className="mt-2 md:mt-0">Protocol Statement: Securing the Autonomous Agent Economy.</p>
        </div>
      </footer>
    </div>
  );
}
