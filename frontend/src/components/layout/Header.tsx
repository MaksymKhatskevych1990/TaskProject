"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { HEADER, HERO, NAV_LINKS, SITE } from "@/lib/site-data";
import { cn } from "@/lib/utils";

export function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  const closeMenu = () => setMenuOpen(false);

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-white/5 bg-[#070b18]/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link href="/" className="flex items-center gap-2.5" onClick={closeMenu}>
          <span
            aria-hidden="true"
            className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-cyan to-violet text-lg"
          >
            ⚡
          </span>
          <span className="font-[family-name:var(--font-exo2)] text-lg font-bold tracking-tight">
            {SITE.brand}
          </span>
        </Link>

        <nav className="hidden items-center gap-8 md:flex" aria-label={HEADER.navigation}>
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm text-muted transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan/50"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <Link
            href="/#contact"
            className="hidden rounded-full bg-gradient-to-r from-cyan to-violet px-4 py-2 text-sm font-semibold text-[#070b18] transition-opacity hover:opacity-90 sm:inline-flex"
          >
            {HERO.primaryCta}
          </Link>

          <button
            type="button"
            className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-white/10 text-foreground md:hidden"
            aria-expanded={menuOpen}
            aria-controls="mobile-nav"
            aria-label={menuOpen ? HEADER.closeMenu : HEADER.openMenu}
            onClick={() => setMenuOpen((open) => !open)}
          >
            <span className="sr-only">{menuOpen ? HEADER.closeMenu : HEADER.openMenu}</span>
            <svg
              aria-hidden="true"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              {menuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>
      </div>

      <div
        className={cn(
          "fixed inset-0 top-16 z-40 md:hidden",
          menuOpen ? "pointer-events-auto" : "pointer-events-none",
        )}
        aria-hidden={!menuOpen}
      >
        <button
          type="button"
          className={cn(
            "absolute inset-0 bg-[#070b18]/80 transition-opacity duration-300",
            menuOpen ? "opacity-100" : "opacity-0",
          )}
          aria-label={HEADER.closeMenu}
          onClick={closeMenu}
        />

        <nav
          id="mobile-nav"
          className={cn(
            "relative border-b border-white/5 bg-[#0d1224] px-4 py-4 shadow-2xl transition-all duration-300",
            menuOpen ? "translate-y-0 opacity-100" : "-translate-y-2 opacity-0",
          )}
          aria-label={HEADER.navigation}
        >
          <ul className="space-y-1">
            {NAV_LINKS.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  onClick={closeMenu}
                  className="block rounded-xl px-4 py-3 text-base font-medium text-foreground transition-colors hover:bg-white/5 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-cyan/50"
                >
                  {link.label}
                </Link>
              </li>
            ))}
            <li className="pt-2">
              <Link
                href="/#contact"
                onClick={closeMenu}
                className="block rounded-full bg-gradient-to-r from-cyan to-violet px-4 py-3 text-center text-sm font-semibold text-[#070b18]"
              >
                {HERO.primaryCta}
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
