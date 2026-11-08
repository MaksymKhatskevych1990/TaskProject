import Link from "next/link";
import { BrandLogo } from "@/components/layout/BrandLogo";
import { getSiteContent } from "@/lib/site-content";
import { formatUaPhone, isPlaceholderPhone, toTelHref } from "@/lib/phone";
import { isRemoteOffice } from "@/lib/office";
import { SERVICE_PAGES } from "@/lib/marketing-pages";

export async function Footer() {
  const content = await getSiteContent();
  const hq = content.offices.find((location) => location.isHeadquarters);
  const otherLocations = content.offices.filter((location) => !location.isHeadquarters);

  return (
    <footer className="border-t border-[var(--card-border)]">
      <div className="mx-auto max-w-[90rem] px-5 py-16 sm:px-8 lg:px-12">
        <div className="grid gap-12 lg:grid-cols-[1fr_2fr] lg:gap-20">
          <div>
            <Link href="/" aria-label={`${content.brand} — на головну`}>
              <BrandLogo emblemSize="sm" brandShort={content.brandShort} />
            </Link>
            <p className="mt-6 max-w-xs text-sm leading-relaxed text-muted">
              {content.footer.about}
            </p>
            <div className="mt-8 flex flex-col gap-2 text-sm">
              {!isPlaceholderPhone(content.phone) ? (
                <a
                  href={toTelHref(content.phone)}
                  className="text-foreground transition-colors hover:text-accent-bright"
                >
                  {formatUaPhone(content.phone)}
                </a>
              ) : null}
              <a
                href={`mailto:${content.email}`}
                className="text-foreground transition-colors hover:text-accent-bright"
              >
                {content.email}
              </a>
              <a
                href={content.telegramUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-muted transition-colors hover:text-accent-bright"
              >
                @{content.telegramUsername}
              </a>
            </div>
          </div>

          <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3">
            <div>
              <p className="label-mono mb-6">Послуги</p>
              <ul className="grid grid-cols-1 gap-2 text-sm text-muted sm:grid-cols-2 lg:grid-cols-1">
                {SERVICE_PAGES.map((page) => (
                  <li key={page.slug}>
                    <Link href={page.href} className="hover:text-foreground">
                      {page.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="label-mono mb-6">{content.footer.offices}</p>
              <div className="grid gap-8">
              {hq ? (
                <div>
                  <p className="text-sm font-medium">
                    {hq.name}
                    {hq.isHeadquarters ? (
                      <span className="ml-2 label-mono text-accent">HQ</span>
                    ) : null}
                  </p>
                  <address className="mt-2 not-italic text-sm leading-relaxed text-muted">
                    {isRemoteOffice(hq) ? (
                      <>
                        Віддалена робота
                        <br />
                        {hq.addressLocality}, Україна
                      </>
                    ) : (
                      <>
                        {hq.streetAddress}
                        <br />
                        {hq.postalCode} {hq.addressLocality}
                      </>
                    )}
                  </address>
                </div>
              ) : null}
              {otherLocations.map((location) => (
                <div key={location.id}>
                  <p className="text-sm font-medium">{location.name}</p>
                  <address className="mt-2 not-italic text-sm leading-relaxed text-muted">
                    {isRemoteOffice(location) ? (
                      <>
                        Віддалена робота
                        <br />
                        {location.addressLocality}
                      </>
                    ) : (
                      <>
                        {location.streetAddress}
                        <br />
                        {location.postalCode} {location.addressLocality}
                      </>
                    )}
                  </address>
                </div>
              ))}
              </div>
            </div>
            <div>
              <p className="label-mono mb-6">Документи</p>
              <ul className="space-y-2 text-sm text-muted">
                <li>
                  <Link href="/privacy" className="hover:text-foreground">
                    Конфіденційність
                  </Link>
                </li>
                <li>
                  <Link href="/oferta" className="hover:text-foreground">
                    Публічна оферта
                  </Link>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-16 flex flex-col gap-4 border-t border-[var(--card-border)] pt-8 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-xs text-muted">
            © {new Date().getFullYear()} {content.brand}. {content.footer.rights}
          </p>
          <div className="flex items-center gap-6">
            <Link href="/privacy" className="nav-link text-xs">
              Конфіденційність
            </Link>
            <Link href="/oferta" className="nav-link text-xs">
              Оферта
            </Link>
            <Link href="/blog" className="nav-link text-xs">
              {content.footer.blog}
            </Link>
            <Link href="/#faq" className="nav-link text-xs">
              {content.footer.faq}
            </Link>
            <a
              href={content.telegramUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="nav-link text-xs"
            >
              {content.footer.telegram}
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
