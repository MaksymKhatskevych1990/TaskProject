import { GUARANTEES } from "@/lib/site-data";

export function GuaranteesSection() {
  return (
    <section className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 text-center">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            Гарантии
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            Работаем без рисков
          </h2>
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
          {GUARANTEES.map((item) => (
            <article
              key={item.title}
              className="rounded-2xl border border-white/5 bg-card p-6 text-center"
            >
              <span className="text-3xl">{item.icon}</span>
              <h3 className="mt-4 font-[family-name:var(--font-exo2)] text-base font-semibold">
                {item.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">
                {item.description}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
