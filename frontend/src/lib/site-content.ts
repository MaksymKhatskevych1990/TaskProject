import { cache } from "react";
import { getBackendApiUrl } from "@/lib/api-config";
import type { PublicSeo } from "@/lib/seo/types";
import {
  BLOG_PAGE,
  CASES,
  CONTACT,
  FAQ_ITEMS,
  FOOTER,
  GEO_LOCATIONS,
  GUARANTEES,
  HERO,
  HERO_BRIEF,
  NAV_LINKS,
  PRICING_PLANS,
  PROCESS_STEPS,
  SECTIONS,
  SERVICES,
  SITE,
  STATS,
  TESTIMONIALS,
} from "@/lib/site-data";

type ApiResponse<T> = {
  success: boolean;
  data: T;
};

export type SiteNavLink = {
  href: string;
  label: string;
};

export type SiteHeroOffer = {
  id: string;
  label: string;
  duration: string;
  price: number;
  plan: string;
  includes: string;
};

export type SiteService = {
  title: string;
  description: string;
  features: string[];
  featured: boolean;
};

export type SiteStat = {
  value: number;
  suffix: string;
  label: string;
  decimals: number;
};

export type SiteTestimonial = {
  name: string;
  role: string;
  text: string;
  rating: number;
};

export type SiteCase = {
  category: string;
  title: string;
  description: string;
  before: string;
  after: string;
  metric: string;
  metricLabel: string;
};

export type SiteProcessStep = {
  title: string;
  description: string;
};

export type SitePricingPlan = {
  slug: string;
  name: string;
  price: number;
  description: string;
  features: string[];
  highlighted: boolean;
  badge: string;
};

export type SiteGuarantee = {
  title: string;
  description: string;
  image: "price" | "term" | "edits" | "support";
};

export type SiteFaqItem = {
  question: string;
  answer: string;
};

export type SiteOffice = {
  id: string;
  name: string;
  label: string;
  streetAddress: string;
  addressLocality: string;
  addressRegion: string;
  postalCode: string;
  addressCountry: string;
  geo: { latitude: number; longitude: number };
  telephone: string;
  isHeadquarters: boolean;
};

export type SiteContent = {
  brand: string;
  brandShort: string;
  domain: string;
  tagline: string;
  description: string;
  email: string;
  phone: string;
  telegramUsername: string;
  telegramUrl: string;
  foundingYear: number;
  currency: string;
  locale: string;
  nav: SiteNavLink[];
  hero: {
    status: string;
    statusMeta: string;
    title: string;
    hint: string;
    primaryCta: string;
    secondaryCta: string;
    chameleonLabel: string;
    conditions: string[];
    offers: SiteHeroOffer[];
  };
  sections: {
    services: { eyebrow: string; title: string; subtitle: string; also: string };
    cases: {
      eyebrow: string;
      title: string;
      subtitle: string;
      before: string;
      after: string;
      result: string;
    };
    portfolio: { eyebrow: string; title: string; subtitle: string; viewAll: string };
    process: { eyebrow: string; title: string; subtitle: string };
    pricing: {
      eyebrow: string;
      title: string;
      subtitle: string;
      from: string;
      choosePlan: string;
    };
    guarantees: { eyebrow: string; title: string };
    faq: { eyebrow: string; title: string };
  };
  services: SiteService[];
  stats: SiteStat[];
  testimonials: SiteTestimonial[];
  cases: SiteCase[];
  process: SiteProcessStep[];
  pricing: SitePricingPlan[];
  guarantees: SiteGuarantee[];
  faq: SiteFaqItem[];
  offices: SiteOffice[];
  contact: {
    title: string;
    subtitle: string;
    submit: string;
    submitting: string;
    successTitle: string;
    successSubtitle: string;
    errorMessage: string;
    fields: {
      name: { label: string; placeholder: string };
      phone: { label: string; placeholder: string };
      project: { label: string; placeholder: string };
      plan: { label: string };
    };
  };
  footer: {
    about: string;
    rights: string;
    blog: string;
    telegram: string;
    writeInTelegram: string;
    offices: string;
    faq: string;
  };
  blogPage: {
    eyebrow: string;
    title: string;
    subtitle: string;
    readMore: string;
    backToBlog: string;
    readTime: string;
    empty: string;
    ctaTitle: string;
    ctaSubtitle: string;
    ctaButton: string;
  };
  seo: PublicSeo;
  blogTitle: string;
  blogDescription: string;
  blogH1: string;
  googleSiteVerification: string;
};

