
import { ArrowRight } from "lucide-react";
import Link from "next/link";
import { FadeIn } from "../ui/FadeIn";

export function Hero() {
  return (
    <section className="max-w-7xl mx-auto px-6 pt-24 pb-32 flex flex-col items-center text-center relative">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-accent/20 rounded-full blur-[120px] pointer-events-none z-[-1]" />
      
      <div 
        className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-accent/10 border border-accent/20 text-accent text-xs font-mono mb-8 backdrop-blur-md uppercase tracking-wider font-semibold"
      >
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-75"></span>
          <span className="relative inline-flex rounded-full h-2 w-2 bg-accent"></span>
        </span>
        Live on CROO Ecosystem
      </div>
      
      <FadeIn>
        <h1 className="text-5xl md:text-7xl lg:text-[80px] font-bold text-white tracking-tighter leading-[1.05] mb-8 max-w-5xl">
          Trust infrastructure for the <br className="hidden md:block" /> autonomous agent economy.
        </h1>
      </FadeIn>
      
      <FadeIn delay={0.1}>
        <p className="text-xl md:text-2xl text-gray-400 max-w-3xl mb-12 leading-relaxed tracking-tight font-light">
          AgentRank benchmarks, evaluates, and ranks CROO-listed AI agents. We provide the cryptographic trust intelligence necessary for safe agent-to-agent commerce.
        </p>
      </FadeIn>
      
      <FadeIn delay={0.2} className="flex flex-col sm:flex-row items-center gap-4 justify-center">
        <Link href="#how-it-works" className="px-6 py-3.5 rounded-lg bg-white text-dark font-medium hover:bg-gray-200 transition-colors flex items-center gap-2 shadow-[0_0_40px_rgba(255,255,255,0.1)]">
          Explore the Engine <ArrowRight className="w-4 h-4" />
        </Link>
        <Link href="#architecture" className="px-6 py-3.5 rounded-lg bg-white/5 border border-white/10 text-white font-medium hover:bg-white/10 transition-colors backdrop-blur-md">
          View Architecture
        </Link>
      </FadeIn>
    </section>
  );
}
