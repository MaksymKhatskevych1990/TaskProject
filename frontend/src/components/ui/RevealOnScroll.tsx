"use client";

import { type ReactNode } from "react";
import { useScrollReveal } from "@/hooks/useScrollReveal";
import { cn } from "@/lib/utils";

type RevealOnScrollProps = {
  children: ReactNode;
  className?: string;
  delayMs?: number;
};

export function RevealOnScroll({
  children,
  className,
  delayMs = 0,
}: RevealOnScrollProps) {
  const { ref, visible } = useScrollReveal<HTMLDivElement>();

  return (
    <div
      ref={ref}
      className={cn(
        "transition-all duration-700 ease-out",
        visible ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0",
        className,
      )}
      style={{ transitionDelay: `${delayMs}ms` }}
    >
      {children}
    </div>
  );
}
