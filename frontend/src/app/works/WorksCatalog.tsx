"use client";

import Link from "next/link";
import { useMemo } from "react";
import { BrowserMockup } from "@/components/portfolio/BrowserMockup";
import type { PortfolioProjectListItem } from "@/lib/portfolio-api";

function pad(n: number) {
  return String(n).padStart(2, "0");
}

export function WorksCatalog({
  projects,
}: {
  projects: PortfolioProjectListItem[];
}) {
  const ordered = useMemo(
    () =>
      [...projects].sort((a, b) => {
        if (a.featured !== b.featured) return a.featured ? -1 : 1;
        return 0;
      }),
    [projects],
  );

  return (
    <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {ordered.map((project, index) => (
        <Link
          key={project.slug}
          href={`/works/${project.slug}`}
          className="proj-card group flex cursor-pointer flex-col overflow-hidden border border-[var(--card-border)] bg-[var(--card)] text-left transition-[border-color,transform] duration-400 hover:-translate-y-0.5 hover:border-accent/35"
        >
          <div className="relative aspect-[16/10] overflow-hidden">
            <BrowserMockup project={project} />
          </div>

          <div className="flex flex-col gap-2 border-t border-[var(--card-border)] px-4 py-4">
            <div className="flex items-start justify-between gap-3">
              <span className="label-mono text-muted">
                {pad(index + 1)} · {project.category}
              </span>
              {project.hasCaseStudy ? (
                <span className="shrink-0 font-[family-name:var(--font-exo2)] text-lg font-bold tracking-tight accent-warm-text">
                  {project.metric}
                </span>
              ) : null}
            </div>
            <h2 className="editorial-heading text-xl text-foreground transition-colors group-hover:text-accent-bright">
              {project.title}
            </h2>
            <p className="line-clamp-2 text-sm text-muted">{project.description}</p>
          </div>
        </Link>
      ))}
    </div>
  );
}
