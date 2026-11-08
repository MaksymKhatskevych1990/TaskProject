"use client";

import { createContext, useContext, type ReactNode } from "react";
import { fallbackSiteContent, type SiteContent } from "@/lib/site-content";

const SiteContentContext = createContext<SiteContent>(fallbackSiteContent);

export function SiteContentProvider({
  value,
  children,
}: {
  value: SiteContent;
  children: ReactNode;
}) {
  return <SiteContentContext.Provider value={value}>{children}</SiteContentContext.Provider>;
}

export function useSiteContent(): SiteContent {
  return useContext(SiteContentContext);
}
