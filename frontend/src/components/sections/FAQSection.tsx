"use client";

import { useState } from "react";
import { FAQ_ITEMS, SECTIONS } from "@/lib/site-data";
import { cn } from "@/lib/utils";

export function FAQSection() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section id="faq" className="py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="grid gap-12 lg:grid-cols-[280px_1fr] lg:gap-20">
          <div>
            <p className="section-number mb-4">07</p>
            <h2 className="editorial-heading text-3xl sm:text-4xl">
              {SECTIONS.faq.title}
            </h2>
          </div>

          <div>
            {FAQ_ITEMS.map((item, index) => {
              const isOpen = openIndex === index;

              return (
                <div
                  key={item.question}
                  className="border-t border-[var(--card-border)]"
                >
                  <button
                    type="button"
                    onClick={() => setOpenIndex(isOpen ? null : index)}
                    className="flex w-full items-start justify-between gap-6 py-6 text-left"
                    aria-expanded={isOpen}
                  >
                    <span className="text-base font-medium">{item.question}</span>
                    <span
                      className={cn(
                        "mt-1 shrink-0 font-[family-name:var(--font-jetbrains)] text-sm text-muted transition-transform duration-300",
                        isOpen && "rotate-45 text-accent",
                      )}
                    >
                      +
                    </span>
                  </button>
                  <div
                    className={cn(
                      "grid transition-all duration-300 ease-in-out",
                      isOpen ? "grid-rows-[1fr]" : "grid-rows-[0fr]",
                    )}
                  >
                    <div className="overflow-hidden">
                      <p className="pb-6 text-sm leading-relaxed text-muted">
                        {item.answer}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
