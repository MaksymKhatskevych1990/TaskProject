import { formatSitePrice, getSiteContent } from "@/lib/site-content";
import { cn } from "@/lib/utils";

export async function PricingSection() {
  const content = await getSiteContent();

  return (
    <section id="pricing" className="border-t border-[var(--card-border)] py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="mb-16 max-w-lg">
          <p className="section-number mb-4">05</p>
          <h2 className="editorial-heading text-3xl sm:text-4xl">
            {content.sections.pricing.title}
          </h2>
          <p className="mt-4 text-sm text-muted">{content.sections.pricing.subtitle}</p>
        </div>

        <div className="grid gap-px bg-[var(--card-border)] lg:grid-cols-3">
          {content.pricing.map((plan) => (
            <article
              key={plan.slug}
              className={cn(
                "flex flex-col bg-background p-8 sm:p-10",
                plan.highlighted && "lg:-mt-4 lg:-mb-4 lg:bg-[var(--card)] lg:py-12",
              )}
            >
              {plan.badge ? (
                <span className="label-mono mb-6 text-accent-warm-bright">
                  {plan.badge}
                </span>
              ) : null}

              <h3 className="editorial-heading text-2xl">{plan.name}</h3>
              <p className="mt-2 text-sm text-muted">{plan.description}</p>

              <div className="mt-8">
                <span className="text-xs text-muted">{content.sections.pricing.from} </span>
                <p className="font-[family-name:var(--font-exo2)] text-3xl font-bold tracking-tight">
                  {formatSitePrice(plan.price, content)}
                </p>
              </div>

              <ul className="mt-8 flex-1 space-y-3 border-t border-[var(--card-border)] pt-8">
                {plan.features.map((feature) => (
                  <li
                    key={feature}
                    className="flex items-start gap-3 text-sm text-muted"
                  >
                    <span className="mt-2 h-1 w-1 shrink-0 rounded-full bg-accent" />
                    {feature}
                  </li>
                ))}
              </ul>

              <a
                href={`?plan=${plan.slug}#contact`}
                className={cn(
                  "mt-10 block py-3 text-center text-sm font-semibold transition-colors",
                  plan.highlighted
                    ? "btn-primary w-full"
                    : "btn-secondary w-full",
                )}
              >
                {content.sections.pricing.choosePlan}
              </a>
            </article>
          ))}
        </div>
        <p className="mt-8 max-w-2xl text-sm leading-relaxed text-muted">
          50% на старті, 50% після здачі. У ціну входять дизайн, розробка, базове SEO і підтримка.
          Хостинг, домен і комісії оплати — окремо, без сюрпризів у рахунку.
        </p>
      </div>
    </section>
  );
}
