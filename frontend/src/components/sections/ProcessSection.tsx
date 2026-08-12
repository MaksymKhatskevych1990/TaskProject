import { PROCESS_STEPS, SECTIONS } from "@/lib/site-data";

export function ProcessSection() {
  return (
    <section id="process" className="py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="grid gap-16 lg:grid-cols-[280px_1fr] lg:gap-20">
          <div className="lg:sticky lg:top-28 lg:self-start">
            <p className="section-number mb-4">04</p>
            <h2 className="editorial-heading text-3xl sm:text-4xl">
              {SECTIONS.process.title}
            </h2>
            <p className="mt-4 text-sm text-muted">
              Від першого дзвінка до запуску — прозорий процес без сюрпризів.
            </p>
          </div>

          <div>
            {PROCESS_STEPS.map((step, index) => (
              <div
                key={step.step}
                className="relative grid grid-cols-[3rem_1fr] gap-6 border-t border-[var(--card-border)] py-10 first:border-t-0 first:pt-0"
              >
                <span className="font-[family-name:var(--font-jetbrains)] text-sm text-accent">
                  {String(step.step).padStart(2, "0")}
                </span>
                <div>
                  <h3 className="text-lg font-semibold">{step.title}</h3>
                  <p className="mt-2 max-w-md text-sm leading-relaxed text-muted">
                    {step.description}
                  </p>
                  {index < PROCESS_STEPS.length - 1 && (
                    <div className="absolute left-[1.125rem] top-[3.5rem] h-[calc(100%-2rem)] w-px bg-[var(--card-border)]" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
