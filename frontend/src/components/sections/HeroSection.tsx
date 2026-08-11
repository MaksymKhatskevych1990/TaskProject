"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { CodeTypingBackground } from "@/components/sections/CodeTypingBackground";
import { RevealOnScroll } from "@/components/ui/RevealOnScroll";
import { HERO } from "@/lib/site-data";
import { cn } from "@/lib/utils";

const NORMAL_PLAYBACK_RATE = 1;
const NERVOUS_PLAYBACK_RATE = 1.85;

function HeroVideo() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [nervous, setNervous] = useState(false);

  const setPlaybackRate = useCallback((rate: number) => {
    const video = videoRef.current;
    if (video) {
      video.playbackRate = rate;
    }
  }, []);

  const handlePointerEnter = useCallback(() => {
    setNervous(true);
    setPlaybackRate(NERVOUS_PLAYBACK_RATE);
  }, [setPlaybackRate]);

  const handlePointerLeave = useCallback(() => {
    setNervous(false);
    setPlaybackRate(NORMAL_PLAYBACK_RATE);
  }, [setPlaybackRate]);

  useEffect(() => {
    return () => setPlaybackRate(NORMAL_PLAYBACK_RATE);
  }, [setPlaybackRate]);

  return (
    <RevealOnScroll delayMs={200}>
      <div className="animate-float relative mx-auto w-full max-w-md">
        <div
          className="cursor-pointer select-none"
          onMouseEnter={handlePointerEnter}
          onMouseLeave={handlePointerLeave}
          onFocus={handlePointerEnter}
          onBlur={handlePointerLeave}
          onTouchStart={handlePointerEnter}
          onTouchEnd={handlePointerLeave}
          onTouchCancel={handlePointerLeave}
          tabIndex={0}
          role="img"
          aria-label="Chameleon Digital Studio — наведи курсор, щоб хameleon хвилювався"
        >
          <div
            className={cn(
              "overflow-hidden rounded-2xl border bg-[#0d1224] shadow-2xl transition-colors duration-200",
              nervous
                ? "animate-nervous-shake animate-nervous-glow border-orange-400/50"
                : "border-white/10 shadow-cyan/10 ring-1 ring-cyan/10",
            )}
          >
            <video
              ref={videoRef}
              autoPlay
              loop
              muted
              playsInline
              preload="metadata"
              className={cn(
                "aspect-[4/5] w-full object-cover transition-[filter] duration-200",
                nervous && "saturate-125 contrast-110",
              )}
            >
              <source src="/video/chameleon-coding.mp4" type="video/mp4" />
            </video>
          </div>
        </div>
      </div>
    </RevealOnScroll>
  );
}

export function HeroSection() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    setVisible(true);
  }, []);

  return (
    <section className="relative overflow-hidden pt-28 pb-20 sm:pt-32 sm:pb-28">
      <CodeTypingBackground />

      <div className="glow-orb -left-32 top-20 h-96 w-96 bg-cyan/20" />
      <div className="glow-orb -right-32 bottom-0 h-80 w-80 bg-violet/20" />

      <div className="relative z-10 mx-auto grid max-w-6xl items-center gap-12 px-4 sm:px-6 lg:grid-cols-2">
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
              href="#portfolio"
              className="rounded-full border border-white/10 px-6 py-3 text-sm font-medium transition-colors hover:border-white/20 hover:bg-white/5"
            >
              {HERO.secondaryCta}
            </a>
          </div>
        </div>

        <HeroVideo />
      </div>
    </section>
  );
}
