import { SECTIONS, SERVICES } from "@/lib/site-data";

const featuredServices = SERVICES.filter((service) => service.featured);
const additionalServices = SERVICES.filter((service) => !service.featured);

export function ServicesSection() {
  return (
    <section id="services" className="py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="grid gap-12 lg:grid-cols-[280px_1fr] lg:gap-20">
          <div className="lg:sticky lg:top-28 lg:self-start">
            <p className="section-number mb-4">01</p>
            <h2 className="editorial-heading text-3xl sm:text-4xl">
              {SECTIONS.services.title}
            </h2>
            <p className="mt-4 text-sm leading-relaxed text-muted">
              {SECTIONS.services.subtitle}
            </p>
          </div>

          <div className="space-y-0">
            {featuredServices.map((service, index) => (
              <article
                key={service.title}
                className="group border-t border-[var(--card-border)] py-10 first:border-t-0 first:pt-0"
              >
                <div className="grid gap-6 sm:grid-cols-[auto_1fr] sm:gap-10">
                  <span className="section-number pt-1">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <div>
                    <h3 className="editorial-heading text-xl sm:text-2xl">
                      {service.title}
                    </h3>
                    <p className="mt-3 max-w-lg text-sm leading-relaxed text-muted">
                      {service.description}
                    </p>
                    {"features" in service && service.features && (
                      <ul className="mt-6 grid gap-2 sm:grid-cols-2">
                        {service.features.map((feature) => (
                          <li
                            key={feature}
                            className="flex items-start gap-2 text-sm text-muted"
                          >
                            <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-accent" />
                            {feature}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>
              </article>
            ))}

            {additionalServices.length > 0 && (
              <div className="border-t border-[var(--card-border)] pt-10">
                <p className="label-mono mb-8">{SECTIONS.services.also}</p>
                <div className="grid gap-8 sm:grid-cols-2">
                  {additionalServices.map((service) => (
                    <article key={service.title}>
                      <h3 className="text-base font-semibold">{service.title}</h3>
                      <p className="mt-2 text-sm leading-relaxed text-muted">
                        {service.description}
                      </p>
                    </article>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
