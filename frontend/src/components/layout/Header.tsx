"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { BrandLogo } from "@/components/layout/BrandLogo";
import { HEADER, HERO, NAV_LINKS, SITE } from "@/lib/site-data";
import { cn } from "@/lib/utils";

export function Header() {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const [pastHero, setPastHero] = useState(false);
  const showHeaderCta = pathname !== "/" || pastHero;

  useEffect(() => {
    const onScroll = () => {
      setScrolled(window.scrollY > 60);
      setPastHero(window.scrollY > window.innerHeight * 0.75);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    document.body.style.overflow = menuOpen ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  const closeMenu = () => setMenuOpen(false);

  return (
    <header
      className={cn(
        "fixed inset-x-0 top-0 z-50 transition-all duration-500",
        scrolled
          ? "border-b border-[var(--card-border)] bg-background/90 backdrop-blur-md"
          : "bg-transparent",
      )}
    >
      <div className="mx-auto flex h-[4.5rem] max-w-[90rem] items-center justify-between px-5 sm:px-8 lg:px-12">
        <Link
          href="/"
          className="flex shrink-0 items-center"
          onClick={closeMenu}
          aria-label={`${SITE.brand} — на головну`}
        >
          <BrandLogo emblemVariant="header" emblemSize="sm" />
        </Link>

        <nav
          className="hidden items-center gap-8 md:flex"
          aria-label={HEADER.navigation}
        >
          {NAV_LINKS.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="nav-link focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-accent/50"
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-4">
          <Link
            href="/#contact"
            className={cn(
              "btn-primary hidden px-5 py-2.5 text-[13px] transition-all duration-300 sm:inline-flex",
              showHeaderCta
                ? "translate-y-0 opacity-100"
                : "pointer-events-none translate-y-1 opacity-0",
            )}
            tabIndex={showHeaderCta ? 0 : -1}
            aria-hidden={!showHeaderCta}
          >
            {HERO.primaryCta}
          </Link>

          <button
            type="button"
            className="flex flex-col items-end gap-[5px] p-2 md:hidden"
            aria-expanded={menuOpen}
            aria-controls="mobile-nav"
            aria-label={menuOpen ? HEADER.closeMenu : HEADER.openMenu}
            onClick={() => setMenuOpen((open) => !open)}
          >
            <span
              className={cn(
                "block h-px w-6 bg-foreground transition-all duration-300",
                menuOpen && "translate-y-[6px] rotate-45",
              )}
            />
            <span
              className={cn(
                "block h-px w-4 bg-foreground transition-all duration-300",
                menuOpen && "opacity-0",
              )}
            />
            <span
              className={cn(
                "block h-px w-6 bg-foreground transition-all duration-300",
                menuOpen && "-translate-y-[6px] -rotate-45",
              )}
            />
          </button>
        </div>
      </div>

      <div
        className={cn(
          "fixed inset-0 z-40 bg-background transition-all duration-500 md:hidden",
          menuOpen
            ? "pointer-events-auto opacity-100"
            : "pointer-events-none opacity-0",
        )}
        aria-hidden={!menuOpen}
      >
        <nav
          id="mobile-nav"
          className="flex h-full flex-col justify-center px-8"
          aria-label={HEADER.navigation}
        >
          <ul className="space-y-6">
            {NAV_LINKS.map((link, index) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  onClick={closeMenu}
                  className="group flex items-baseline gap-4"
                >
                  <span className="section-number opacity-40">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span className="editorial-heading text-3xl text-foreground transition-colors group-hover:text-accent-bright">
                    {link.label}
                  </span>
                </Link>
              </li>
            ))}
          </ul>

          <div className="mt-16">
            <Link
              href="/#contact"
              onClick={closeMenu}
              className="btn-primary px-8 py-3.5"
            >
              {HERO.primaryCta}
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
}
