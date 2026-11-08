import { WHY_US } from "@/lib/marketing-pages";

export function WhyUsSection() {
  return (
    <section id="why" className="border-b border-[var(--card-border)] py-16 sm:py-20">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="mb-10 max-w-lg">
          <p className="label-mono mb-3">Чому замовляють</p>
          <h2 className="editorial-heading text-3xl sm:text-4xl">
            Щоб не сумніватись після заявки
          </h2>
        </div>
        <div className="grid gap-10 md:grid-cols-3">
          {WHY_US.map((item, index) => (
            <article key={item.title}>
              <p className="section-number mb-4">{String(index + 1).padStart(2, "0")}</p>
              <h3 className="text-lg font-semibold">{item.title}</h3>
              <p className="mt-3 text-sm leading-relaxed text-muted">{item.text}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
