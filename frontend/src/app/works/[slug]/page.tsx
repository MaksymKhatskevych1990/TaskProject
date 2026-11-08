import type { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Breadcrumbs } from "@/components/layout/Breadcrumbs";
import { MarketingChrome } from "@/components/layout/MarketingChrome";
import { BrowserMockup } from "@/components/portfolio/BrowserMockup";
import { publicCoverUrl, staticGallery } from "@/lib/portfolio-covers";
import { JsonLd } from "@/components/seo/JsonLd";
import { getPortfolioProject, getPortfolioProjects } from "@/lib/portfolio-api";
import { createPageMetadata } from "@/lib/seo/metadata";
import {
  buildBreadcrumbNode,
  buildCreativeWorkNode,
  buildSchemaGraph,
  buildWebPageNode,
} from "@/lib/seo/schema";
import { getSiteContent } from "@/lib/site-content";

export const dynamic = "force-dynamic";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const project = await getPortfolioProject(slug);
  if (!project) return { title: "Кейс не знайдено" };
  return createPageMetadata({
    title: `${project.title} — кейс розробки сайту`,
    description: project.description,
    path: `/works/${project.slug}`,
  });
}

export default async function WorkCasePage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const [project, content, projects] = await PromiseAllSafe(slug);
  if (!project) notFound();

  const shots =
    staticGallery(project.slug).length > 0
      ? staticGallery(project.slug)
      : project.gallery
          .map((item) => ({
            url: publicCoverUrl(item.imageUrl),
            caption: item.caption || project.title,
          }))
          .filter((item): item is { url: string; caption: string } => Boolean(item.url));

  const schema = buildSchemaGraph([
    buildWebPageNode({
      path: `/works/${project.slug}`,
      name: project.title,
      description: project.description,
    }),
    buildCreativeWorkNode(project),
    buildBreadcrumbNode([
      { name: "Головна", path: "/" },
      { name: "Роботи", path: "/works" },
      { name: project.title, path: `/works/${project.slug}` },
    ]),
  ]);

  const others = projects.filter((item) => item.slug !== project.slug).slice(0, 3);

  return (
    <MarketingChrome>
      <JsonLd data={schema} />
      <main className="pt-28 pb-20">
        <article className="mx-auto max-w-4xl px-5 sm:px-8">
          <Breadcrumbs
            items={[
              { href: "/", label: "Головна" },
              { href: "/works", label: "Роботи" },
              { href: `/works/${project.slug}`, label: project.title },
            ]}
          />
          <p className="label-mono mt-10 text-accent-bright">кейс · {project.category}</p>
          <h1 className="editorial-heading mt-3 text-4xl sm:text-5xl">{project.title}</h1>
          <p className="mt-4 max-w-2xl text-base leading-relaxed text-muted">
            {project.caseDescription || project.description}
          </p>

          <div className="relative mt-10 aspect-[16/10] overflow-hidden border border-[var(--card-border)]">
            <BrowserMockup project={project} />
          </div>

          {project.hasCaseStudy ? (
            <div className="mt-10 grid grid-cols-3 items-center gap-4 border-t border-[var(--card-border)] pt-8">
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

          <div className="mt-8 flex flex-wrap gap-2">
            {project.tags.map((tag) => (
              <span
                key={tag}
                className="border border-[var(--card-border)] px-2.5 py-0.5 text-[11px] text-muted"
              >
                {tag}
              </span>
            ))}
          </div>

          {shots.length > 0 ? (
            <div className="mt-12 space-y-8">
              <p className="label-mono">Екрани сайту</p>
              {shots.map((photo) => (
                <figure key={`${photo.url}-${photo.caption}`} className="space-y-3">
                  <div className="relative aspect-[16/10] overflow-hidden border border-[var(--card-border)] bg-[#0a0b0c]">
                    <Image
                      src={photo.url}
                      alt={photo.caption}
                      fill
                      className="object-cover object-top"
                      sizes="(max-width: 900px) 100vw, 860px"
                    />
                  </div>
                  <figcaption className="text-sm text-muted">{photo.caption}</figcaption>
                </figure>
              ))}
            </div>
          ) : null}

          <div className="mt-12 flex flex-wrap gap-3">
            {isPublicClientUrl(project.clientUrl) ? (
              <a
                href={project.clientUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="btn-secondary px-5 py-3"
              >
                Відкрити живий сайт
              </a>
            ) : null}
            <Link href="/#contact" className="btn-primary px-5 py-3">
              {content.sections.portfolio.viewAll}
            </Link>
          </div>

          {others.length > 0 ? (
            <section className="mt-20 border-t border-[var(--card-border)] pt-10">
              <h2 className="editorial-heading text-2xl">Інші роботи</h2>
              <ul className="mt-6 space-y-3">
                {others.map((item) => (
                  <li key={item.slug}>
                    <Link
                      href={`/works/${item.slug}`}
                      className="text-sm text-muted transition-colors hover:text-accent-bright"
                    >
                      {item.title}
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
        </article>
      </main>
    </MarketingChrome>
  );
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

async function PromiseAllSafe(slug: string) {
  const [project, content, projects] = await Promise.all([
    getPortfolioProject(slug),
    getSiteContent(),
    getPortfolioProjects(),
  ]);
  return [project, content, projects] as const;
}
