import type { BlogPostDetail, BlogPostListItem } from "@/lib/blog-api";
import {
  FAQ_ITEMS,
  GEO_LOCATIONS,
  SEO,
  SERVICES,
  SITE,
  TESTIMONIALS,
} from "@/lib/site-data";
import { absoluteUrl, getSiteUrl } from "@/lib/seo/site-url";

type SchemaNode = Record<string, unknown>;

const ORG_ID = `${getSiteUrl()}/#organization`;
const WEBSITE_ID = `${getSiteUrl()}/#website`;

function postalAddress(location: (typeof GEO_LOCATIONS)[number]): SchemaNode {
  return {
    "@type": "PostalAddress",
    streetAddress: location.streetAddress,
    addressLocality: location.addressLocality,
    addressRegion: location.addressRegion,
    postalCode: location.postalCode,
    addressCountry: location.addressCountry,
  };
}

function openingHoursSpecification(): SchemaNode {
  return {
    "@type": "OpeningHoursSpecification",
    dayOfWeek: SEO.openingHours.days,
    opens: SEO.openingHours.opens,
    closes: SEO.openingHours.closes,
  };
}

export function buildOrganizationNode(): SchemaNode {
  const headquarters = GEO_LOCATIONS.find((location) => location.isHeadquarters) ?? GEO_LOCATIONS[0];

  return {
    "@type": ["Organization", "ProfessionalService"],
    "@id": ORG_ID,
    name: SITE.brand,
    alternateName: SITE.brandShort,
    url: getSiteUrl(),
    logo: {
      "@type": "ImageObject",
      url: absoluteUrl("/og-image.png"),
    },
    image: absoluteUrl("/og-image.png"),
    description: SITE.description,
    email: SITE.email,
    telephone: SITE.phone,
    foundingDate: String(SITE.foundingYear),
    address: postalAddress(headquarters),
    geo: {
      "@type": "GeoCoordinates",
      latitude: headquarters.geo.latitude,
      longitude: headquarters.geo.longitude,
    },
    openingHoursSpecification: openingHoursSpecification(),
    areaServed: SEO.areaServed.map((name) => ({
      "@type": "AdministrativeArea",
      name,
    })),
    knowsAbout: SEO.knowsAbout,
    sameAs: [...SITE.sameAs],
    contactPoint: [
      {
        "@type": "ContactPoint",
        contactType: "sales",
        telephone: SITE.phone,
        email: SITE.email,
        availableLanguage: ["Ukrainian", "English"],
        areaServed: "UA",
      },
      {
        "@type": "ContactPoint",
        contactType: "customer support",
        url: SITE.telegramUrl,
        availableLanguage: ["Ukrainian", "English"],
      },
    ],
    hasOfferCatalog: {
      "@type": "OfferCatalog",
      name: "Digital-послуги",
      itemListElement: SERVICES.filter((service) => service.featured).map((service, index) => ({
        "@type": "Offer",
        position: index + 1,
        itemOffered: {
          "@type": "Service",
          name: service.title,
          description: service.description,
          provider: { "@id": ORG_ID },
        },
      })),
    },
  };
}

export function buildLocalBusinessNodes(): SchemaNode[] {
  return GEO_LOCATIONS.map((location) => ({
    "@type": "LocalBusiness",
    "@id": `${getSiteUrl()}/#location-${location.id}`,
    name: `${SITE.brand} — ${location.name}`,
    description: `${SITE.brand}: дизайн, розробка сайтів, SEO та Telegram-боти в ${location.addressLocality}.`,
    url: getSiteUrl(),
    telephone: location.telephone,
    email: SITE.email,
    parentOrganization: { "@id": ORG_ID },
    address: postalAddress(location),
    geo: {
      "@type": "GeoCoordinates",
      latitude: location.geo.latitude,
      longitude: location.geo.longitude,
    },
    openingHoursSpecification: openingHoursSpecification(),
    areaServed: {
      "@type": "City",
      name: location.addressLocality,
    },
  }));
}

export function buildWebSiteNode(): SchemaNode {
  return {
    "@type": "WebSite",
    "@id": WEBSITE_ID,
    name: SITE.brand,
    url: getSiteUrl(),
    description: SITE.description,
    inLanguage: SITE.language,
    publisher: { "@id": ORG_ID },
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: `${getSiteUrl()}/blog?q={search_term_string}`,
      },
      "query-input": "required name=search_term_string",
    },
  };
}

export function buildWebPageNode({
  path,
  name,
  description,
}: {
  path: string;
  name: string;
  description: string;
}): SchemaNode {
  const url = absoluteUrl(path);

  return {
    "@type": "WebPage",
    "@id": `${url}#webpage`,
    url,
    name,
    description,
    isPartOf: { "@id": WEBSITE_ID },
    about: { "@id": ORG_ID },
    inLanguage: SITE.language,
  };
}

