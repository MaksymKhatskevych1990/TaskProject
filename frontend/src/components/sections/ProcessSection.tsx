import { PROCESS_STEPS, SECTIONS } from "@/lib/site-data";

export function ProcessSection() {
  return (
    <section className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="mb-12 text-center">
          <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
            {SECTIONS.process.eyebrow}
          </p>
          <h2 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            {SECTIONS.process.title}
          </h2>
        </div>

        <div className="relative mx-auto max-w-2xl">
          <div className="absolute left-6 top-0 bottom-0 w-px bg-gradient-to-b from-cyan via-violet to-transparent" />

          <div className="space-y-8">
            {PROCESS_STEPS.map((step) => (
              <div key={step.step} className="relative flex gap-6 pl-2">
                <div className="relative z-10 flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-cyan/30 bg-[#070b18] font-[family-name:var(--font-exo2)] text-sm font-bold text-cyan shadow-lg shadow-cyan/20">
                  {step.step}
                </div>
                <div className="pb-2 pt-1">
                  <h3 className="font-[family-name:var(--font-exo2)] text-lg font-semibold">
                    {step.title}
                  </h3>
                  <p className="mt-1 text-sm leading-relaxed text-muted">
                    {step.description}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
