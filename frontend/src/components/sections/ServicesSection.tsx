import { SERVICES } from "@/lib/site-data";
import { cn } from "@/lib/utils";

const glowClasses = {
  cyan: "hover:border-cyan/40 hover:shadow-cyan/10",
  violet: "hover:border-violet/40 hover:shadow-violet/10",
  green: "hover:border-emerald-400/40 hover:shadow-emerald-400/10",
  orange: "hover:border-orange-400/40 hover:shadow-orange-400/10",
} as const;

export function ServicesSection() {
  return (
    <section id="services" className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 text-center">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            Услуги
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            Что мы делаем
          </h2>
        </div>

        <div className="grid gap-6 sm:grid-cols-2">
          {SERVICES.map((service) => (
            <article
              key={service.title}
              className={cn(
                "group rounded-2xl border border-white/5 bg-card p-6 transition-all duration-300 hover:shadow-lg",
                glowClasses[service.glow as keyof typeof glowClasses],
              )}
            >
              <span className="text-3xl">{service.icon}</span>
              <h3 className="mt-4 font-[family-name:var(--font-exo2)] text-xl font-semibold">
                {service.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">
                {service.description}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
