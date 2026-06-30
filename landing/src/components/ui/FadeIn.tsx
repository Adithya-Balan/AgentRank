"use client";

import { ReactNode } from "react";

interface FadeInProps {
  children: ReactNode;
  delay?: number;
  className?: string;
}

export function FadeIn({ children, delay = 0, className = "" }: FadeInProps) {
  // Pure rendering with transition delay to clean up unused variables
  return (
    <div 
      className={className}
      style={{ transitionDelay: `${delay}s` }}
    >
      {children}
    </div>
  );
}
