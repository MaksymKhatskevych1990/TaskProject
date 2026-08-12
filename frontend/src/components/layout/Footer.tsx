import Link from "next/link";
import { BrandLogo } from "@/components/layout/BrandLogo";
import { FOOTER, GEO_LOCATIONS, SITE } from "@/lib/site-data";

export function Footer() {
  return (
    <footer className="border-t border-white/5 py-12">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-10 grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
          <div className="sm:col-span-2 lg:col-span-1">
            <Link href="/" className="flex shrink-0 items-center" aria-label={`${SITE.brand} — на головну`}>
              <BrandLogo emblemSize="sm" />
            </Link>
            <p className="mt-4 max-w-xs text-sm leading-relaxed text-muted">
              Працюємо з клієнтами по всій Україні та Європі. Офіси та представництва:
            </p>
          </div>

          <div className="lg:col-span-3">
            <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
              Наші локації
            </p>
            <ul className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {GEO_LOCATIONS.map((location) => (
                <li key={location.id} className="text-sm">
                  <p className="font-medium text-foreground">
                    {location.name}
                    {location.isHeadquarters ? (
                      <span className="ml-1.5 text-[10px] uppercase tracking-wide text-cyan/80">
                        HQ
                      </span>
                    ) : null}
                  </p>
                  <address className="mt-1 not-italic leading-relaxed text-muted">
                    {location.streetAddress}
                    <br />
                    {location.postalCode} {location.addressLocality}
                  </address>
                  <a
                    href={`tel:${location.telephone.replace(/\s/g, "")}`}
                    className="mt-1 inline-block text-cyan transition-opacity hover:opacity-80"
                  >
                    {location.telephone}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="flex flex-col gap-8 border-t border-white/5 pt-8 sm:flex-row sm:items-end sm:justify-between">
          <div className="flex flex-col gap-4 sm:items-end">
            <div className="flex items-center gap-6">
              <Link
                href="/blog"
                className="nav-link text-sm"
              >
                {FOOTER.blog}
              </Link>
              <a
                href={SITE.telegramUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="nav-link text-sm text-cyan"
              >
                {FOOTER.telegram}
              </a>
              <a
                href={`mailto:${SITE.email}`}
                className="nav-link text-sm"
              >
                {SITE.email}
              </a>
            </div>
            <p className="text-sm text-muted">
              © {new Date().getFullYear()} {SITE.brand}. {FOOTER.rights}
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
