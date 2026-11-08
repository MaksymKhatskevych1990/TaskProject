export type PublicSeo = {
  title: string;
  description: string;
  h1: string;
  ogTitle: string;
  ogDescription: string;
  ogImage: string | null;
  canonicalUrl: string;
  noindex: boolean;
  focusKeyword: string;
};

export type SiteSeoSettings = {
  seo: PublicSeo;
  blogTitle: string;
  blogDescription: string;
  blogH1: string;
  googleSiteVerification: string;
};
