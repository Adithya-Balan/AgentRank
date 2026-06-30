import { Code } from "lucide-react";
import Link from "next/link";

export function Navbar() {
  return (
    <nav className="fixed top-0 w-full z-50 border-b border-white/5 bg-dark/60 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-full overflow-hidden shadow-[0_0_20px_rgba(23,232,104,0.3)] border border-accent/20">
            <img src="/logo.png" alt="AgentRank Logo" className="w-full h-full object-cover" />
          </div>
          <span className="font-semibold text-white tracking-tight text-lg">AgentRank</span>
        </div>
        <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-400">
          <Link href="#problem" className="hover:text-white transition-colors">The Problem</Link>
          <Link href="#how-it-works" className="hover:text-white transition-colors">How it Works</Link>
          <Link href="#ecosystem" className="hover:text-white transition-colors">CROO Native</Link>
          <Link href="#architecture" className="hover:text-white transition-colors">Architecture</Link>
        </div>
        <div className="flex items-center gap-4">
          <Link href="https://github.com/Adithya-Balan/AgentRank" className="text-xs sm:text-sm font-medium text-white bg-white/10 hover:bg-white/20 px-3 py-1.5 sm:px-4 sm:py-2 rounded-full transition-colors flex items-center gap-2">
            <Code className="w-4 h-4" /> GitHub Repo
          </Link>
        </div>
      </div>
    </nav>
  );
}
