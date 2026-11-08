"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { BrowserMockup } from "@/components/portfolio/BrowserMockup";
import { publicCoverUrl, staticGallery } from "@/lib/portfolio-covers";
import { useSiteContent } from "@/components/site-content/SiteContentProvider";
import type { PortfolioProjectDetail, PortfolioProjectListItem } from "@/lib/portfolio-api";

function pad(n: number) {
  return String(n).padStart(2, "0");
}

function sortProjects(projects: PortfolioProjectListItem[]) {
  return [...projects].sort((a, b) => {
    if (a.featured !== b.featured) return a.featured ? -1 : 1;
    return 0;
  });
}

function isPublicClientUrl(url: string): boolean {
  if (!url) return false;
  try {
    const parsed = new URL(url);
    return !["localhost", "127.0.0.1"].includes(parsed.hostname);
  } catch {
    return false;
  }
}

function ProjectTile({
  project,
  index,
}: {
  project: PortfolioProjectListItem;
  index: number;
}) {
  return (
    <Link
      href={`/works/${project.slug}`}
      className="proj-card group flex cursor-pointer flex-col overflow-hidden border border-[var(--card-border)] bg-[var(--card)] transition-[border-color,transform] duration-400 hover:-translate-y-0.5 hover:border-accent/35"
    >
      <div className="relative aspect-[16/10] w-full shrink-0 overflow-hidden">
        <BrowserMockup project={project} />
      </div>

      <div className="flex flex-col gap-2 border-t border-[var(--card-border)] px-4 py-3.5 sm:px-5 sm:py-4">
        <div className="flex items-start justify-between gap-3">
          <div className="flex min-w-0 flex-wrap items-center gap-x-2.5 gap-y-1">
            <span className="label-mono text-accent-bright">{pad(index + 1)}</span>
            <span className="label-mono truncate text-muted">{project.category}</span>
          </div>
          {project.hasCaseStudy ? (
            <span className="shrink-0 font-[family-name:var(--font-exo2)] text-lg font-bold tracking-tight accent-warm-text sm:text-xl">
              {project.metric}
            </span>
          ) : null}
        </div>

        <div className="flex items-end justify-between gap-3">
          <div className="min-w-0">
            <h3 className="editorial-heading text-lg leading-snug text-foreground transition-colors group-hover:text-accent-bright sm:text-xl">
              {project.title}
            </h3>
            <p className="mt-1 line-clamp-1 text-sm text-muted">
              {project.description}
            </p>
          </div>
          <span
            aria-hidden="true"
            className="mb-0.5 shrink-0 font-[family-name:var(--font-jetbrains)] text-sm text-muted transition-all duration-300 group-hover:translate-x-0.5 group-hover:text-accent-bright"
          >
            →
          </span>
        </div>
      </div>
    </Link>
  );
}

