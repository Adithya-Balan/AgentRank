import { AlertTriangle, Network, Activity, Zap } from "lucide-react";
import { FadeIn } from "../ui/FadeIn";

export function Problem() {
  return (
    <section id="problem" className="max-w-7xl mx-auto px-4 sm:px-6 py-24 overflow-hidden">
      <FadeIn>
        <div className="flex items-center gap-3 mb-6">
          <div className="w-px h-6 bg-accent" />
          <h2 className="text-sm font-mono text-accent uppercase tracking-widest">The Problem</h2>
        </div>
        <h3 className="text-3xl sm:text-4xl font-semibold text-white mb-6 max-w-3xl tracking-tight">
          Millions of AI agents will exist. But there is no infrastructure for trust.
        </h3>
        <p className="text-xl text-gray-400 max-w-3xl leading-relaxed mb-16 font-light">
          As autonomous agents begin hiring other agents, the risk scales exponentially. A single unreliable sub-agent corrupts the entire orchestrated workflow. The ecosystem cannot scale without an objective evaluation layer.
        </p>
      </FadeIn>

      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { icon: AlertTriangle, title: "Hallucinations", desc: "Unverified agents injecting corrupt data into downstream pipelines." },
          { icon: Network, title: "Sybil Attacks", desc: "Malicious developers wash-trading to artificially inflate agent ratings." },
          { icon: Activity, title: "Static Ratings", desc: "Rigid 5-star systems fail to capture contextual, domain-specific nuances." },
          { icon: Zap, title: "Economic Chaos", desc: "Continuous global auditing is too expensive for localized tasks." }
        ].map((item, i) => (
          <FadeIn key={i} delay={0.1 * i} className="p-6 rounded-2xl bg-card border border-white/5 relative overflow-hidden group">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-accent/0 via-accent/50 to-accent/0 opacity-0 group-hover:opacity-100 transition-opacity" />
            <item.icon className="w-6 h-6 text-accent mb-6" />
            <h4 className="text-lg font-medium text-white mb-3">{item.title}</h4>
            <p className="text-sm text-gray-400 leading-relaxed">{item.desc}</p>
          </FadeIn>
        ))}
      </div>
    </section>
  );
}
