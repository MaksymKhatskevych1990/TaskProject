import { CASES, SECTIONS } from "@/lib/site-data";

export function CaseStudiesSection() {
  return (
    <section id="cases" className="bg-[var(--card)] py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="mb-16 flex items-end justify-between gap-8">
          <div>
            <p className="section-number mb-4">03</p>
            <h2 className="editorial-heading text-3xl sm:text-4xl">
              {SECTIONS.cases.title}
            </h2>
          </div>
        </div>

        <div className="space-y-0">
          {CASES.map((item, index) => (
            <article
              key={item.title}
              className="grid gap-6 border-t border-[var(--card-border)] py-12 sm:grid-cols-[1fr_auto_1fr] sm:items-center sm:gap-12"
            >
              <div className={index % 2 === 1 ? "sm:order-3 sm:text-right" : ""}>
                <p className="label-mono mb-2">{SECTIONS.cases.before}</p>
                <p className="text-lg text-muted line-through decoration-[var(--card-border)]">
                  {item.before}
                </p>
              </div>

              <div className="text-center sm:order-2">
                <p className="font-[family-name:var(--font-exo2)] text-4xl font-bold tracking-tight accent-warm-text sm:text-5xl">
                  {item.metric}
                </p>
                <p className="mt-2 text-xs text-muted">{item.title}</p>
              </div>

              <div className={index % 2 === 1 ? "sm:order-1" : "sm:text-right"}>
                <p className="label-mono mb-2">{SECTIONS.cases.after}</p>
                <p className="text-lg font-medium accent-text">{item.after}</p>
                <p className="mt-2 text-sm text-muted">{item.description}</p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