export function PortfolioCaseModal({
  project,
  onClose,
}: {
  project: PortfolioProjectDetail;
  onClose: () => void;
}) {
  const content = useSiteContent();
  const [lightbox, setLightbox] = useState<string | null>(null);

  const photos = useMemo(() => {
    const fallback = staticGallery(project.slug);
    if (fallback.length > 0) return fallback;

    const fromGallery = project.gallery
      .map((item) => ({
        url: publicCoverUrl(item.imageUrl),
        caption: item.caption || project.title,
      }))
      .filter((item): item is { url: string; caption: string } => Boolean(item.url));

    if (fromGallery.length > 0) return fromGallery;

    const cover = publicCoverUrl(project.coverImage, project.slug);
    if (cover) return [{ url: cover, caption: project.title }];
    return [] as { url: string; caption: string }[];
  }, [project]);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        if (lightbox) setLightbox(null);
        else onClose();
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    document.body.style.overflow = "hidden";

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [onClose, lightbox]);

  return (
    <div
      className="project-modal-overlay"
      role="presentation"
      onClick={onClose}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="portfolio-case-title"
        className="project-modal-panel"
        onClick={(event) => event.stopPropagation()}
      >
        <button
          type="button"
          onClick={onClose}
          className="project-modal-close"
          aria-label="Закрити"
        >
          ×
        </button>

        <div className="project-modal-body mx-auto max-w-4xl px-5 sm:px-8">
          <header className="mb-8">
            <p className="label-mono text-accent-bright">
              кейс · {project.category}
            </p>
            <h3
              id="portfolio-case-title"
              className="editorial-heading mt-3 text-3xl sm:text-4xl"
            >
              {project.title}
            </h3>
            <p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted sm:text-base">
              {project.caseDescription || project.description}
            </p>
          </header>

          <div className="relative mb-8 aspect-[16/10] overflow-hidden border border-[var(--card-border)]">
            <BrowserMockup project={project} />
          </div>

          <div className="grid gap-10 border-t border-[var(--card-border)] pt-10 lg:grid-cols-[minmax(0,1.4fr)_minmax(240px,0.7fr)] lg:gap-14">
            <div>
              {project.hasCaseStudy ? (
                <div className="mb-8 grid grid-cols-3 items-center gap-4">
                  <div>
                    <p className="label-mono mb-1">{content.sections.cases.before}</p>
                    <p className="text-sm text-muted">{project.before}</p>
                  </div>
                  <p className="text-center font-[family-name:var(--font-exo2)] text-3xl font-bold accent-warm-text">
                    {project.metric}
                  </p>
                  <div className="text-right">
                    <p className="label-mono mb-1">{content.sections.cases.after}</p>
                    <p className="text-sm font-medium accent-text">{project.after}</p>
                  </div>
                </div>
              ) : null}

              <div className="flex flex-wrap gap-2">
                {project.tags.map((tag) => (
                  <span
                    key={tag}
                    className="border border-[var(--card-border)] px-2.5 py-0.5 text-[11px] text-muted"
                  >
                    {tag}
                  </span>
                ))}
              </div>

              {photos.length > 0 ? (
                <div className="mt-10">
                  <p className="label-mono mb-4">Екрани сайту</p>
                  <div className="grid gap-4">
                    {photos.map((photo) => (
                      <button
                        key={`${photo.url}-${photo.caption}`}
                        type="button"
                        className="relative aspect-[16/10] overflow-hidden border border-[var(--card-border)] bg-[#0a0b0c] text-left"
                        onClick={() => setLightbox(photo.url)}
                        aria-label={photo.caption || "Відкрити фото"}
                      >
                        <Image
                          src={photo.url}
                          alt={photo.caption}
                          fill
                          className="object-cover object-top"
                          sizes="(max-width: 900px) 100vw, 640px"
                        />
                      </button>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>

            <aside className="border border-[var(--card-border)] bg-[var(--card)] p-6 lg:sticky lg:top-6 lg:self-start">
              <p className="label-mono text-accent-bright">{project.category}</p>
              <p className="editorial-heading mt-3 text-xl">{project.title}</p>
              <div className="mt-8 flex flex-col gap-3">
                {isPublicClientUrl(project.clientUrl) ? (
                  <a
                    href={project.clientUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-secondary py-2.5 text-center"
                  >
                    Відкрити сайт
                  </a>
                ) : null}
                <Link
                  href="/#contact"
                  onClick={onClose}
                  className="btn-primary py-2.5 text-center"
                >
                  {content.sections.portfolio.viewAll}
                </Link>
              </div>
            </aside>
          </div>
        </div>
      </div>

      {lightbox ? (
        <div
          role="presentation"
          className="project-modal-lightbox"
          onClick={() => setLightbox(null)}
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={lightbox} alt="" className="project-modal-lightbox-img" />
        </div>
      ) : null}
    </div>
  );
}

type PortfolioSectionClientProps = {
  projects: PortfolioProjectListItem[];
};

export function PortfolioSectionClient({
  projects,
}: PortfolioSectionClientProps) {
  const content = useSiteContent();
  const ordered = useMemo(() => sortProjects(projects).slice(0, 4), [projects]);

  return (
    <>
      <section id="portfolio" className="overflow-hidden py-16 sm:py-20 lg:py-24">
        <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
          <div className="mb-6 flex items-end justify-between gap-6 border-b border-[var(--card-border)] pb-4 sm:mb-7">
            <div className="max-w-xl">
              <p className="section-number mb-3">02</p>
              <h2 className="editorial-heading text-3xl sm:text-4xl">
                {content.sections.portfolio.title}
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-muted">
                {content.sections.portfolio.subtitle}
              </p>
            </div>
            <Link
              href="/works"
              className="hidden shrink-0 border-b border-muted/40 pb-1 font-[family-name:var(--font-jetbrains)] text-xs tracking-[0.12em] text-muted transition-colors hover:border-accent hover:text-accent-bright sm:inline-flex"
            >
              Усі роботи
            </Link>
          </div>

          <div className="proj-home-grid">
            {ordered.map((project, index) => (
              <ProjectTile key={project.slug} project={project} index={index} />
            ))}
          </div>

          <div className="mt-6 sm:hidden">
            <Link href="/works" className="btn-secondary w-full text-center">
              Усі роботи
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
