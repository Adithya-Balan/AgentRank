"use client";

import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Hero } from "@/components/sections/Hero";
import { Problem } from "@/components/sections/Problem";
import { Pipeline } from "@/components/sections/Pipeline";
import { TrustScoring } from "@/components/sections/TrustScoring";
import { EcosystemIntelligence } from "@/components/sections/EcosystemIntelligence";
import { Architecture } from "@/components/sections/Architecture";
import { Vision } from "@/components/sections/Vision";
import { Line } from "@/components/ui/Line";

export default function Home() {
  return (
    <div className="min-h-screen text-gray-300 font-sans selection:bg-accent selection:text-white pb-24">
      <Navbar />

      <main className="pt-32">
        <Hero />
        <Problem />
        <Line />
        <Pipeline />
        <Line />
        <TrustScoring />
        <EcosystemIntelligence />
        <Architecture />
        <Vision />
      </main>

      <Footer />
    </div>
  );
}
