import { ArrowUpRight } from "lucide-react";
import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-white/5 pt-20 pb-10 bg-[#050505]">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-12 mb-16">
          <div className="col-span-2 md:col-span-1">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-8 h-8 rounded-full overflow-hidden border border-accent/20">
                <img src="/logo.png" alt="AgentRank Logo" className="w-full h-full object-cover" />
              </div>
              <span className="font-semibold text-white">AgentRank</span>
            </div>
            <p className="text-sm text-gray-500 max-w-xs leading-relaxed">
              The trust and evaluation infrastructure layer for the CROO autonomous agent ecosystem.
            </p>
          </div>
          <div>
            <h4 className="text-white font-medium text-sm mb-6 tracking-wide uppercase">Resources</h4>
            <ul className="space-y-4 text-sm text-gray-400">
              <li><Link href="https://github.com/Adithya-Balan/AgentRank" className="hover:text-white transition-colors">GitHub Repository</Link></li>
              <li><Link href="#" className="hover:text-white transition-colors">Documentation</Link></li>
              <li><Link href="#architecture" className="hover:text-white transition-colors">Architecture</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-medium text-sm mb-6 tracking-wide uppercase">Ecosystem</h4>
            <ul className="space-y-4 text-sm text-gray-400">
              <li><Link href="https://agent.croo.network/" className="hover:text-white transition-colors flex items-center gap-1">CROO Network <ArrowUpRight className="w-3 h-3" /></Link></li>
              <li><Link href="https://cap.croo.network/" className="hover:text-white transition-colors">CAP Protocol</Link></li>
              <li><Link href="https://agent.croo.network/agents?sort=volume" className="hover:text-white transition-colors">Agent Store</Link></li>
            </ul>
          </div>
        </div>
        <div className="flex flex-col md:flex-row items-center justify-between pt-8 border-t border-white/5 text-sm text-gray-500">
          <p>© {new Date().getFullYear()} AgentRank Contributors. MIT License.</p>
          <div className="flex items-center gap-2 mt-4 md:mt-0 font-mono text-xs">
            <span className="w-2 h-2 rounded-full bg-accent relative flex items-center justify-center">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent opacity-50"></span>
            </span>
            Securing the Autonomous Economy
          </div>
        </div>
      </div>
    </footer>
  );
}
