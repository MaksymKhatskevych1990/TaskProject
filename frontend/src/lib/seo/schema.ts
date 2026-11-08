import type { BlogPostDetail, BlogPostListItem } from "@/lib/blog-api";
import { isPlaceholderPhone } from "@/lib/phone";
import { isCredibleOffice } from "@/lib/office";
import type { PortfolioProjectListItem } from "@/lib/portfolio-api";
import { SEO } from "@/lib/site-data";
import { fallbackSiteContent, type SiteContent, type SiteOffice } from "@/lib/site-content";
import { absoluteUrl, getSiteUrl } from "@/lib/seo/site-url";

type SchemaNode = Record<string, unknown>;

const ORG_ID = `${getSiteUrl()}/#organization`;
const WEBSITE_ID = `${getSiteUrl()}/#website`;

function resolveSite(content?: SiteContent): SiteContent {
  return content ?? fallbackSiteContent;
}

function postalAddress(location: SiteOffice): SchemaNode {
  const address: SchemaNode = {
    "@type": "PostalAddress",
    addressLocality: location.addressLocality,
    addressRegion: location.addressRegion,
    addressCountry: location.addressCountry,
  };
  if (location.streetAddress.trim() && isCredibleOffice(location)) {
    address.streetAddress = location.streetAddress;
  }
  if (location.postalCode && isCredibleOffice(location)) {
    address.postalCode = location.postalCode;
  }
  return address;
}

function openingHoursSpecification(): SchemaNode {
  return {
    "@type": "OpeningHoursSpecification",
    dayOfWeek: SEO.openingHours.days,
    opens: SEO.openingHours.opens,
    closes: SEO.openingHours.closes,
  };
}

export function buildOrganizationNode(content?: SiteContent): SchemaNode {
  const site = resolveSite(content);
  const headquarters =
    site.offices.find((location) => location.isHeadquarters) ?? site.offices[0];
  const phone = isPlaceholderPhone(site.phone) ? undefined : site.phone;

  return {
    "@type": ["Organization", "ProfessionalService"],
    "@id": ORG_ID,
    name: site.brand,
    alternateName: site.brandShort,
    url: getSiteUrl(),
    logo: {
      "@type": "ImageObject",
      url: absoluteUrl("/og-image.png"),
    },
    image: absoluteUrl("/og-image.png"),
    description: site.description,
    email: site.email,
    ...(phone ? { telephone: phone } : {}),
    foundingDate: String(site.foundingYear),
    address: headquarters
      ? postalAddress(headquarters)
      : {
          "@type": "PostalAddress",
          addressLocality: "Дніпро",
          addressCountry: "UA",
        },
    ...(headquarters
      ? {
          geo: {
            "@type": "GeoCoordinates",
            latitude: headquarters.geo.latitude,
            longitude: headquarters.geo.longitude,
          },
        }
      : {}),
    openingHoursSpecification: openingHoursSpecification(),
    areaServed: SEO.areaServed.map((name) => ({
      "@type": "AdministrativeArea",
      name,
    })),
    knowsAbout: SEO.knowsAbout,
    sameAs: [site.telegramUrl],
    contactPoint: [
      {
        "@type": "ContactPoint",
        contactType: "sales",
        ...(phone ? { telephone: phone } : {}),
        email: site.email,
        availableLanguage: ["Ukrainian", "English"],
        areaServed: "UA",
      },
      {
        "@type": "ContactPoint",
        contactType: "customer support",
        url: site.telegramUrl,
        availableLanguage: ["Ukrainian", "English"],
      },
    ],
    hasOfferCatalog: {
      "@type": "OfferCatalog",
      name: "Сайти, магазини, SEO, реклама і автоматизація",
      itemListElement: site.pricing.map((plan, index) => ({
        "@type": "Offer",
        position: index + 1,
        name: plan.name,
        description: plan.description,
        price: plan.price,
        priceCurrency: "UAH",
        availability: "https://schema.org/InStock",
        url: absoluteUrl(`/?plan=${plan.slug}#contact`),
        itemOffered: {
          "@type": "Service",
          name: plan.name,
          provider: { "@id": ORG_ID },
        },
      })),
    },
  };
}

export function buildLocalBusinessNodes(content?: SiteContent): SchemaNode[] {
  const site = resolveSite(content);
  return site.offices.filter(isCredibleOffice).filter((location) => location.streetAddress.trim()).map(
    (location) => ({
      "@type": "ProfessionalService",
      "@id": `${getSiteUrl()}/#location-${location.id}`,
      name: `${site.brand} — ${location.name}`,
      description: `${site.brand}: розробка сайтів, SEO та Telegram-боти. ${location.addressLocality}.`,
      url: getSiteUrl(),
      telephone: location.telephone,
      email: site.email,
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
    }),
  );
}

