import { SECTIONS, SERVICES } from "@/lib/site-data";
import { cn } from "@/lib/utils";

const glowClasses = {
  cyan: "hover:border-cyan/40 hover:shadow-cyan/10",
  violet: "hover:border-violet/40 hover:shadow-violet/10",
  green: "hover:border-emerald-400/40 hover:shadow-emerald-400/10",
  orange: "hover:border-orange-400/40 hover:shadow-orange-400/10",
} as const;

const featuredServices = SERVICES.filter((service) => service.featured);
const additionalServices = SERVICES.filter((service) => !service.featured);

export function ServicesSection() {
  return (
    <section id="services" className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 text-center">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            {SECTIONS.services.eyebrow}
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            {SECTIONS.services.title}
          </h2>
          <p className="mx-auto mt-3 max-w-2xl text-sm leading-relaxed text-muted">
            {SECTIONS.services.subtitle}
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {featuredServices.map((service) => (
            <article
              key={service.title}
              className={cn(
                "group flex flex-col rounded-2xl border border-white/5 bg-card p-6 transition-all duration-300 hover:shadow-lg",
                glowClasses[service.glow as keyof typeof glowClasses],
              )}
            >
              <span aria-hidden="true" className="text-3xl">
                {service.icon}
              </span>
              <h3 className="mt-4 font-[family-name:var(--font-exo2)] text-xl font-semibold">
                {service.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">
                {service.description}
              </p>
              {"features" in service && service.features && (
                <ul className="mt-5 flex-1 space-y-2.5 border-t border-white/5 pt-5">
                  {service.features.map((feature) => (
                    <li
                      key={feature}
                      className="flex items-start gap-2 text-sm text-muted"
                    >
                      <span className="mt-0.5 text-cyan">✓</span>
                      {feature}
                    </li>
                  ))}
                </ul>
              )}
            </article>
          ))}
        </div>

        {additionalServices.length > 0 && (
          <div className="mt-14">
            <p className="mb-6 text-center font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-muted">
              {SECTIONS.services.also}
            </p>
            <div className="mx-auto grid max-w-3xl gap-6 sm:grid-cols-2">
              {additionalServices.map((service) => (
                <article
                  key={service.title}
                  className={cn(
                    "group rounded-2xl border border-white/5 bg-card p-6 transition-all duration-300 hover:shadow-lg",
                    glowClasses[service.glow as keyof typeof glowClasses],
                  )}
                >
                  <span aria-hidden="true" className="text-3xl">
                    {service.icon}
                  </span>
                  <h3 className="mt-4 font-[family-name:var(--font-exo2)] text-lg font-semibold">
                    {service.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted">
                    {service.description}
                  </p>
                </article>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
