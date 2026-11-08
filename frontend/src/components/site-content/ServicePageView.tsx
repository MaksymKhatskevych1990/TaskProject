import Link from "next/link";
import { MarketingChrome } from "@/components/layout/MarketingChrome";
import { Breadcrumbs } from "@/components/layout/Breadcrumbs";
import { JsonLd } from "@/components/seo/JsonLd";
import {
  SERVICE_PAGES,
  serviceCtaHref,
  servicePagesBySlugs,
  type ServicePage,
} from "@/lib/marketing-pages";
import { getPortfolioProjects } from "@/lib/portfolio-api";
import { buildBreadcrumbNode, buildSchemaGraph, buildWebPageNode } from "@/lib/seo/schema";
import { formatSitePrice, getSiteContent } from "@/lib/site-content";
import { absoluteUrl } from "@/lib/seo/site-url";

export async function ServicePageView({ page }: { page: ServicePage }) {
  const [content, projects] = await Promise.all([getSiteContent(), getPortfolioProjects()]);
  const plan = page.relatedPlan
    ? content.pricing.find((item) => item.slug === page.relatedPlan)
    : undefined;
  const relatedServices = page.relatedServiceSlugs
    ? servicePagesBySlugs(page.relatedServiceSlugs)
    : SERVICE_PAGES.filter((item) => item.slug !== page.slug).slice(0, 4);
  const relatedWorks = (page.relatedWorks ?? [])
    .map((slug) => projects.find((item) => item.slug === slug))
    .filter((item): item is NonNullable<typeof item> => Boolean(item));
  const schema = buildSchemaGraph([
    buildWebPageNode({
      path: page.href,
      name: page.h1,
      description: page.seoDescription,
    }),
    buildBreadcrumbNode([
      { name: "Головна", path: "/" },
      { name: "Послуги", path: "/poslugy" },
      { name: page.title, path: page.href },
    ]),
    {
      "@type": "FAQPage",
      mainEntity: page.faqs.map((item) => ({
        "@type": "Question",
        name: item.question,
        acceptedAnswer: { "@type": "Answer", text: item.answer },
      })),
    },
    {
      "@type": "Service",
      name: page.title,
      description: page.seoDescription,
      url: absoluteUrl(page.href),
      areaServed: "UA",
      provider: { "@type": "Organization", name: content.brand },
    },
  ]);

  return (
    <MarketingChrome>
      <JsonLd data={schema} />
      <main className="pt-28 pb-20">
        <article className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
          <Breadcrumbs
            items={[
              { href: "/", label: "Головна" },
              { href: "/poslugy", label: "Послуги" },
              { href: page.href, label: page.title },
            ]}
          />
          <p className="label-mono mt-10 mb-4">{page.eyebrow}</p>
          <h1 className="editorial-heading max-w-3xl text-4xl sm:text-5xl">{page.h1}</h1>
          <p className="mt-6 max-w-2xl text-base leading-relaxed text-muted">{page.intro}</p>
          <p className="mt-4 max-w-2xl text-sm leading-relaxed text-foreground">{page.outcome}</p>

          {plan ? (
            <p className="mt-6 font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-[0.14em] text-muted">
              від {formatSitePrice(plan.price, content)} · тариф «{plan.name}»
            </p>
          ) : page.priceHint ? (
            <p className="mt-6 font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-[0.14em] text-muted">
              {page.priceHint}
            </p>
          ) : null}

          <div className="mt-8 flex flex-wrap gap-3">
            <Link href={serviceCtaHref(page)} className="btn-primary px-7 py-3.5">
              {page.cta}
            </Link>
            <Link href="/works" className="btn-secondary px-5 py-3.5">
              Дивитись живі сайти
            </Link>
          </div>

          <div className="mt-20 grid gap-16 lg:grid-cols-2">
            <section>
              <h2 className="editorial-heading text-2xl">Що входить</h2>
              <ul className="mt-6 space-y-3">
                {page.includes.map((item) => (
                  <li key={item} className="flex items-start gap-3 text-sm text-muted">
                    <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-accent" />
                    {item}
                  </li>
                ))}
              </ul>
            </section>
            <section>
              <h2 className="editorial-heading text-2xl">Як проходить робота</h2>
              <ol className="mt-6 space-y-4">
                {page.process.map((item, index) => (
                  <li key={item} className="grid grid-cols-[2rem_1fr] gap-3 text-sm text-muted">
                    <span className="font-[family-name:var(--font-jetbrains)] text-accent">
                      {String(index + 1).padStart(2, "0")}
                    </span>
                    {item}
                  </li>
                ))}
              </ol>
            </section>
          </div>

          {relatedWorks.length > 0 ? (
            <section className="mt-20">
              <h2 className="editorial-heading text-2xl">Приклади з портфоліо</h2>
              <ul className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {relatedWorks.map((project) => (
                  <li key={project.slug}>
                    <Link
                      href={`/works/${project.slug}`}
                      className="block border border-[var(--card-border)] p-5 transition-colors hover:border-accent/40"
                    >
                      <p className="label-mono text-muted">{project.category}</p>
                      <p className="mt-2 editorial-heading text-xl">{project.title}</p>
                      <p className="mt-2 line-clamp-2 text-sm text-muted">{project.description}</p>
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}

          <section className="mt-20 max-w-3xl">
            <h2 className="editorial-heading text-2xl">Питання перед замовленням</h2>
            <div className="mt-8">
              {page.faqs.map((item) => (
                <div key={item.question} className="border-t border-[var(--card-border)] py-6">
                  <h3 className="text-base font-medium">{item.question}</h3>
                  <p className="mt-3 text-sm leading-relaxed text-muted">{item.answer}</p>
                </div>
              ))}
            </div>
          </section>

          <p className="mt-16 text-sm text-muted">
            Також:{" "}
            {relatedServices.map((item, index, list) => (
              <span key={item.slug}>
                <Link href={item.href} className="text-foreground hover:text-accent-bright">
                  {item.title}
                </Link>
                {index < list.length - 1 ? " · " : ""}
              </span>
            ))}
            {" · "}
            <Link href="/poslugy" className="text-foreground hover:text-accent-bright">
              усі послуги
            </Link>
          </p>
        </article>
      </main>
    </MarketingChrome>
  );
}
