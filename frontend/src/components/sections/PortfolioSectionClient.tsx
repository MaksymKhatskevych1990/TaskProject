"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { SECTIONS } from "@/lib/site-data";
import type { PortfolioProjectDetail, PortfolioProjectListItem } from "@/lib/portfolio-api";
import { cn } from "@/lib/utils";

function PortfolioPreview({
  title,
  gradient,
  coverImage,
}: {
  title: string;
  gradient: string;
  coverImage: string | null;
}) {
  return (
    <div className="overflow-hidden border border-[var(--card-border)] bg-[var(--card-elevated)]">
      <div className="flex items-center gap-2 border-b border-[var(--card-border)] px-3 py-2">
        <span className="font-[family-name:var(--font-jetbrains)] text-[9px] tracking-wide text-muted">
          {title.toLowerCase().replace(/\s+/g, "")}.ua
        </span>
      </div>
      <div className={cn("relative aspect-[16/10] bg-gradient-to-br", gradient)}>
        {coverImage ? (
          <Image
            src={coverImage}
            alt={title}
            fill
            className="object-cover object-top transition-transform duration-700 group-hover:scale-[1.02]"
            sizes="(max-width: 768px) 85vw, 420px"
          />
        ) : (
          <div className="flex h-full items-center justify-center p-6">
            <div className="w-full space-y-2">
              <div className="h-2 w-2/3 bg-[var(--card-border)]" />
              <div className="h-1.5 w-full bg-[var(--card-border)]" />
              <div className="h-1.5 w-4/5 bg-[var(--card-border)]" />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function PortfolioCaseModal({
  project,
  onClose,
}: {
  project: PortfolioProjectDetail;
  onClose: () => void;
}) {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };

    document.addEventListener("keydown", handleKeyDown);
    document.body.style.overflow = "hidden";

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [onClose]);

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center sm:items-center sm:p-6"
      role="presentation"
      onClick={onClose}
    >
      <div className="absolute inset-0 bg-background/90 backdrop-blur-sm" />

      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="portfolio-case-title"
        className="relative z-10 flex max-h-[92vh] w-full max-w-3xl flex-col overflow-hidden border border-[var(--card-border)] bg-[var(--card)] sm:max-h-[85vh]"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4 border-b border-[var(--card-border)] px-6 py-5">
          <div>
            <p className="label-mono">{project.category}</p>
            <h3
              id="portfolio-case-title"
              className="mt-1 editorial-heading text-xl sm:text-2xl"
            >
              {project.title}
            </h3>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-2 text-muted transition-colors hover:text-foreground"
            aria-label="Закрити"
          >
            ✕
          </button>
        </div>

        <div className="overflow-y-auto px-6 py-6">
          <PortfolioPreview
            title={project.title}
            gradient={project.gradient}
            coverImage={project.coverImage}
          />

          {project.hasCaseStudy ? (
            <div className="mt-8 grid grid-cols-3 items-center gap-4 border-t border-[var(--card-border)] pt-8">
              <div>
                <p className="label-mono mb-1">{SECTIONS.cases.before}</p>
                <p className="text-sm text-muted">{project.before}</p>
              </div>
              <p className="text-center font-[family-name:var(--font-exo2)] text-2xl font-bold accent-warm-text">
                {project.metric}
              </p>
              <div className="text-right">
                <p className="label-mono mb-1">{SECTIONS.cases.after}</p>
                <p className="text-sm font-medium accent-text">{project.after}</p>
              </div>
            </div>
          ) : null}

          <p className="mt-6 text-sm leading-relaxed text-muted">
            {project.caseDescription || project.description}
          </p>

          <div className="mt-4 flex flex-wrap gap-2">
            {project.tags.map((tag) => (
              <span
                key={tag}
                className="border border-[var(--card-border)] px-2.5 py-0.5 text-[11px] text-muted"
              >
                {tag}
              </span>
            ))}
          </div>

          {project.gallery.length > 0 ? (
            <div className="mt-8 grid gap-3 sm:grid-cols-2">
              {project.gallery.map((item) =>
                item.imageUrl ? (
                  <figure
                    key={`${item.ordering}-${item.imageUrl}`}
                    className="overflow-hidden border border-[var(--card-border)]"
                  >
                    <div className="relative aspect-[16/10]">
                      <Image
                        src={item.imageUrl}
                        alt={item.caption || project.title}
                        fill
                        className="object-cover"
                        sizes="(max-width: 768px) 100vw, 384px"
                      />
                    </div>
                    {item.caption ? (
                      <figcaption className="px-3 py-2 text-xs text-muted">
                        {item.caption}
                      </figcaption>
                    ) : null}
                  </figure>
                ) : null,
              )}
            </div>
          ) : null}
        </div>

        <div className="flex flex-col gap-3 border-t border-[var(--card-border)] px-6 py-5 sm:flex-row">
          {project.clientUrl ? (
            <a
              href={project.clientUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-secondary flex-1 py-2.5 text-center"
            >
              Відкрити сайт
            </a>
          ) : null}
          <Link
            href="/#contact"
            onClick={onClose}
            className="btn-primary flex-1 py-2.5 text-center"
          >
            {SECTIONS.portfolio.viewAll}
          </Link>
        </div>
      </div>
    </div>
  );
}

function PortfolioScroll({
  projects,
  onOpen,
}: {
  projects: PortfolioProjectListItem[];
  onOpen: (slug: string) => void;
}) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  const updateScrollState = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;

    setCanScrollLeft(el.scrollLeft > 4);
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 4);
  }, []);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;

    updateScrollState();

    const onScroll = () => updateScrollState();
    const onResize = () => updateScrollState();

    const onWheel = (event: WheelEvent) => {
      if (Math.abs(event.deltaY) <= Math.abs(event.deltaX)) return;
      event.preventDefault();
      el.scrollLeft += event.deltaY;
    };

    el.addEventListener("scroll", onScroll, { passive: true });
    el.addEventListener("wheel", onWheel, { passive: false });
    window.addEventListener("resize", onResize);

    return () => {
      el.removeEventListener("scroll", onScroll);
      el.removeEventListener("wheel", onWheel);
      window.removeEventListener("resize", onResize);
    };
  }, [projects.length, updateScrollState]);

  const scrollBy = (direction: "left" | "right") => {
    const el = scrollRef.current;
    if (!el) return;
    const amount = Math.min(el.clientWidth * 0.85, 480);
    el.scrollBy({ left: direction === "left" ? -amount : amount, behavior: "smooth" });
  };

  return (
    <div className="relative">
      {/* Fade edges */}
      <div
        className={cn(
          "pointer-events-none absolute inset-y-0 left-0 z-10 w-16 bg-gradient-to-r from-background to-transparent transition-opacity duration-300 sm:w-24",
          canScrollLeft ? "opacity-100" : "opacity-0",
        )}
      />
      <div
        className={cn(
          "pointer-events-none absolute inset-y-0 right-0 z-10 w-16 bg-gradient-to-l from-background to-transparent transition-opacity duration-300 sm:w-24",
          canScrollRight ? "opacity-100" : "opacity-0",
        )}
      />

      {/* Nav buttons */}
      <button
        type="button"
        onClick={() => scrollBy("left")}
        aria-label="Попередній проєкт"
        className={cn(
          "absolute left-2 top-[38%] z-20 flex h-10 w-10 -translate-y-1/2 items-center justify-center border border-[var(--card-border)] bg-background/90 text-foreground backdrop-blur-sm transition-all hover:border-accent hover:text-accent-bright sm:left-6",
          canScrollLeft ? "opacity-100" : "pointer-events-none opacity-0",
        )}
      >
        ←
      </button>
      <button
        type="button"
        onClick={() => scrollBy("right")}
        aria-label="Наступний проєкт"
        className={cn(
          "absolute right-2 top-[38%] z-20 flex h-10 w-10 -translate-y-1/2 items-center justify-center border border-[var(--card-border)] bg-background/90 text-foreground backdrop-blur-sm transition-all hover:border-accent hover:text-accent-bright sm:right-6",
          canScrollRight ? "opacity-100" : "pointer-events-none opacity-0",
        )}
      >
        →
      </button>

      <div
        ref={scrollRef}
        className="horizontal-scroll px-5 sm:px-8 lg:px-12"
        role="region"
        aria-label="Портфоліо проєктів"
        tabIndex={0}
      >
        {projects.map((project) => (
          <button
            key={project.slug}
            type="button"
            onClick={() => onOpen(project.slug)}
            className="group w-[min(85vw,420px)] cursor-pointer text-left"
          >
            <PortfolioPreview
              title={project.title}
              gradient={project.gradient}
              coverImage={project.coverImage}
            />
            <div className="mt-4 pr-4">
              <span className="label-mono text-accent-bright">{project.category}</span>
              <h3 className="mt-1 text-lg font-semibold text-foreground">{project.title}</h3>
              <p className="mt-2 line-clamp-2 text-sm text-muted">
                {project.description}
              </p>
              {project.hasCaseStudy ? (
                <p className="mt-3 text-sm font-medium accent-warm-text">
                  {project.metric}
                </p>
              ) : null}
            </div>
          </button>
        ))}
      </div>

      <p className="mt-2 px-5 text-center font-[family-name:var(--font-jetbrains)] text-[10px] tracking-widest text-muted sm:px-8 lg:px-12">
        ← прокрутіть або використайте колесо миші →
      </p>
    </div>
  );
}

