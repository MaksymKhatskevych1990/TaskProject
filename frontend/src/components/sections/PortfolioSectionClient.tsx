"use client";

import Image from "next/image";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";
import { SECTIONS } from "@/lib/site-data";
import type { PortfolioProjectDetail, PortfolioProjectListItem } from "@/lib/portfolio-api";
import { cn } from "@/lib/utils";

const accentClasses = {
  cyan: "group-hover:border-cyan/40 group-hover:shadow-cyan/10",
  violet: "group-hover:border-violet/40 group-hover:shadow-violet/10",
  green: "group-hover:border-emerald-400/40 group-hover:shadow-emerald-400/10",
  orange: "group-hover:border-orange-400/40 group-hover:shadow-orange-400/10",
} as const;

const tagColors: Record<string, string> = {
  Дизайн: "bg-violet/10 text-violet",
  "UI/UX": "bg-violet/10 text-violet",
  Брендинг: "bg-violet/10 text-violet",
  Розробка: "bg-cyan/10 text-cyan",
  Лендинг: "bg-cyan/10 text-cyan",
  "E-commerce": "bg-emerald-400/10 text-emerald-400",
  SEO: "bg-emerald-400/10 text-emerald-400",
  Аналітика: "bg-emerald-400/10 text-emerald-400",
  Бот: "bg-cyan/10 text-cyan",
  CRM: "bg-cyan/10 text-cyan",
  CMS: "bg-cyan/10 text-cyan",
  "A/B": "bg-orange-400/10 text-orange-400",
};

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
    <div className="overflow-hidden rounded-xl border border-white/5 bg-[#070b18]">
      <div className="flex items-center gap-1.5 border-b border-white/5 px-3 py-2">
        <span className="h-2 w-2 rounded-full bg-red-400/70" />
        <span className="h-2 w-2 rounded-full bg-yellow-400/70" />
        <span className="h-2 w-2 rounded-full bg-green-400/70" />
        <span className="ml-1 truncate font-[family-name:var(--font-jetbrains)] text-[9px] text-muted">
          {title.toLowerCase().replace(/\s+/g, "")}.ua
        </span>
      </div>
      <div className={cn("relative aspect-[16/10] bg-gradient-to-br", gradient)}>
        {coverImage ? (
          <Image
            src={coverImage}
            alt={title}
            fill
            className="object-cover object-top transition-transform duration-500 group-hover:scale-[1.03]"
            sizes="(max-width: 768px) 100vw, 33vw"
          />
        ) : (
          <div className="p-4">
            <div className="space-y-2">
              <div className="h-2.5 w-2/3 rounded bg-white/20" />
              <div className="h-1.5 w-full rounded bg-white/10" />
              <div className="h-1.5 w-4/5 rounded bg-white/10" />
            </div>
            <div className="mt-4 grid grid-cols-3 gap-2">
              {[1, 2, 3].map((i) => (
                <div key={i} className="aspect-square rounded-lg bg-white/10" />
              ))}
            </div>
            <div className="mt-3 h-6 w-24 rounded-full bg-white/20" />
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
      if (event.key === "Escape") {
        onClose();
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    document.body.style.overflow = "hidden";

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [onClose]);

  if (!project) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center p-0 sm:items-center sm:p-4"
      role="presentation"
      onClick={onClose}
    >
      <div className="absolute inset-0 bg-[#070b18]/85 backdrop-blur-sm" />

      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="portfolio-case-title"
        className="relative z-10 flex max-h-[92vh] w-full max-w-3xl flex-col overflow-hidden rounded-t-2xl border border-white/10 bg-card shadow-2xl sm:rounded-2xl"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-4 border-b border-white/5 px-5 py-4 sm:px-6">
          <div>
            <p className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-wider text-cyan">
              {project.category}
            </p>
            <h3
              id="portfolio-case-title"
              className="mt-1 font-[family-name:var(--font-exo2)] text-xl font-bold sm:text-2xl"
            >
              {project.title}
            </h3>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="rounded-full border border-white/10 px-3 py-1.5 text-sm text-muted transition-colors hover:border-white/20 hover:text-foreground"
            aria-label="Закрити"
          >
            ✕
          </button>
        </div>

        <div className="overflow-y-auto px-5 py-5 sm:px-6">
          <PortfolioPreview
            title={project.title}
            gradient={project.gradient}
            coverImage={project.coverImage}
          />

          {project.hasCaseStudy ? (
            <div className="mt-6 grid grid-cols-3 items-center gap-2 rounded-xl border border-white/5 bg-white/5 px-4 py-4">
              <div className="min-w-0">
                <p className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase text-muted">
                  {SECTIONS.cases.before}
                </p>
                <p className="mt-1 truncate text-sm">{project.before}</p>
              </div>
              <p className="gradient-text text-center font-[family-name:var(--font-exo2)] text-2xl font-bold">
                {project.metric}
              </p>
              <div className="min-w-0 text-right">
                <p className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase text-muted">
                  {SECTIONS.cases.after}
                </p>
                <p className="mt-1 truncate text-sm font-medium text-cyan">
                  {project.after}
                </p>
              </div>
            </div>
          ) : null}

          <p className="mt-5 text-sm leading-relaxed text-muted">
            {project.caseDescription || project.description}
          </p>

          <div className="mt-4 flex flex-wrap gap-1.5">
            {project.tags.map((tag) => (
              <span
                key={tag}
                className={cn(
                  "rounded-full px-2.5 py-0.5 text-[11px] font-medium",
                  tagColors[tag] ?? "bg-white/5 text-muted",
                )}
              >
                {tag}
              </span>
            ))}
          </div>

          {project.gallery.length > 0 ? (
            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              {project.gallery.map((item) =>
                item.imageUrl ? (
                  <figure
                    key={`${item.ordering}-${item.imageUrl}`}
                    className="overflow-hidden rounded-xl border border-white/5"
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

        <div className="flex flex-col gap-3 border-t border-white/5 px-5 py-4 sm:flex-row sm:px-6">
            {project.clientUrl ? (
              <a
                href={project.clientUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex flex-1 items-center justify-center rounded-full border border-white/10 px-5 py-2.5 text-sm font-medium transition-colors hover:border-cyan/40 hover:text-cyan"
              >
                Відкрити сайт
              </a>
            ) : null}
            <Link
              href="/#contact"
              onClick={onClose}
              className="inline-flex flex-1 items-center justify-center rounded-full bg-gradient-to-r from-cyan to-violet px-5 py-2.5 text-sm font-semibold text-[#070b18] transition-opacity hover:opacity-90"
            >
              {SECTIONS.portfolio.viewAll}
          </Link>
        </div>
      </div>
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
    if (detailsBySlug[slug]) {
      setSelectedSlug(slug);
    }
  }, [detailsBySlug]);

  const closeProject = useCallback(() => {
    setSelectedSlug(null);
  }, []);

  const selectedProject = selectedSlug ? detailsBySlug[selectedSlug] : null;

  return (
    <>
      <section id="portfolio" className="relative py-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mb-12 text-center">
            <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
              {SECTIONS.portfolio.eyebrow}
            </p>
            <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
              {SECTIONS.portfolio.title}
            </h2>
            <p className="mx-auto mt-3 max-w-2xl text-sm leading-relaxed text-muted">
              {SECTIONS.portfolio.subtitle}
            </p>
          </div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {projects.map((project) => (
              <button
                key={project.slug}
                type="button"
                onClick={() => openProject(project.slug)}
                className={cn(
                  "group flex cursor-pointer flex-col rounded-2xl border border-white/5 bg-card p-5 text-left transition-all duration-300 hover:shadow-lg",
                  accentClasses[project.accent],
                )}
              >
                <PortfolioPreview
                  title={project.title}
                  gradient={project.gradient}
                  coverImage={project.coverImage}
                />

                <div className="mt-4 flex flex-1 flex-col">
                  <span className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase tracking-wider text-cyan">
                    {project.category}
                  </span>
                  <h3 className="mt-1 font-[family-name:var(--font-exo2)] text-lg font-semibold">
                    {project.title}
                  </h3>
                  <p className="mt-2 flex-1 text-sm leading-relaxed text-muted">
                    {project.description}
                  </p>

                  {project.hasCaseStudy ? (
                    <p className="mt-3 font-[family-name:var(--font-exo2)] text-sm font-semibold text-cyan">
                      {project.metric}
                    </p>
                  ) : null}

                  <div className="mt-4 flex flex-wrap gap-1.5">
                    {project.tags.map((tag) => (
                      <span
                        key={tag}
                        className={cn(
                          "rounded-full px-2.5 py-0.5 text-[11px] font-medium",
                          tagColors[tag] ?? "bg-white/5 text-muted",
                        )}
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </button>
            ))}
          </div>

          <div className="mt-12 text-center">
            <Link
              href="/#contact"
              className="inline-flex rounded-full bg-gradient-to-r from-cyan to-violet px-6 py-3 text-sm font-semibold text-[#070b18] transition-opacity hover:opacity-90"
            >
              {SECTIONS.portfolio.viewAll}
            </Link>
          </div>
        </div>
      </section>

      {selectedProject ? (
        <PortfolioCaseModal project={selectedProject} onClose={closeProject} />
      ) : null}
    </>
  );
}
