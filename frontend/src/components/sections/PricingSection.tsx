import { formatPrice, PRICING_PLANS, SECTIONS } from "@/lib/site-data";
import { cn } from "@/lib/utils";

export function PricingSection() {
  return (
    <section id="pricing" className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 section-intro mx-auto max-w-2xl">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            {SECTIONS.pricing.eyebrow}
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            {SECTIONS.pricing.title}
          </h2>
          <p className="mt-3 text-sm text-muted">
            {SECTIONS.pricing.subtitle}
          </p>
        </div>

        <div className="grid items-end gap-5 lg:grid-cols-3">
          {PRICING_PLANS.map((plan, index) => (
            <article
              key={plan.name}
              className={cn(
                "relative flex flex-col border p-6",
                index % 2 === 0 ? "surface-card" : "surface-card-alt",
                plan.highlighted
                  ? "gradient-border border-transparent bg-card shadow-xl shadow-violet/10 lg:-translate-y-2"
                  : "border-white/5 bg-card",
              )}
            >
              {"badge" in plan && plan.badge && (
                <span className="absolute -top-3 left-5 bg-gradient-to-r from-cyan to-violet px-3 py-1 font-[family-name:var(--font-jetbrains)] text-[10px] font-semibold uppercase tracking-wider text-[#070b18]">
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
                  "mt-8 block py-3 text-center text-sm font-semibold transition-opacity hover:opacity-90",
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
