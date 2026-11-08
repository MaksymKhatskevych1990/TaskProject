"use client";

import { useEffect, useRef, useState } from "react";
import { useSiteContent } from "@/components/site-content/SiteContentProvider";

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
          const duration = 1200;
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
    <span
      ref={ref}
      className="font-[family-name:var(--font-exo2)] text-3xl font-bold tracking-tight sm:text-4xl"
    >
      {display}
      <span className="accent-text">{suffix}</span>
    </span>
  );
}

export function SocialProofSection() {
  const content = useSiteContent();
  const featured = content.testimonials[0];

  return (
    <section className="border-y border-[var(--card-border)]">
      <div className="mx-auto max-w-[90rem] px-5 py-16 sm:px-8 lg:px-12">
        <div className="grid gap-12 lg:grid-cols-[1.2fr_1fr] lg:gap-20">
          {featured ? (
            <blockquote>
              <p className="pull-quote text-foreground">
                &ldquo;{featured.text}&rdquo;
              </p>
              <footer className="mt-6 flex items-baseline gap-3">
                <cite className="not-italic text-sm font-medium">{featured.name}</cite>
                <span className="text-xs text-muted">— {featured.role}</span>
              </footer>
            </blockquote>
          ) : (
            <div />
          )}

          <div className="grid grid-cols-2 gap-x-8 gap-y-10 border-l border-[var(--card-border)] pl-8 lg:pl-12">
            {content.stats.map((stat) => (
              <div key={stat.label}>
                <AnimatedCounter
                  value={stat.value}
                  suffix={stat.suffix}
                  decimals={stat.decimals}
                />
                <p className="mt-1.5 text-xs leading-snug text-muted">{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="overflow-hidden border-t border-[var(--card-border)] py-4">
        <div className="animate-marquee flex w-max gap-16 whitespace-nowrap px-8">
          {[...content.testimonials, ...content.testimonials].map((item, i) => (
            <span key={`${item.name}-${i}`} className="flex items-center gap-4 text-sm text-muted">
              <span className="accent-text">—</span>
              <span>&ldquo;{item.text}&rdquo;</span>
              <span className="text-xs">· {item.name}</span>
            </span>
          ))}
        </div>
      </div>
    </section>
  );
}
