import type { Metadata } from "next";
import { SEO, SITE } from "@/lib/site-data";
import { absoluteUrl, getSiteUrl } from "@/lib/seo/site-url";

type PageMetadataOptions = {
  title?: string;
  description?: string;
  path?: string;
  type?: "website" | "article";
  publishedTime?: string;
  modifiedTime?: string;
  noIndex?: boolean;
  ogImage?: string | null;
  ogTitle?: string;
  ogDescription?: string;
  canonical?: string;
  absoluteTitle?: boolean;
  googleVerification?: string;
};

export function createPageMetadata({
  title = SEO.defaultTitle,
  description = SITE.description,
  path = "/",
  type = "website",
  publishedTime,
  modifiedTime,
  noIndex = false,
  ogImage,
  ogTitle,
  ogDescription,
  canonical,
  absoluteTitle = false,
  googleVerification,
}: PageMetadataOptions = {}): Metadata {
  const url = canonical || absoluteUrl(path);
  const image = ogImage || absoluteUrl(SEO.ogImagePath);
  const socialTitle = ogTitle || title;
  const socialDescription = ogDescription || description;

  return {
    metadataBase: new URL(getSiteUrl()),
    title: absoluteTitle
      ? { absolute: title }
      : path === "/"
        ? { default: title, template: SEO.titleTemplate }
        : title,
    description,
    keywords: [...SITE.keywords],
    authors: [{ name: SITE.brand, url: getSiteUrl() }],
    creator: SITE.brand,
    publisher: SITE.brand,
    formatDetection: {
      email: false,
      address: false,
      telephone: false,
    },
    alternates: {
      canonical: url,
      languages: {
        "uk-UA": url,
        "x-default": url,
      },
    },
    robots: noIndex
      ? { index: false, follow: false }
      : {
          index: true,
          follow: true,
          googleBot: {
            index: true,
            follow: true,
            "max-image-preview": "large",
            "max-snippet": -1,
            "max-video-preview": -1,
          },
        },
    openGraph: {
      type,
      locale: SITE.locale.replace("-", "_"),
      url,
      siteName: SITE.brand,
      title: socialTitle,
      description: socialDescription,
      images: [
        {
          url: image,
          width: 1200,
          height: 630,
          alt: socialTitle,
        },
      ],
      ...(publishedTime ? { publishedTime } : {}),
      ...(modifiedTime ? { modifiedTime } : {}),
    },
    twitter: {
      card: "summary_large_image",
      title: socialTitle,
      description: socialDescription,
      images: [image],
    },
    ...(googleVerification ? { verification: { google: googleVerification } } : {}),
    other: {
      "geo.region": SEO.geoRegion,
      "geo.placename": SEO.geoPlacename,
      "geo.position": SEO.geoPosition,
      ICBM: SEO.icbm,
    },
  };
}
