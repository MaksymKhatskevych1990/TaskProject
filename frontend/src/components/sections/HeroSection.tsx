"use client";

import { useCallback, useEffect, useRef } from "react";
import { CodeTypingBackground } from "@/components/sections/CodeTypingBackground";
import { RevealOnScroll } from "@/components/ui/RevealOnScroll";
import { HERO } from "@/lib/site-data";

const TYPING_LOOP_START = 7;
const TYPING_LOOP_END = 9.95;
const HEAD_TURN_START = 1.75;
const HEAD_TURN_END = 4;

function HeroVideo() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const hoveredRef = useRef(false);

  const startTypingLoop = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;

    video.currentTime = TYPING_LOOP_START;
    void video.play();
  }, []);

  const handleTimeUpdate = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;

    if (hoveredRef.current) {
      if (video.currentTime >= HEAD_TURN_END) {
        video.pause();
        video.currentTime = HEAD_TURN_END;
      }
      return;
    }

    if (video.currentTime >= TYPING_LOOP_END || video.currentTime < TYPING_LOOP_START) {
      video.currentTime = TYPING_LOOP_START;
    }
  }, []);

  const handlePointerEnter = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;

    hoveredRef.current = true;
    video.currentTime = HEAD_TURN_START;
    void video.play();
  }, []);

  const handlePointerLeave = useCallback(() => {
    hoveredRef.current = false;
    startTypingLoop();
  }, [startTypingLoop]);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    const onLoaded = () => startTypingLoop();

    video.addEventListener("loadedmetadata", onLoaded);
    if (video.readyState >= 1) {
      startTypingLoop();
    }

    return () => video.removeEventListener("loadedmetadata", onLoaded);
  }, [startTypingLoop]);

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
          aria-label={HERO.chameleon.ariaLabel}
        >
          <div className="relative overflow-hidden rounded-2xl rounded-tr-none border border-white/10 bg-[#0d1224] shadow-2xl shadow-cyan/10 ring-1 ring-cyan/10">
            <video
              ref={videoRef}
              muted
              playsInline
              preload="auto"
              onTimeUpdate={handleTimeUpdate}
              className="aspect-[4/5] w-full object-cover"
            >
              <source src="/video/first.mp4" type="video/mp4" />
            </video>
          </div>
        </div>
      </div>
    </RevealOnScroll>
  );
}

export function HeroSection() {
  return (
    <section className="relative overflow-hidden pt-28 pb-20 sm:pt-32 sm:pb-28">
      <CodeTypingBackground />

      <div className="glow-orb -left-32 top-20 h-96 w-96 bg-cyan/20" />
      <div className="glow-orb -right-32 bottom-0 h-80 w-80 bg-violet/20" />

      <div className="relative z-10 mx-auto grid max-w-6xl items-end gap-10 px-4 sm:px-6 lg:grid-cols-[1.1fr_0.9fr] lg:gap-16">
        <div className="hologram-panel space-y-7 lg:pb-6">
          <div className="hologram-reveal badge-tag" style={{ animationDelay: "0ms" }}>
            <span className="h-1.5 w-1.5 shrink-0 bg-cyan" aria-hidden="true" />
            {HERO.badge}
          </div>

          <h1
            className="hologram-reveal hologram-reveal-text hologram-glow font-[family-name:var(--font-exo2)] text-4xl font-bold leading-[1.08] tracking-tight sm:text-5xl lg:text-[3.35rem]"
            style={{ animationDelay: "280ms" }}
          >
            {HERO.title}{" "}
            <span className="gradient-text">{HERO.titleAccent}</span>
          </h1>

          <p
            className="hologram-reveal max-w-lg text-lg leading-relaxed text-muted"
            style={{ animationDelay: "560ms" }}
          >
            {HERO.subtitle}
          </p>

          <div className="flex flex-col gap-3 pt-1 sm:flex-row sm:items-center sm:gap-4">
            <a
              href="#contact"
              className="hologram-reveal btn-primary px-7 py-3.5"
              style={{ animationDelay: "840ms" }}
            >
              {HERO.primaryCta}
            </a>
            <a
              href="#portfolio"
              className="hologram-reveal btn-secondary px-7 py-3.5"
              style={{ animationDelay: "1020ms" }}
            >
              {HERO.secondaryCta}
            </a>
          </div>
        </div>

        <div className="lg:-mr-4 lg:translate-y-2">
          <HeroVideo />
        </div>
      </div>
    </section>
  );
}
