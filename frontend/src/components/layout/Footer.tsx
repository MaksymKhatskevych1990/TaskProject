import Link from "next/link";
import { BrandLogo } from "@/components/layout/BrandLogo";
import { FOOTER, SITE } from "@/lib/site-data";

export function Footer() {
  return (
    <footer className="border-t border-white/5 py-12">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="flex flex-col gap-8 sm:flex-row sm:items-end sm:justify-between">
          <Link href="/" className="flex shrink-0 items-center" aria-label={`${SITE.brand} — на головну`}>
            <BrandLogo emblemSize="sm" />
          </Link>
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