export function buildWebSiteNode(content?: SiteContent): SchemaNode {
  const site = resolveSite(content);
  return {
    "@type": "WebSite",
    "@id": WEBSITE_ID,
    name: site.brand,
    url: getSiteUrl(),
    description: site.description,
    inLanguage: site.locale.startsWith("uk") ? "uk" : site.locale,
    publisher: { "@id": ORG_ID },
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
    inLanguage: "uk",
  };
}

export function buildServiceNodes(content?: SiteContent): SchemaNode[] {
  const site = resolveSite(content);
  return site.services.map((service) => ({
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

export function buildFaqPageNode(content?: SiteContent): SchemaNode {
  const site = resolveSite(content);
  return {
    "@type": "FAQPage",
    "@id": `${getSiteUrl()}/#faq`,
    mainEntity: site.faq.map((item) => ({
      "@type": "Question",
      name: item.question,
      acceptedAnswer: {
        "@type": "Answer",
        text: item.answer,
      },
    })),
  };
}

export function buildReviewNodes(content?: SiteContent): SchemaNode[] {
  const site = resolveSite(content);
  const ratings = site.testimonials.map((item) => item.rating);
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
      ratingCount: site.testimonials.length,
      reviewCount: site.testimonials.length,
    },
    ...site.testimonials.map((item, index) => ({
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

export function buildHomePageGraph(
  page?: {
    name?: string;
    description?: string;
  },
  content?: SiteContent,
): SchemaNode[] {
  const site = resolveSite(content);
  return [
    ...buildLocalBusinessNodes(site),
    buildWebPageNode({
      path: "/",
      name: page?.name || `${site.brand} — ${site.tagline}`,
      description: page?.description || site.description,
    }),
    ...buildServiceNodes(site),
    buildFaqPageNode(site),
    ...buildReviewNodes(site),
  ];
}

export function buildBlogListGraph(
  posts: BlogPostListItem[],
  content?: SiteContent,
): SchemaNode[] {
  const site = resolveSite(content);
  return [
    buildWebPageNode({
      path: "/blog",
      name: `Блог — ${site.brand}`,
      description: `Поради з дизайну, розробки сайтів та SEO від команди ${site.brandShort}.`,
    }),
    {
      "@type": "CollectionPage",
      "@id": `${absoluteUrl("/blog")}#collection`,
      name: `Блог — ${site.brand}`,
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

export function buildBlogPostGraph(
  post: BlogPostDetail,
  content?: SiteContent,
): SchemaNode[] {
  const site = resolveSite(content);
  const url = post.seo?.canonicalUrl || absoluteUrl(`/blog/${post.slug}`);
  const headline = post.seo?.h1 || post.title;
  const description = post.seo?.description || post.excerpt;

  return [
    buildWebPageNode({
      path: `/blog/${post.slug}`,
      name: headline,
      description,
    }),
    {
      "@type": "BlogPosting",
      "@id": `${url}#article`,
      headline,
      description,
      url,
      datePublished: post.date,
      dateModified: post.updatedAt || post.date,
      inLanguage: site.locale.startsWith("uk") ? "uk" : site.locale,
      author: {
        "@type": "Organization",
        "@id": ORG_ID,
        name: site.brand,
      },
      publisher: {
        "@type": "Organization",
        "@id": ORG_ID,
        name: site.brand,
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

export function buildBreadcrumbNode(
  items: { name: string; path: string }[],
): SchemaNode {
  return {
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, index) => ({
      "@type": "ListItem",
      position: index + 1,
      name: item.name,
      item: absoluteUrl(item.path),
    })),
  };
}

export function buildPortfolioListNode(projects: PortfolioProjectListItem[]): SchemaNode {
  return {
    "@type": "ItemList",
    "@id": `${absoluteUrl("/works")}#list`,
    name: "Портфоліо",
    itemListElement: projects.map((project, index) => ({
      "@type": "ListItem",
      position: index + 1,
      url: absoluteUrl(`/works/${project.slug}`),
      name: project.title,
    })),
  };
}

export function buildCreativeWorkNode(project: {
  slug: string;
  title: string;
  description: string;
  category: string;
}): SchemaNode {
  const url = absoluteUrl(`/works/${project.slug}`);
  return {
    "@type": "CreativeWork",
    "@id": `${url}#work`,
    name: project.title,
    description: project.description,
    url,
    genre: project.category,
    creator: { "@id": ORG_ID },
  };
}

export function buildSchemaGraph(nodes: SchemaNode[]): Record<string, unknown> {
  return {
    "@context": "https://schema.org",
    "@graph": nodes.filter(Boolean),
  };
}
