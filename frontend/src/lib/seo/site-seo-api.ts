import { getSiteContent } from "@/lib/site-content";
import type { SiteSeoSettings } from "@/lib/seo/types";

export async function getSiteSeo(): Promise<SiteSeoSettings> {
  const content = await getSiteContent();
  return {
    seo: content.seo,
    blogTitle: content.blogTitle,
    blogDescription: content.blogDescription,
    blogH1: content.blogH1,
    googleSiteVerification: content.googleSiteVerification,
  };
}
