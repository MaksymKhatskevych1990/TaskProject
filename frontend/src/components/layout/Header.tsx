import Link from "next/link";
import { NAV_LINKS, SITE } from "@/lib/site-data";

export function Header() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/5 bg-[#070b18]/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2.5">
          <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-cyan to-violet text-lg">
            ⚡
          </span>
          <span className="font-[family-name:var(--font-exo2)] text-lg font-bold tracking-tight">
            {SITE.brand}
          </span>
        </Link>

        <nav className="hidden items-center gap-8 md:flex">
          {NAV_LINKS.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm text-muted transition-colors hover:text-foreground"
            >
              {link.label}
            </a>
          ))}
        </nav>

        <a
          href="#contact"
          className="rounded-full bg-gradient-to-r from-cyan to-violet px-4 py-2 text-sm font-semibold text-[#070b18] transition-opacity hover:opacity-90"
        >
          Обсудить проект
        </a>
      </div>
    </header>
  );
}
