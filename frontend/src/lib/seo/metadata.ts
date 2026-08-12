import type { Metadata } from "next";
import { SEO, SITE } from "@/lib/site-data";
import { absoluteUrl, getSiteUrl } from "@/lib/seo/site-url";

type PageMetadataOptions = {
  title?: string;
  description?: string;
  path?: string;
  type?: "website" | "article";
  publishedTime?: string;
  noIndex?: boolean;
};

export function createPageMetadata({
  title = SEO.defaultTitle,
  description = SITE.description,
  path = "/",
  type = "website",
  publishedTime,
  noIndex = false,
}: PageMetadataOptions = {}): Metadata {
  const url = absoluteUrl(path);
  const ogImage = absoluteUrl(SEO.ogImagePath);

  return {
    metadataBase: new URL(getSiteUrl()),
    title: {
      default: SEO.defaultTitle,
      template: SEO.titleTemplate,
    },
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
      title,
      description,
      images: [
        {
          url: ogImage,
          width: 1200,
          height: 630,
          alt: SITE.brand,
        },
      ],
      ...(publishedTime ? { publishedTime } : {}),
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [ogImage],
    },
    other: {
      "geo.region": SEO.geoRegion,
      "geo.placename": SEO.geoPlacename,
      "geo.position": SEO.geoPosition,
      ICBM: SEO.icbm,
    },
  };
}
