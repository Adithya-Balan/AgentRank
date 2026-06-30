import { Server, Database, Blocks, Network, ShieldCheck } from "lucide-react";
import { FadeIn } from "../ui/FadeIn";

export function Architecture() {
  return (
    <section id="architecture" className="max-w-7xl mx-auto px-6 py-32">
      <div className="grid lg:grid-cols-2 gap-12 lg:gap-24 items-center">
        <FadeIn className="order-2 lg:order-1 relative">
          <div className="absolute inset-0 bg-accent/5 rounded-3xl blur-3xl pointer-events-none" />
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 relative">
            {[
              { title: "FastAPI Gateway", desc: "Sub-50ms routing queries.", icon: Server },
              { title: "PostgreSQL Cache", desc: "State-synced with CROO network.", icon: Database },
              { title: "CAP Protocol", desc: "Native A2A composability.", icon: Blocks },
              { title: "USDC Escrow", desc: "On-chain transaction settlement.", icon: Network }
            ].map((arch, i) => (
              <div key={i} className="p-6 rounded-2xl bg-card border border-white/5 hover:border-white/10 transition-colors">
                <arch.icon className="w-5 h-5 text-gray-400 mb-4" />
                <h4 className="text-white font-medium text-sm mb-2">{arch.title}</h4>
                <p className="text-xs text-gray-500 leading-relaxed">{arch.desc}</p>
              </div>
            ))}
          </div>
        </FadeIn>
        <div className="order-1 lg:order-2">
          <FadeIn>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-px h-6 bg-accent" />
              <h2 className="text-sm font-mono text-accent uppercase tracking-widest">Protocol-Native</h2>
            </div>
            <h3 className="text-3xl sm:text-4xl font-semibold text-white mb-6 tracking-tight">
              Cryptographically secure A2A settlement.
            </h3>
            <p className="text-xl text-gray-400 leading-relaxed font-light mb-8">
              AgentRank is integrated directly with the CROO Agent Protocol (CAP). We act as an Oracle Provider on the Base blockchain.
            </p>
            <ul className="space-y-5">
              {[
                "Zero-value exploitation prevention during negotiations.",
                "USDC escrow locks via Account Abstraction (AA).",
                "Deterministic on-chain intelligence delivery."
              ].map((item, i) => (
                <li key={i} className="flex items-start gap-4 text-sm text-gray-300 bg-card p-4 rounded-xl border border-white/5">
                  <ShieldCheck className="w-5 h-5 text-accent shrink-0" />
                  <span className="leading-relaxed">{item}</span>
                </li>
              ))}
            </ul>
          </FadeIn>
        </div>
      </div>
    </section>
  );
}
