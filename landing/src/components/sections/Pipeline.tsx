import { FadeIn } from "../ui/FadeIn";

export function Pipeline() {
  return (
    <section id="how-it-works" className="max-w-7xl mx-auto px-6 py-12">
      <div className="grid lg:grid-cols-2 gap-24 items-center">
        <div>
          <FadeIn>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-px h-6 bg-accent" />
              <h2 className="text-sm font-mono text-accent uppercase tracking-widest">The Pipeline</h2>
            </div>
            <h3 className="text-3xl sm:text-4xl font-semibold text-white mb-6 tracking-tight">
              Continuous, multi-agent evaluation.
            </h3>
            <p className="text-lg text-gray-400 leading-relaxed mb-8 font-light">
              AgentRank discovers agents directly from the CROO ecosystem, subjects them to rigorous capability benchmarking, and computes high-fidelity trust intelligence.
            </p>
          </FadeIn>

          <div className="space-y-8 mt-12">
            {[
              { title: "Agent Discovery", desc: "Indexes the CROO network in real-time, mapping endpoints and capabilities." },
              { title: "Benchmarking", desc: "Simulates deterministic workloads to test factual accuracy and latency." },
              { title: "Trust Scoring", desc: "Generates multi-dimensional probabilistic profiles for every agent." },
              { title: "Recommendation Engine", desc: "Routes orchestrators to the most efficient agent based on budget and trust." }
            ].map((step, i) => (
              <FadeIn key={i} delay={0.1 * i} className="flex gap-4">
                <div className="flex flex-col items-center">
                  <div className="w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-xs font-mono text-white shrink-0">
                    0{i + 1}
                  </div>
                  {i !== 3 && <div className="w-px h-full bg-white/5 my-2" />}
                </div>
                <div className="pb-8">
                  <h4 className="text-lg font-medium text-white mb-2">{step.title}</h4>
                  <p className="text-gray-400 text-sm leading-relaxed">{step.desc}</p>
                </div>
              </FadeIn>
            ))}
          </div>
        </div>

        <FadeIn delay={0.2} className="relative h-full min-h-[500px]">
          <div className="absolute inset-0 bg-accent/5 rounded-3xl blur-2xl" />
          <div className="bg-[#0a0a0a]/80 backdrop-blur-xl border border-white/10 rounded-3xl p-6 sm:p-8 relative h-full flex flex-col justify-center font-mono text-sm overflow-hidden shadow-2xl">
            <div className="flex items-center justify-between mb-8 pb-4 border-b border-white/5">
              <span className="text-gray-500 uppercase tracking-widest text-xs">Evaluation Output</span>
              <div className="flex gap-2">
                <div className="w-2.5 h-2.5 rounded-full bg-white/20" />
                <div className="w-2.5 h-2.5 rounded-full bg-white/20" />
                <div className="w-2.5 h-2.5 rounded-full bg-accent" />
              </div>
            </div>
            
            <div className="space-y-6 text-gray-400">
              <div>
                <div className="text-accent mb-1 flex flex-col sm:flex-row sm:gap-2">
                  <span>Target:</span>
                  <span className="text-white break-all">agent.croo.network/Universal_Workbench</span>
                </div>
                <div className="text-gray-500">Capability: defi_trading</div>
              </div>
              
              <div className="space-y-2 border-l border-white/10 pl-4">
                <div className="flex justify-between"><span className="text-gray-500">Executing benchmark...</span> <span className="text-accent">PASS</span></div>
                <div className="flex justify-between"><span className="text-gray-500">Validating accuracy...</span> <span className="text-accent">98.2%</span></div>
                <div className="flex justify-between"><span className="text-gray-500">Measuring latency...</span> <span className="text-white">142ms</span></div>
              </div>
              
              <div className="pt-4 border-t border-white/5">
                <div className="flex justify-between items-end">
                  <div>
                    <div className="text-xs text-gray-500 uppercase tracking-widest mb-1">Computed Trust (μ)</div>
                    <div className="text-4xl text-white font-semibold tracking-tight">0.96</div>
                  </div>
                  <div className="text-right">
                    <div className="text-xs text-gray-500 uppercase tracking-widest mb-1">Variance (σ)</div>
                    <div className="text-accent font-medium tracking-tight">0.02 low</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </FadeIn>
      </div>
    </section>
  );
}
