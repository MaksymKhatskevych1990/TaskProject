import Link from "next/link";
import { BrandLogo } from "@/components/layout/BrandLogo";
import { FOOTER, GEO_LOCATIONS, SITE } from "@/lib/site-data";

export function Footer() {
  const hq = GEO_LOCATIONS.find((l) => l.isHeadquarters);
  const otherLocations = GEO_LOCATIONS.filter((l) => !l.isHeadquarters);

  return (
    <footer className="border-t border-[var(--card-border)]">
      <div className="mx-auto max-w-[90rem] px-5 py-16 sm:px-8 lg:px-12">
        <div className="grid gap-12 lg:grid-cols-[1fr_2fr] lg:gap-20">
          <div>
            <Link href="/" aria-label={`${SITE.brand} — на головну`}>
              <BrandLogo emblemSize="sm" />
            </Link>
            <p className="mt-6 max-w-xs text-sm leading-relaxed text-muted">
              IT-студія з Києва. Працюємо з клієнтами по всій Україні та Європі — повністю віддалено.
            </p>
            <div className="mt-8 flex flex-col gap-2 text-sm">
              <a
                href={`mailto:${SITE.email}`}
                className="text-foreground transition-colors hover:text-accent-bright"
              >
                {SITE.email}
              </a>
              <a
                href={SITE.telegramUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted transition-colors hover:text-accent-bright"
              >
                @{SITE.telegramUsername}
              </a>
            </div>
          </div>

          <div>
            <p className="label-mono mb-6">Офіси</p>
            <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {hq ? (
                <div>
                  <p className="text-sm font-medium">
                    {hq.name}
                    <span className="ml-2 label-mono text-accent">HQ</span>
                  </p>
                  <address className="mt-2 not-italic text-sm leading-relaxed text-muted">
                    {hq.streetAddress}
                    <br />
                    {hq.postalCode} {hq.addressLocality}
                  </address>
                </div>
              ) : null}
              {otherLocations.map((location) => (
                <div key={location.id}>
                  <p className="text-sm font-medium">{location.name}</p>
                  <address className="mt-2 not-italic text-sm leading-relaxed text-muted">
                    {location.streetAddress}
                    <br />
                    {location.postalCode} {location.addressLocality}
                  </address>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-16 flex flex-col gap-4 border-t border-[var(--card-border)] pt-8 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs text-muted">
            © {new Date().getFullYear()} {SITE.brand}. {FOOTER.rights}
          </p>
          <div className="flex items-center gap-6">
            <Link href="/blog" className="nav-link text-xs">
              {FOOTER.blog}
            </Link>
            <Link href="/#faq" className="nav-link text-xs">
              FAQ
            </Link>
            <a
              href={SITE.telegramUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="nav-link text-xs"
            >
              {FOOTER.telegram}
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
