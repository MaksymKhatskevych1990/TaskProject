import { formatPrice, PRICING_PLANS, SECTIONS } from "@/lib/site-data";
import { cn } from "@/lib/utils";

export function PricingSection() {
  return (
    <section id="pricing" className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 text-center">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            {SECTIONS.pricing.eyebrow}
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            {SECTIONS.pricing.title}
          </h2>
          <p className="mx-auto mt-3 max-w-lg text-sm text-muted">
            {SECTIONS.pricing.subtitle}
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-3">
          {PRICING_PLANS.map((plan) => (
            <article
              key={plan.name}
              className={cn(
                "relative flex flex-col rounded-2xl border p-6",
                plan.highlighted
                  ? "gradient-border border-transparent bg-card shadow-xl shadow-violet/10"
                  : "border-white/5 bg-card",
              )}
            >
              {"badge" in plan && plan.badge && (
                <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-gradient-to-r from-cyan to-violet px-4 py-1 text-xs font-semibold text-[#070b18]">
                  {plan.badge}
                </span>
              )}

              <h3 className="font-[family-name:var(--font-exo2)] text-xl font-semibold">
                {plan.name}
              </h3>
              <p className="mt-1 text-sm text-muted">{plan.description}</p>

              <div className="mt-6">
                <span className="text-sm text-muted">{SECTIONS.pricing.from} </span>
                <span className="font-[family-name:var(--font-exo2)] text-3xl font-bold">
                  {formatPrice(plan.price)}
                </span>
              </div>

              <ul className="mt-6 flex-1 space-y-3">
                {plan.features.map((feature) => (
                  <li
                    key={feature}
                    className="flex items-start gap-2 text-sm text-muted"
                  >
                    <span className="mt-0.5 text-cyan">✓</span>
                    {feature}
                  </li>
                ))}
              </ul>

              <a
                href={`?plan=${plan.slug}#contact`}
                className={cn(
                  "mt-8 block rounded-full py-3 text-center text-sm font-semibold transition-opacity hover:opacity-90",
                  plan.highlighted
                    ? "bg-gradient-to-r from-cyan to-violet text-[#070b18]"
                    : "border border-white/10 hover:bg-white/5",
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
