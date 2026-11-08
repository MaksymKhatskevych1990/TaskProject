import { COMPARISON } from "@/lib/marketing-pages";

export function ComparisonSection() {
  return (
    <section className="border-t border-[var(--card-border)] py-20 sm:py-28">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="mb-12 max-w-lg">
          <h2 className="editorial-heading text-3xl sm:text-4xl">{COMPARISON.title}</h2>
          <p className="mt-4 text-sm leading-relaxed text-muted">{COMPARISON.subtitle}</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full min-w-[40rem] border-collapse text-left text-sm">
            <thead>
              <tr className="border-b border-[var(--card-border)]">
                <th className="py-4 pr-4 font-medium text-muted"> </th>
                {COMPARISON.columns.map((column) => (
                  <th
                    key={column}
                    className={`py-4 pr-4 font-medium ${
                      column === "Chameleon" ? "accent-text" : "text-muted"
                    }`}
                  >
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {COMPARISON.rows.map((row) => (
                <tr key={row.label} className="border-b border-[var(--card-border)]">
                  <th className="py-4 pr-4 font-medium text-foreground">{row.label}</th>
                  {row.values.map((value, index) => (
                    <td
                      key={`${row.label}-${index}`}
                      className={`py-4 pr-4 ${
                        index === 2 ? "font-medium text-foreground" : "text-muted"
                      }`}
                    >
                      {value}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
