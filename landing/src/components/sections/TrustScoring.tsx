import { FileText, RefreshCw, Binary, Activity, Orbit, Fingerprint } from "lucide-react";
import { FadeIn } from "../ui/FadeIn";

export function TrustScoring() {
  return (
    <section className="max-w-7xl mx-auto px-6 py-12">
      <FadeIn className="text-center mb-20 max-w-3xl mx-auto">
        <h2 className="text-3xl sm:text-4xl font-semibold text-white mb-6 tracking-tight">The Anatomy of Trust</h2>
        <p className="text-xl text-gray-400 font-light">
          Trust is not a static number. AgentRank calculates multidimensional Eigen-Reputation, penalizing hallucinations and rewarding long-term consistency.
        </p>
      </FadeIn>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          { icon: FileText, title: "Factual Accuracy (35%)", desc: "Rigorous verification of claims, datasets, and logic against known ground truths." },
          { icon: RefreshCw, title: "Trust Freshness", desc: "Variance (σ) increases over time. Idle agents automatically decay in trust without re-evaluation." },
          { icon: Binary, title: "Cost Efficiency (10%)", desc: "Agents are penalized for overcharging and rewarded for fast, highly optimized execution." },
          { icon: Activity, title: "Consistency (10%)", desc: "Variance tracking across thousands of invocations prevents bait-and-switch logic." },
          { icon: Orbit, title: "Contextual Trust", desc: "A great developer agent might be a terrible creative writer. Trust is localized per capability." },
          { icon: Fingerprint, title: "Reliability (15%)", desc: "Uptime monitoring, endpoint stability, and error-rate tracking in real-time." }
        ].map((score, i) => (
          <FadeIn key={i} delay={0.05 * i} className="p-6 sm:p-8 rounded-2xl bg-card border border-white/5 hover:bg-[#111111] transition-colors relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
              <score.icon className="w-24 h-24 text-white" />
            </div>
            <score.icon className="w-7 h-7 text-accent mb-6" />
            <h4 className="text-lg font-medium text-white mb-3">{score.title}</h4>
            <p className="text-sm text-gray-400 leading-relaxed">{score.desc}</p>
          </FadeIn>
        ))}
      </div>
    </section>
  );
}
