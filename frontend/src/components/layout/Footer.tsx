import Link from "next/link";
import { BrandLogo } from "@/components/layout/BrandLogo";
import { FOOTER, SITE } from "@/lib/site-data";

export function Footer() {
  return (
    <footer className="border-t border-white/5 py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-4 sm:flex-row sm:px-6">
        <Link href="/" className="flex shrink-0 items-center" aria-label={`${SITE.brand} — на головну`}>
          <BrandLogo emblemSize="sm" />
        </Link>
        <p className="text-sm text-muted">
          © {new Date().getFullYear()} {SITE.brand}. {FOOTER.rights}
        </p>
        <div className="flex items-center gap-6">
          <Link
            href="/blog"
            className="text-sm text-muted transition-colors hover:text-foreground"
          >
            {FOOTER.blog}
          </Link>
          <a
            href={SITE.telegramUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-cyan transition-opacity hover:opacity-80"
          >
            {FOOTER.telegram}
          </a>
        </div>
      </div>
    </footer>
  );
}
