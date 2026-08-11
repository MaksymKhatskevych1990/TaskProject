import { GUARANTEES, SECTIONS } from "@/lib/site-data";
import { cn } from "@/lib/utils";

export function GuaranteesSection() {
  return (
    <section className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 section-intro">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            {SECTIONS.guarantees.eyebrow}
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            {SECTIONS.guarantees.title}
          </h2>
        </div>

        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
          {GUARANTEES.map((item, index) => (
            <article
              key={item.title}
              className={cn(
                "border border-white/5 bg-card p-6 text-left",
                index % 2 === 0 ? "surface-card" : "surface-card-alt",
              )}
            >
              <span aria-hidden="true" className="text-3xl">
                {item.icon}
              </span>
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
