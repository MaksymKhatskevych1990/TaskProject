import { SITE } from "@/lib/site-data";

export function getSiteUrl(): string {
  const fromEnv = process.env.NEXT_PUBLIC_SITE_URL ?? process.env.SITE_URL;
  if (fromEnv) {
    return fromEnv.replace(/\/$/, "");
  }
  return `https://${SITE.domain}`;
}

export function absoluteUrl(path: string): string {
  if (path.startsWith("http")) {
    return path;
  }
  const normalized = path.startsWith("/") ? path : `/${path}`;
  return `${getSiteUrl()}${normalized}`;
}