export const fallbackSiteContent: SiteContent = {
  brand: SITE.brand,
  brandShort: SITE.brandShort,
  domain: SITE.domain,
  tagline: SITE.tagline,
  description: SITE.description,
  email: SITE.email,
  phone: SITE.phone,
  telegramUsername: SITE.telegramUsername,
  telegramUrl: SITE.telegramUrl,
  foundingYear: SITE.foundingYear,
  currency: SITE.currency,
  locale: SITE.locale,
  nav: NAV_LINKS.map((item) => ({ href: item.href, label: item.label })),
  hero: {
    status: HERO.status,
    statusMeta: HERO.statusMeta,
    title: HERO.title,
    hint: HERO.hint,
    primaryCta: HERO.primaryCta,
    secondaryCta: HERO.secondaryCta,
    chameleonLabel: HERO.chameleon.ariaLabel,
    conditions: [...HERO.conditions],
    offers: HERO_BRIEF.map((item) => ({
      id: item.id,
      label: item.label,
      duration: item.duration,
      price: item.price,
      plan: item.plan,
      includes: item.includes,
    })),
  },
  sections: {
    services: { ...SECTIONS.services },
    cases: { ...SECTIONS.cases },
    portfolio: { ...SECTIONS.portfolio },
    process: {
      eyebrow: SECTIONS.process.eyebrow,
      title: SECTIONS.process.title,
      subtitle: "Від першого дзвінка до запуску — прозорий процес без сюрпризів.",
    },
    pricing: { ...SECTIONS.pricing },
    guarantees: { ...SECTIONS.guarantees },
    faq: { ...SECTIONS.faq },
  },
  services: SERVICES.map((item) => ({
    title: item.title,
    description: item.description,
    features: "features" in item && item.features ? [...item.features] : [],
    featured: item.featured,
  })),
  stats: STATS.map((item) => ({
    value: item.value,
    suffix: item.suffix,
    label: item.label,
    decimals: item.decimals,
  })),
  testimonials: TESTIMONIALS.map((item) => ({ ...item })),
  cases: CASES.map((item) => ({ ...item })),
  process: PROCESS_STEPS.map((item) => ({
    title: item.title,
    description: item.description,
  })),
  pricing: PRICING_PLANS.map((item) => ({
    slug: item.slug,
    name: item.name,
    price: item.price,
    description: item.description,
    features: [...item.features],
    highlighted: item.highlighted,
    badge: "badge" in item && item.badge ? item.badge : "",
  })),
  guarantees: GUARANTEES.map((item) => ({ ...item })),
  faq: FAQ_ITEMS.map((item) => ({ ...item })),
  offices: GEO_LOCATIONS.map((item) => ({ ...item })),
  contact: {
    title: CONTACT.title,
    subtitle: CONTACT.subtitle,
    submit: CONTACT.submit,
    submitting: CONTACT.submitting,
    successTitle: CONTACT.successTitle,
    successSubtitle: CONTACT.successSubtitle,
    errorMessage: CONTACT.errorMessage,
    fields: {
      name: { ...CONTACT.fields.name },
      phone: { ...CONTACT.fields.phone },
      project: { ...CONTACT.fields.project },
      plan: { ...CONTACT.fields.plan },
    },
  },
  footer: {
    about:
      "Digital-студія з Дніпра. Сайти, магазини й боти під ключ для клієнтів по Україні та ЄС — повністю онлайн.",
    rights: FOOTER.rights,
    blog: FOOTER.blog,
    telegram: FOOTER.telegram,
    writeInTelegram: FOOTER.writeInTelegram,
    offices: "Локація",
    faq: "FAQ",
  },
  blogPage: {
    ...BLOG_PAGE,
    ctaTitle: "Потрібна допомога з проєктом?",
    ctaSubtitle: "Розкажіть про задачу — відповімо в Telegram протягом 30 хвилин.",
    ctaButton: "Розпочати проєкт",
  },
  seo: {
    title: `Розробка сайтів під ключ — ${SITE.brand}`,
    description: SITE.description,
    h1: HERO.title,
    ogTitle: `Розробка сайтів під ключ — ${SITE.brand}`,
    ogDescription: SITE.description,
    ogImage: null,
    canonicalUrl: "",
    noindex: false,
    focusKeyword: "",
  },
  blogTitle: "",
  blogDescription: "",
  blogH1: "",
  googleSiteVerification: "",
};

export function formatSitePrice(amount: number, content: SiteContent): string {
  return `${amount.toLocaleString(content.locale)} ${content.currency}`;
}

export const getSiteContent = cache(async (): Promise<SiteContent> => {
  try {
    const response = await fetch(new URL("/api/v1/website/content/", getBackendApiUrl()).href, {
      cache: "no-store",
    });
    if (!response.ok) {
      return fallbackSiteContent;
    }
    const payload = (await response.json()) as ApiResponse<SiteContent>;
    return payload.success && payload.data ? payload.data : fallbackSiteContent;
  } catch {
    return fallbackSiteContent;
  }
});