type PortfolioSectionClientProps = {
  projects: PortfolioProjectListItem[];
  detailsBySlug: Record<string, PortfolioProjectDetail>;
};

export function PortfolioSectionClient({
  projects,
  detailsBySlug,
}: PortfolioSectionClientProps) {
  const [selectedSlug, setSelectedSlug] = useState<string | null>(null);

  const openProject = useCallback((slug: string) => {
    if (detailsBySlug[slug]) setSelectedSlug(slug);
  }, [detailsBySlug]);

  const closeProject = useCallback(() => setSelectedSlug(null), []);
  const selectedProject = selectedSlug ? detailsBySlug[selectedSlug] : null;

  return (
    <>
      <section id="portfolio" className="overflow-hidden py-24 sm:py-32">
        <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
          <div className="mb-12 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="section-number mb-4">02</p>
              <h2 className="editorial-heading text-3xl sm:text-4xl">
                {SECTIONS.portfolio.title}
              </h2>
              <p className="mt-3 max-w-md text-sm text-muted">
                {SECTIONS.portfolio.subtitle}
              </p>
            </div>
            <Link href="/#contact" className="btn-secondary shrink-0 self-start sm:self-auto">
              {SECTIONS.portfolio.viewAll}
            </Link>
          </div>
        </div>

        <PortfolioScroll projects={projects} onOpen={openProject} />
      </section>

      {selectedProject ? (
        <PortfolioCaseModal project={selectedProject} onClose={closeProject} />
      ) : null}
    </>
  );
}
