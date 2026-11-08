export const STATIC_COVER_BY_SLUG: Record<string, string> = {
  artmagic: "/portfolio-covers/artmagic.png",
  luxmeb: "/portfolio-covers/luxmeb.png",
  rudwood: "/portfolio-covers/rudwood.png",
  "ac-clean": "/portfolio-covers/ac-clean.png",
  "elvet-group": "/portfolio-covers/elvet.png",
  "notarius-korneenkova": "/portfolio-covers/notarius.png",
  "glow-beauty": "/portfolio-covers/luxmeb.png",
  "techflow-saas": "/portfolio-covers/rudwood.png",
  elven: "/portfolio-covers/rudwood.png",
  "salon-pro": "/portfolio-covers/elvet.png",
  "legal-partners": "/portfolio-covers/notarius.png",
};

export const STATIC_GALLERY_BY_SLUG: Record<string, { url: string; caption: string }[]> =
  {
    artmagic: [
      { url: "/portfolio-covers/artmagic.png", caption: "Головна" },
      { url: "/portfolio-covers/artmagic-inner.png", caption: "Каталог" },
      { url: "/portfolio-covers/artmagic-detail.png", caption: "Картка товару" },
    ],
    luxmeb: [
      { url: "/portfolio-covers/luxmeb.png", caption: "Головна" },
      { url: "/portfolio-covers/luxmeb-inner.png", caption: "Проєкти" },
      { url: "/portfolio-covers/luxmeb-detail.png", caption: "Деталі проєкту" },
    ],
    rudwood: [
      { url: "/portfolio-covers/rudwood.png", caption: "Головна" },
      { url: "/portfolio-covers/rudwood-inner.png", caption: "Каталог" },
      { url: "/portfolio-covers/rudwood-detail.png", caption: "Картка товару" },
    ],
    "ac-clean": [
      { url: "/portfolio-covers/ac-clean.png", caption: "Головна" },
      { url: "/portfolio-covers/ac-clean-inner.png", caption: "Як ми працюємо" },
      { url: "/portfolio-covers/ac-clean-detail.png", caption: "Форма заявки" },
    ],
    "elvet-group": [
      { url: "/portfolio-covers/elvet.png", caption: "Головна" },
      { url: "/portfolio-covers/elvet-inner.png", caption: "Каталог філерів" },
      { url: "/portfolio-covers/elvet-detail.png", caption: "Картка товару" },
    ],
    "salon-pro": [
      { url: "/portfolio-covers/elvet.png", caption: "Головна" },
      { url: "/portfolio-covers/elvet-inner.png", caption: "Каталог філерів" },
      { url: "/portfolio-covers/elvet-detail.png", caption: "Картка товару" },
    ],
  };

export function staticGallery(slug: string): { url: string; caption: string }[] {
  return STATIC_GALLERY_BY_SLUG[slug] ?? [];
}

export function publicCoverUrl(
  url: string | null | undefined,
  slug?: string,
): string | null {
  if (slug && STATIC_COVER_BY_SLUG[slug]) {
    return STATIC_COVER_BY_SLUG[slug];
  }

  if (!url) return null;

  if (url.startsWith("/media/") || url.startsWith("/portfolio-covers/")) {
    return url;
  }

  try {
    const parsed = new URL(url);
    if (parsed.hostname === "minio" || parsed.hostname.endsWith(".internal")) {
      const parts = parsed.pathname.replace(/^\/+/, "").split("/");
      if (parts.length >= 2) {
        return `/media/${parts.slice(1).join("/")}${parsed.search}`;
      }
      return null;
    }
    if (parsed.pathname.startsWith("/media/")) {
      return `${parsed.pathname}${parsed.search}`;
    }
    return url;
  } catch {
    return null;
  }
}
