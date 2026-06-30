"use client";

import { ReactNode } from "react";

interface FadeInProps {
  children: ReactNode;
  delay?: number;
  className?: string;
}

export function FadeIn({ children, delay = 0, className = "" }: FadeInProps) {
  // Pure rendering, no animations to guarantee 100% visibility.
  return (
    <div className={className}>
      {children}
    </div>
  );
}
