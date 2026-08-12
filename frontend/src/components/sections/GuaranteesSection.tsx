import { GUARANTEES, SECTIONS } from "@/lib/site-data";

export function GuaranteesSection() {
  return (
    <section id="guarantees" className="bg-[var(--card)] py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="grid gap-12 lg:grid-cols-2 lg:gap-20">
          <div>
            <p className="section-number mb-4">06</p>
            <h2 className="editorial-heading text-3xl sm:text-4xl">
              {SECTIONS.guarantees.title}
            </h2>
          </div>

          <div className="space-y-8">
            {GUARANTEES.map((item, index) => (
              <div
                key={item.title}
                className="grid grid-cols-[2rem_1fr] gap-4 border-t border-[var(--card-border)] pt-8 first:border-t-0 first:pt-0"
              >
                <span className="font-[family-name:var(--font-jetbrains)] text-xs text-muted">
                  {String(index + 1).padStart(2, "0")}
                </span>
                <div>
                  <h3 className="font-medium">{item.title}</h3>
                  <p className="mt-1.5 text-sm leading-relaxed text-muted">
                    {item.description}
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
