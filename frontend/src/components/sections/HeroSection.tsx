"use client";

import { useEffect, useRef, useState } from "react";
import { HERO } from "@/lib/site-data";

function BrowserMockup() {
  return (
    <div className="animate-float relative mx-auto w-full max-w-md">
      <div className="overflow-hidden rounded-2xl border border-white/10 bg-[#0d1224] shadow-2xl shadow-cyan/10">
        <div className="flex items-center gap-1.5 border-b border-white/5 px-4 py-3">
          <span className="h-2.5 w-2.5 rounded-full bg-red-400/80" />
          <span className="h-2.5 w-2.5 rounded-full bg-yellow-400/80" />
          <span className="h-2.5 w-2.5 rounded-full bg-green-400/80" />
          <span className="ml-2 font-[family-name:var(--font-jetbrains)] text-[10px] text-muted">
            devcraft.studio
          </span>
        </div>
        <div className="space-y-3 p-4">
          <div className="h-3 w-3/4 rounded bg-gradient-to-r from-cyan/40 to-violet/40" />
          <div className="h-2 w-full rounded bg-white/5" />
          <div className="h-2 w-5/6 rounded bg-white/5" />
          <div className="mt-4 grid grid-cols-3 gap-2">
            {[1, 2, 3].map((i) => (
              <div key={i} className="h-16 rounded-lg bg-white/5" />
            ))}
          </div>
        </div>
      </div>

      <div className="absolute -right-4 top-8 w-44 rounded-xl border border-cyan/30 bg-[#0d1224] p-3 shadow-lg shadow-cyan/20">
        <div className="mb-2 flex items-center gap-2">
          <span className="flex h-6 w-6 items-center justify-center rounded-full bg-cyan/20 text-xs">
            🤖
          </span>
          <span className="font-[family-name:var(--font-jetbrains)] text-[10px] text-cyan">
            AI-бот
          </span>
        </div>
        <div className="space-y-1.5">
          <div className="rounded-lg rounded-bl-none bg-cyan/10 px-2 py-1 text-[10px]">
            Здравствуйте! Чем помочь?
          </div>
          <div className="ml-auto w-fit rounded-lg rounded-br-none bg-violet/20 px-2 py-1 text-[10px]">
            Хочу сайт
          </div>
        </div>
      </div>
    </div>
  );
}

export function HeroSection() {
  const [visible, setVisible] = useState(false);
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    setVisible(true);
  }, []);

  return (
    <section
      ref={ref}
      className="relative overflow-hidden pt-28 pb-20 sm:pt-32 sm:pb-28"
    >
      <div className="glow-orb -left-32 top-20 h-96 w-96 bg-cyan/20" />
      <div className="glow-orb -right-32 bottom-0 h-80 w-80 bg-violet/20" />

      <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-4 sm:px-6 lg:grid-cols-2">
        <div
          className={`space-y-6 transition-all duration-700 ${visible ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"}`}
        >
          <div className="inline-flex items-center gap-2 rounded-full border border-cyan/30 bg-cyan/5 px-4 py-1.5">
            <span className="h-2 w-2 animate-pulse rounded-full bg-cyan" />
            <span className="font-[family-name:var(--font-jetbrains)] text-xs text-cyan">
              {HERO.badge}
            </span>
          </div>

          <h1 className="font-[family-name:var(--font-exo2)] text-4xl font-bold leading-tight tracking-tight sm:text-5xl lg:text-6xl">
            {HERO.title}{" "}
            <span className="gradient-text">{HERO.titleAccent}</span>
          </h1>

          <p className="max-w-xl text-lg text-muted">{HERO.subtitle}</p>

          <div className="flex flex-wrap gap-4">
            <a
              href="#contact"
              className="rounded-full bg-gradient-to-r from-cyan to-violet px-6 py-3 text-sm font-semibold text-[#070b18] transition-opacity hover:opacity-90"
            >
              {HERO.primaryCta}
            </a>
            <a
              href="#cases"
              className="rounded-full border border-white/10 px-6 py-3 text-sm font-medium transition-colors hover:border-white/20 hover:bg-white/5"
            >
              {HERO.secondaryCta}
            </a>
          </div>
        </div>

        <BrowserMockup />
      </div>
    </section>
  );
}
