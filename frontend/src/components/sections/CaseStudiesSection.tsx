import Link from "next/link";
import { getPortfolioProjects } from "@/lib/portfolio-api";

export async function CaseStudiesSection() {
  const projects = (await getPortfolioProjects()).filter((item) => item.hasCaseStudy).slice(0, 4);

  if (projects.length === 0) return null;

  return (
    <section id="cases" className="bg-[var(--card)] py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="mb-12 max-w-lg sm:mb-16">
          <p className="section-number mb-4">03</p>
          <h2 className="editorial-heading text-3xl sm:text-4xl">Результати на живих сайтах</h2>
          <p className="mt-4 text-sm leading-relaxed text-muted">
            Не абстрактні «+640%», а проєкти, які можна відкрити. Було / стало — як клієнт продавав
            до запуску і як продає зараз.
          </p>
        </div>

        <div className="hidden border-b border-[var(--card-border)] pb-4 lg:grid lg:grid-cols-[minmax(0,1.4fr)_1fr_1fr_8.5rem] lg:gap-8">
          <p className="label-mono">Проєкт</p>
          <p className="label-mono">Було</p>
          <p className="label-mono">Стало</p>
          <p className="label-mono text-right">Ефект</p>
        </div>

        <div>
          {projects.map((item) => (
            <article
              key={item.slug}
              className="grid gap-6 border-b border-[var(--card-border)] py-8 last:border-b-0 sm:py-10 lg:grid-cols-[minmax(0,1.4fr)_1fr_1fr_8.5rem] lg:items-center lg:gap-8"
            >
              <div>
                <p className="label-mono mb-2">{item.category}</p>
                <h3 className="editorial-heading text-xl sm:text-2xl">
                  <Link href={`/works/${item.slug}`} className="hover:text-accent-bright">
                    {item.title}
                  </Link>
                </h3>
                <p className="mt-2 max-w-sm text-sm leading-relaxed text-muted">
                  {item.description}
                </p>
              </div>

              <div className="grid grid-cols-2 gap-4 lg:contents">
                <div>
                  <p className="label-mono mb-2 lg:hidden">Було</p>
                  <p className="text-lg text-muted line-through decoration-[var(--card-border)]">
                    {item.before}
                  </p>
                </div>
                <div>
                  <p className="label-mono mb-2 lg:hidden">Стало</p>
                  <p className="text-lg font-medium accent-text">{item.after}</p>
                </div>
              </div>

              <div className="lg:text-right">
                <p className="label-mono mb-2 lg:hidden">Ефект</p>
                <p className="font-[family-name:var(--font-exo2)] text-4xl font-bold tracking-tight accent-warm-text">
                  {item.metric}
                </p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
