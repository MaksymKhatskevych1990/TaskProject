"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { formatPrice, HERO, HERO_BRIEF } from "@/lib/site-data";
import { cn } from "@/lib/utils";

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
    if (video.readyState >= 1) startTypingLoop();

    return () => video.removeEventListener("loadedmetadata", onLoaded);
  }, [startTypingLoop]);

  return (
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
      <video
        ref={videoRef}
        muted
        playsInline
        preload="auto"
        onTimeUpdate={handleTimeUpdate}
        className="h-full w-full object-cover object-top"
      >
        <source src="/video/first.mp4" type="video/mp4" />
      </video>
    </div>
  );
}

export function HeroSection() {
  const [selectedId, setSelectedId] = useState<(typeof HERO_BRIEF)[number]["id"]>("site");
  const selected = HERO_BRIEF.find((item) => item.id === selectedId) ?? HERO_BRIEF[0];

  return (
    <section className="relative min-h-[100svh] overflow-hidden">
      <div
        className="pointer-events-none absolute inset-y-0 right-0 hidden w-[min(52vw,640px)] lg:block"
        aria-hidden="true"
      >
        <div className="pointer-events-auto absolute inset-0 [mask-image:linear-gradient(to_right,transparent_0%,black_28%)]">
          <HeroVideo />
        </div>
      </div>

      <div className="relative z-10 mx-auto flex min-h-[100svh] max-w-[90rem] flex-col justify-between px-5 pb-8 pt-28 sm:px-8 sm:pb-10 lg:px-12 lg:pb-12">
        <div className="grid gap-10 lg:grid-cols-[minmax(0,1fr)_minmax(0,0.85fr)] lg:items-end lg:gap-8">
          <div className="hologram-panel max-w-3xl">
            <div
              className="hologram-reveal flex flex-wrap items-baseline gap-x-4 gap-y-1"
              style={{ animationDelay: "0ms" }}
            >
              <span className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.18em] text-accent-bright">
                {HERO.status}
              </span>
              <span className="text-sm text-muted">{HERO.statusMeta}</span>
            </div>

            <h1
              className="hologram-reveal hologram-reveal-text hologram-glow mt-8 font-[family-name:var(--font-exo2)] text-[clamp(2.6rem,7.2vw,5.25rem)] font-extrabold leading-[0.95] tracking-[-0.04em] text-surface-warm"
              style={{ animationDelay: "220ms" }}
            >
              {HERO.title}
            </h1>

            <p
              className="hologram-reveal mt-5 max-w-md text-base text-surface-warm-muted"
              style={{ animationDelay: "480ms" }}
            >
              {HERO.hint}
            </p>
          </div>

          <div className="relative mx-auto aspect-[3/4] w-full max-w-[220px] lg:hidden">
            <HeroVideo />
            <p className="mt-2 text-center font-[family-name:var(--font-jetbrains)] text-[10px] tracking-wide text-muted">
              наведи курсор →
            </p>
          </div>
        </div>

        <div className="mt-10 max-w-3xl lg:mt-0">
          <div
            className="hologram-reveal border-t border-[var(--card-border)]"
            style={{ animationDelay: "720ms" }}
            role="listbox"
            aria-label="Тип проєкту"
          >
            {HERO_BRIEF.map((item, index) => {
              const isActive = item.id === selectedId;

              return (
                <button
                  key={item.id}
                  type="button"
                  role="option"
                  aria-selected={isActive}
                  onClick={() => setSelectedId(item.id)}
                  className={cn(
                    "grid w-full grid-cols-[auto_1fr_auto] items-baseline gap-4 border-b border-[var(--card-border)] py-4 text-left transition-colors sm:gap-6 sm:py-5",
                    isActive ? "text-foreground" : "text-muted hover:text-foreground",
                  )}
                >
                  <span className="font-[family-name:var(--font-jetbrains)] text-[11px] text-accent-bright">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span
                    className={cn(
                      "font-[family-name:var(--font-exo2)] text-2xl tracking-tight sm:text-3xl",
                      isActive && "text-accent-bright",
                    )}
                  >
                    {item.label}
                  </span>
                  <span className="hidden text-sm sm:block">
                    {item.duration}
                    <span className="mx-2 text-muted">·</span>
                    від {formatPrice(item.price)}
                  </span>
                </button>
              );
            })}
          </div>

          <div
            className="hologram-reveal mt-8 flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between"
            style={{ animationDelay: "960ms" }}
          >
            <div className="max-w-md">
              <p className="text-sm leading-relaxed text-surface-warm-muted">
                {selected.includes}
              </p>
              <p className="mt-3 font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-[0.14em] text-muted sm:hidden">
                {selected.duration} · від {formatPrice(selected.price)}
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <a
                href={`?plan=${selected.plan}&need=${selected.id}#contact`}
                className="btn-primary px-7 py-3.5"
              >
                {HERO.primaryCta}
              </a>
              <a href="#portfolio" className="btn-secondary px-5 py-3.5">
                {HERO.secondaryCta}
              </a>
            </div>
          </div>
        </div>

        <ul className="mt-10 flex flex-wrap gap-x-8 gap-y-2 border-t border-[var(--card-border)] pt-5 text-xs text-muted">
          {HERO.conditions.map((item) => (
            <li key={item} className="flex items-center gap-2">
              <span className="h-1 w-1 rounded-full bg-accent" />
              {item}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
