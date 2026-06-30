import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgentRank | Trust Infrastructure for Autonomous AI",
  description: "AgentRank is a trust and evaluation infrastructure layer built specifically for the CROO autonomous agent ecosystem.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark scroll-smooth">
      <body className="antialiased bg-dark text-white font-sans">
        <div className="fixed inset-0 z-[-1] bg-grid-pattern opacity-30"></div>
        <div className="fixed inset-0 z-[-1] bg-gradient-to-b from-dark via-transparent to-dark opacity-90 pointer-events-none"></div>
        {children}
      </body>
    </html>
  );
}
