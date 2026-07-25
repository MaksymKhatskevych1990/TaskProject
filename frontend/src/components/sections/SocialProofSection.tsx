"use client";

import { useEffect, useRef, useState } from "react";
import { STATS, TESTIMONIALS } from "@/lib/site-data";

function AnimatedCounter({
  value,
  suffix,
  decimals = 0,
}: {
  value: number;
  suffix: string;
  decimals?: number;
}) {
  const [count, setCount] = useState(0);
  const ref = useRef<HTMLSpanElement>(null);
  const started = useRef(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !started.current) {
          started.current = true;
          const duration = 1500;
          const start = performance.now();

          const tick = (now: number) => {
            const progress = Math.min((now - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            setCount(value * eased);
            if (progress < 1) requestAnimationFrame(tick);
          };

          requestAnimationFrame(tick);
        }
      },
      { threshold: 0.3 },
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [value]);

  const display =
    decimals > 0 ? count.toFixed(decimals) : Math.round(count).toString();

  return (
    <span ref={ref} className="gradient-text font-[family-name:var(--font-exo2)] text-4xl font-bold sm:text-5xl">
      {display}
      {suffix}
    </span>
  );
}

export function SocialProofSection() {
  return (
    <section className="relative py-20">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="grid grid-cols-2 gap-8 lg:grid-cols-4">
          {STATS.map((stat) => (
            <div key={stat.label} className="text-center">
              <AnimatedCounter
                value={stat.value}
                suffix={stat.suffix}
                decimals={"decimals" in stat ? stat.decimals : 0}
              />
              <p className="mt-2 text-sm text-muted">{stat.label}</p>
            </div>
          ))}
        </div>

        <div className="mt-16 grid gap-6 md:grid-cols-3">
          {TESTIMONIALS.map((item) => (
            <article
              key={item.name}
              className="rounded-2xl border border-white/5 bg-card p-6 transition-colors hover:border-white/10"
            >
              <div className="mb-3 text-amber-400">
                {"★".repeat(item.rating)}
              </div>
              <p className="mb-4 text-sm leading-relaxed text-muted">
                &ldquo;{item.text}&rdquo;
              </p>
              <div>
                <p className="font-medium">{item.name}</p>
                <p className="text-xs text-muted">{item.role}</p>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
