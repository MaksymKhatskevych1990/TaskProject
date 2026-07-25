import { CASES } from "@/lib/site-data";

export function CaseStudiesSection() {
  return (
    <section id="cases" className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 text-center">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            Кейсы
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            Результаты клиентов
          </h2>
        </div>

        <div className="grid gap-6 md:grid-cols-3">
          {CASES.map((item) => (
            <article
              key={item.title}
              className="rounded-2xl border border-white/5 bg-card p-6"
            >
              <span className="text-3xl">{item.emoji}</span>
              <h3 className="mt-4 font-[family-name:var(--font-exo2)] text-lg font-semibold">
                {item.title}
              </h3>
              <p className="mt-2 text-sm text-muted">{item.description}</p>

              <div className="mt-6 flex items-center justify-between rounded-xl bg-white/5 px-4 py-3">
                <div>
                  <p className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase text-muted">
                    Было
                  </p>
                  <p className="text-sm">{item.before}</p>
                </div>
                <span className="gradient-text font-[family-name:var(--font-exo2)] text-xl font-bold">
                  {item.metric}
                </span>
                <div className="text-right">
                  <p className="font-[family-name:var(--font-jetbrains)] text-[10px] uppercase text-muted">
                    Стало
                  </p>
                  <p className="text-sm font-medium text-cyan">{item.after}</p>
                </div>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