export function buildServiceNodes(): SchemaNode[] {
  return SERVICES.map((service) => ({
    "@type": "Service",
    "@id": `${getSiteUrl()}/#service-${encodeURIComponent(service.title)}`,
    name: service.title,
    description: service.description,
    provider: { "@id": ORG_ID },
    areaServed: SEO.areaServed.map((name) => ({
      "@type": "AdministrativeArea",
      name,
    })),
    ...("features" in service && service.features
      ? {
          hasOfferCatalog: {
            "@type": "OfferCatalog",
            name: service.title,
            itemListElement: service.features.map((feature, index) => ({
              "@type": "Offer",
              position: index + 1,
              itemOffered: {
                "@type": "Service",
                name: feature,
              },
            })),
          },
        }
      : {}),
  }));
}

export function buildFaqPageNode(): SchemaNode {
  return {
    "@type": "FAQPage",
    "@id": `${getSiteUrl()}/#faq`,
    mainEntity: FAQ_ITEMS.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: item.answer,
      },
    })),
  };
}

export function buildReviewNodes(): SchemaNode[] {
  const ratings = TESTIMONIALS.map((item) => item.rating);
  const average =
    ratings.reduce((sum, rating) => sum + rating, 0) / Math.max(ratings.length, 1);

  return [
    {
      "@type": "AggregateRating",
      "@id": `${getSiteUrl()}/#aggregate-rating`,
      itemReviewed: { "@id": ORG_ID },
      ratingValue: average.toFixed(1),
      bestRating: "5",
      worstRating: "1",
      ratingCount: TESTIMONIALS.length,
      reviewCount: TESTIMONIALS.length,
    },
    ...TESTIMONIALS.map((item, index) => ({
      "@type": "Review",
      "@id": `${getSiteUrl()}/#review-${index + 1}`,
      itemReviewed: { "@id": ORG_ID },
      author: {
        "@type": "Person",
        name: item.name,
      },
      reviewRating: {
        "@type": "Rating",
        ratingValue: String(item.rating),
        bestRating: "5",
        worstRating: "1",
      },
      reviewBody: item.text,
    })),
  ];
}

export function buildHomePageGraph(): SchemaNode[] {
  return [
    ...buildLocalBusinessNodes(),
    buildWebPageNode({
      path: "/",
      name: SEO.defaultTitle,
      description: SITE.description,
    }),
    ...buildServiceNodes(),
    buildFaqPageNode(),
    ...buildReviewNodes(),
  ];
}

export function buildBlogListGraph(posts: BlogPostListItem[]): SchemaNode[] {
  return [
    buildWebPageNode({
      path: "/blog",
      name: `Блог — ${SITE.brand}`,
      description: `Поради з дизайну, розробки сайтів та SEO від команди ${SITE.brandShort}.`,
    }),
    {
      "@type": "CollectionPage",
      "@id": `${absoluteUrl("/blog")}#collection`,
      name: `Блог — ${SITE.brand}`,
      url: absoluteUrl("/blog"),
      isPartOf: { "@id": WEBSITE_ID },
      mainEntity: {
        "@type": "ItemList",
        itemListElement: posts.map((post, index) => ({
          "@type": "ListItem",
          position: index + 1,
          url: absoluteUrl(`/blog/${post.slug}`),
          name: post.title,
        })),
      },
    },
  ];
}

export function buildBlogPostGraph(post: BlogPostDetail): SchemaNode[] {
  const url = absoluteUrl(`/blog/${post.slug}`);

  return [
    buildWebPageNode({
      path: `/blog/${post.slug}`,
      name: post.title,
      description: post.excerpt,
    }),
    {
      "@type": "BlogPosting",
      "@id": `${url}#article`,
      headline: post.title,
      description: post.excerpt,
      url,
      datePublished: post.date,
      dateModified: post.date,
      inLanguage: SITE.language,
      author: {
        "@type": "Organization",
        "@id": ORG_ID,
        name: SITE.brand,
      },
      publisher: {
        "@type": "Organization",
        "@id": ORG_ID,
        name: SITE.brand,
        logo: {
          "@type": "ImageObject",
          url: absoluteUrl("/og-image.png"),
        },
      },
      mainEntityOfPage: {
        "@type": "WebPage",
        "@id": `${url}#webpage`,
      },
      articleSection: post.category,
      wordCount: post.content.join(" ").split(/\s+/).length,
      isPartOf: { "@id": WEBSITE_ID },
    },
    {
      "@type": "BreadcrumbList",
      "@id": `${url}#breadcrumb`,
      itemListElement: [
        {
          "@type": "ListItem",
          position: 1,
          name: "Головна",
          item: getSiteUrl(),
        },
        {
          "@type": "ListItem",
          position: 2,
          name: "Блог",
          item: absoluteUrl("/blog"),
        },
        {
          "@type": "ListItem",
          position: 3,
          name: post.title,
          item: url,
        },
      ],
    },
  ];
}

export function buildSchemaGraph(nodes: SchemaNode[]): Record<string, unknown> {
  return {
    "@context": "https://schema.org",
    "@graph": nodes,
  };
}
