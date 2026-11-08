"use client";

import { useState } from "react";
import type { PortfolioProjectListItem } from "@/lib/portfolio-api";
import { publicCoverUrl } from "@/lib/portfolio-covers";

export { publicCoverUrl, staticGallery } from "@/lib/portfolio-covers";

/** Full-bleed agency mockup — chrome is baked into the cover art. */
export function BrowserMockup({
  project,
}: {
  project: Pick<
    PortfolioProjectListItem,
    "slug" | "title" | "accent" | "gradient" | "coverImage"
  >;
  sizes?: string;
}) {
  const cover = publicCoverUrl(project.coverImage, project.slug);
  const [broken, setBroken] = useState(false);
  const showImage = Boolean(cover && !broken);

  return (
    <div className="relative h-full min-h-[160px] w-full overflow-hidden bg-[#0a0b0c]">
      {showImage ? (
        // eslint-disable-next-line @next/next/no-img-element
        <img
          src={cover as string}
          alt={project.title}
          className="proj-img absolute inset-0 h-full w-full object-cover object-center"
          onError={() => setBroken(true)}
        />
      ) : (
        <div
          className={`absolute inset-0 bg-gradient-to-br ${project.gradient}`}
        />
      )}
      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-black/35 to-transparent" />
    </div>
  );
}
