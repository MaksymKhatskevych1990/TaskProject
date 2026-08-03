"use client";

import { useSectionScrollSnap } from "@/hooks/useSectionScrollSnap";

export function SectionScrollSnap({ children }: { children: React.ReactNode }) {
  useSectionScrollSnap(true);
  return <>{children}</>;
}
