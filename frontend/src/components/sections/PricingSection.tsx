import { formatPrice, PRICING_PLANS, SECTIONS } from "@/lib/site-data";
import { cn } from "@/lib/utils";

export function PricingSection() {
  return (
    <section id="pricing" className="border-t border-[var(--card-border)] py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="mb-16 max-w-lg">
          <p className="section-number mb-4">05</p>
          <h2 className="editorial-heading text-3xl sm:text-4xl">
            {SECTIONS.pricing.title}
          </h2>
          <p className="mt-4 text-sm text-muted">{SECTIONS.pricing.subtitle}</p>
        </div>

        <div className="grid gap-px bg-[var(--card-border)] lg:grid-cols-3">
          {PRICING_PLANS.map((plan) => (
            <article
              key={plan.name}
              className={cn(
                "flex flex-col bg-background p-8 sm:p-10",
                plan.highlighted && "lg:-mt-4 lg:-mb-4 lg:bg-[var(--card)] lg:py-12",
              )}
            >
              {"badge" in plan && plan.badge && (
                <span className="label-mono mb-6 text-accent-warm-bright">
                  {plan.badge}
                </span>
              )}

              <h3 className="editorial-heading text-2xl">{plan.name}</h3>
              <p className="mt-2 text-sm text-muted">{plan.description}</p>

              <div className="mt-8">
                <span className="text-xs text-muted">{SECTIONS.pricing.from} </span>
                <p className="font-[family-name:var(--font-exo2)] text-3xl font-bold tracking-tight">
                  {formatPrice(plan.price)}
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
                {SECTIONS.pricing.choosePlan}
              </a>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
