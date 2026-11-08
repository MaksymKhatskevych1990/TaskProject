import type { Metadata } from "next";
import Link from "next/link";
import { MarketingChrome } from "@/components/layout/MarketingChrome";
import { Breadcrumbs } from "@/components/layout/Breadcrumbs";
import { JsonLd } from "@/components/seo/JsonLd";
import {
  SERVICE_CLUSTERS,
  SERVICE_HUB,
  getServicePage,
} from "@/lib/marketing-pages";
import { createPageMetadata } from "@/lib/seo/metadata";
import { buildBreadcrumbNode, buildSchemaGraph, buildWebPageNode } from "@/lib/seo/schema";
import { formatSitePrice, getSiteContent } from "@/lib/site-content";

export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  return createPageMetadata({
    title: SERVICE_HUB.seoTitle,
    description: SERVICE_HUB.seoDescription,
    path: "/poslugy",
    absoluteTitle: true,
  });
}

export default async function ServicesHubPage() {
  const content = await getSiteContent();
  const schema = buildSchemaGraph([
    buildWebPageNode({
      path: "/poslugy",
      name: SERVICE_HUB.h1,
      description: SERVICE_HUB.seoDescription,
    }),
    buildBreadcrumbNode([
      { name: "Головна", path: "/" },
      { name: "Послуги", path: "/poslugy" },
    ]),
  ]);

  return (
    <MarketingChrome>
      <JsonLd data={schema} />
      <main className="pt-28 pb-20">
        <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
          <Breadcrumbs
            items={[
              { href: "/", label: "Головна" },
              { href: "/poslugy", label: "Послуги" },
            ]}
          />
          <h1 className="editorial-heading mt-10 max-w-3xl text-4xl sm:text-5xl">
            {SERVICE_HUB.h1}
          </h1>
          <p className="mt-5 max-w-xl text-sm leading-relaxed text-muted">
            {SERVICE_HUB.subtitle}
          </p>

          <div className="mt-16 space-y-16">
            {SERVICE_CLUSTERS.map((cluster) => (
              <section key={cluster.title}>
                <h2 className="editorial-heading text-2xl sm:text-3xl">{cluster.title}</h2>
                <div className="mt-8 grid gap-px bg-[var(--card-border)] md:grid-cols-2 xl:grid-cols-3">
                  {cluster.slugs.map((slug) => {
                    const page = getServicePage(slug);
                    if (!page) return null;
                    const plan = page.relatedPlan
                      ? content.pricing.find((item) => item.slug === page.relatedPlan)
                      : undefined;
                    return (
                      <article key={page.slug} className="flex flex-col bg-background p-8 sm:p-10">
                        <h3 className="editorial-heading text-2xl">
                          <Link href={page.href} className="hover:text-accent-bright">
                            {page.title}
                          </Link>
                        </h3>
                        <p className="mt-3 flex-1 text-sm leading-relaxed text-muted">
                          {page.intro}
                        </p>
                        {plan ? (
                          <p className="mt-6 text-sm">від {formatSitePrice(plan.price, content)}</p>
                        ) : page.priceHint ? (
                          <p className="mt-6 text-sm text-muted">{page.priceHint}</p>
                        ) : null}
                        <Link href={page.href} className="btn-secondary mt-8 w-full text-center">
                          Деталі послуги
                        </Link>
                      </article>
                    );
                  })}
                </div>
              </section>
            ))}
          </div>
        </div>
      </main>
    </MarketingChrome>
  );
}
