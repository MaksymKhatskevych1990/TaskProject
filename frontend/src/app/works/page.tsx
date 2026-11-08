import type { Metadata } from "next";
import { MarketingChrome } from "@/components/layout/MarketingChrome";
import { JsonLd } from "@/components/seo/JsonLd";
import { WorksCatalog } from "@/app/works/WorksCatalog";
import { getPortfolioProjects } from "@/lib/portfolio-api";
import { createPageMetadata } from "@/lib/seo/metadata";
import {
  buildPortfolioListNode,
  buildSchemaGraph,
  buildWebPageNode,
} from "@/lib/seo/schema";
import { getSiteContent } from "@/lib/site-content";

export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  const content = await getSiteContent();
  return createPageMetadata({
    title: `Портфоліо сайтів і магазинів — ${content.brand}`,
    description:
      "Живі кейси: інтернет-магазини, корпоративні сайти та лендинги. Артмагія, LuxMeb, RudWood, Elvet Group, AS clean.",
    path: "/works",
  });
}

export default async function WorksPage() {
  const [projects, content] = await Promise.all([
    getPortfolioProjects(),
    getSiteContent(),
  ]);
  const schema = buildSchemaGraph([
    buildWebPageNode({
      path: "/works",
      name: content.sections.portfolio.title,
      description: content.sections.portfolio.subtitle,
    }),
    buildPortfolioListNode(projects),
  ]);

  return (
    <MarketingChrome>
      <JsonLd data={schema} />
      <main className="pt-28 pb-20">
        <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
          <div className="mb-12 max-w-lg border-b border-[var(--card-border)] pb-8">
            <p className="label-mono mb-4">{content.sections.portfolio.eyebrow}</p>
            <h1 className="editorial-heading text-3xl sm:text-4xl lg:text-5xl">
              {content.sections.portfolio.title}
            </h1>
            <p className="mt-4 text-sm leading-relaxed text-muted">
              {content.sections.portfolio.subtitle}
            </p>
          </div>

          {projects.length === 0 ? (
            <p className="text-sm text-muted">Роботи зʼявляться незабаром.</p>
          ) : (
            <WorksCatalog projects={projects} />
          )}
        </div>
      </main>
    </MarketingChrome>
  );
}
