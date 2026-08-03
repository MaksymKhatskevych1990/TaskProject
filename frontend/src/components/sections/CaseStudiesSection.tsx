import { CASES, SECTIONS } from "@/lib/site-data";

export function CaseStudiesSection() {
  return (
    <section id="cases" className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 text-center">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            {SECTIONS.cases.eyebrow}
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            {SECTIONS.cases.title}
          </h2>
        </div>

        <div className="grid gap-6 md:grid-cols-3 md:items-stretch">
          {CASES.map((item) => (
            <article
              key={item.title}
              className="flex h-full min-h-[22rem] flex-col rounded-2xl border border-white/5 bg-card p-6"
            >
              <span aria-hidden="true" className="block h-8 shrink-0 text-3xl leading-none">
                {item.emoji}
              </span>

              <h3 className="mt-4 line-clamp-2 h-14 shrink-0 font-[family-name:var(--font-exo2)] text-lg font-semibold leading-snug">
                {item.title}
              </h3>

              <p className="mt-2 line-clamp-3 h-[4.125rem] shrink-0 text-sm leading-relaxed text-muted">
                {item.description}
              </p>

              <div className="mt-auto shrink-0 pt-6">
                <div className="grid h-[4.25rem] grid-cols-3 items-center gap-2 rounded-xl bg-white/5 px-3">
                  <div className="min-w-0">
                    <p className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase text-muted">
                      {SECTIONS.cases.before}
                    </p>
                    <p className="mt-1 truncate text-sm leading-tight">{item.before}</p>
                  </div>

                  <p className="gradient-text text-center font-[family-name:var(--font-exo2)] text-xl font-bold leading-none">
                    {item.metric}
                  </p>

                  <div className="min-w-0 text-right">
                    <p className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase text-muted">
                      {SECTIONS.cases.after}
                    </p>
                    <p className="mt-1 truncate text-sm font-medium leading-tight text-cyan">
                      {item.after}
                    </p>
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
