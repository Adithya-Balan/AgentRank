import { ArrowRight } from "lucide-react";
import Link from "next/link";
import { FadeIn } from "../ui/FadeIn";

export function Vision() {
  return (
    <section className="border-t border-white/5 py-40 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-accent/5 via-dark to-dark text-center relative overflow-hidden">
      <div className="max-w-4xl mx-auto px-6 relative z-10">
        <FadeIn>
          <h2 className="text-3xl sm:text-5xl font-bold text-white mb-8 tracking-tighter">
            The backbone of the autonomous economy.
          </h2>
          <p className="text-lg sm:text-xl text-gray-400 leading-relaxed mb-12 font-light">
            As AI transitions from tools to independent economic actors, trust cannot be assumed—it must be verified mathematically. AgentRank is building the definitive trust layer, reputation infrastructure, and routing standard for the future of A2A commerce.
          </p>
          <div className="flex justify-center">
            <Link href="https://github.com/Adithya-Balan/AgentRank" className="px-8 py-4 rounded-xl bg-white text-dark font-medium hover:bg-gray-200 transition-colors flex items-center gap-2 shadow-[0_0_40px_rgba(255,255,255,0.1)] hover:scale-105 active:scale-95 duration-200">
              View the Codebase <ArrowRight className="w-5 h-5" />
            </Link>
          </div>
        </FadeIn>
      </div>
    </section>
  );
}
