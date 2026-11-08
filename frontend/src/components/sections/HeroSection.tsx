"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useSiteContent } from "@/components/site-content/SiteContentProvider";
import { formatSitePrice } from "@/lib/site-content";
import { cn } from "@/lib/utils";

const TYPING_LOOP_START = 7;
const TYPING_LOOP_END = 9.85;
const HEAD_TURN_START = 1.75;
const HEAD_TURN_END = 4;

function seekAndPlay(video: HTMLVideoElement, time: number) {
  const play = () => {
    void video.play();
  };

  if (Math.abs(video.currentTime - time) < 0.04) {
    play();
    return;
  }

  const onSeeked = () => {
    video.removeEventListener("seeked", onSeeked);
    play();
  };

  video.addEventListener("seeked", onSeeked);
  video.currentTime = time;
}

function HeroVideo({
  className,
  ariaLabel,
  cover = false,
}: {
  className?: string;
  ariaLabel: string;
  cover?: boolean;
}) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const lookingRef = useRef(false);

  const startTypingLoop = useCallback(() => {
    const video = videoRef.current;
    if (!video) return;
    lookingRef.current = false;
    seekAndPlay(video, TYPING_LOOP_START);
  }, []);

  const lookAtCursor = useCallback(() => {
    const video = videoRef.current;
    if (!video || lookingRef.current) return;
    lookingRef.current = true;
    seekAndPlay(video, HEAD_TURN_START);
  }, []);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;

    let frame = 0;

    const tick = () => {
      if (lookingRef.current) {
        if (video.currentTime >= HEAD_TURN_END && video.currentTime < TYPING_LOOP_START) {
          video.pause();
          if (Math.abs(video.currentTime - HEAD_TURN_END) > 0.03) {
            video.currentTime = HEAD_TURN_END;
          }
        }
      } else if (
        video.ended ||
        video.currentTime >= TYPING_LOOP_END ||
        video.currentTime < TYPING_LOOP_START - 0.05
      ) {
        video.currentTime = TYPING_LOOP_START;
        void video.play();
      }

      frame = requestAnimationFrame(tick);
    };

    const onLoaded = () => startTypingLoop();
    video.addEventListener("loadedmetadata", onLoaded);
    video.addEventListener("ended", startTypingLoop);
    if (video.readyState >= 1) startTypingLoop();
    frame = requestAnimationFrame(tick);

    return () => {
      cancelAnimationFrame(frame);
      video.removeEventListener("loadedmetadata", onLoaded);
      video.removeEventListener("ended", startTypingLoop);
    };
  }, [startTypingLoop]);

  return (
    <div
      className={cn("h-full w-full cursor-pointer select-none", className)}
      onPointerEnter={lookAtCursor}
      onPointerLeave={startTypingLoop}
      onPointerDown={lookAtCursor}
      role="img"
      aria-label={ariaLabel}
    >
      <video
        ref={videoRef}
        muted
        playsInline
        autoPlay
        preload="auto"
        className={cn("h-full w-full object-center", cover ? "object-cover" : "object-contain")}
      >
        <source src="/video/first.mp4" type="video/mp4" />
      </video>
    </div>
  );
}

export function HeroSection({ heading }: { heading?: string }) {
  const content = useSiteContent();
  const offers = content.hero.offers;
  const [selectedId, setSelectedId] = useState(offers[0]?.id ?? "site");
  const selected = offers.find((item) => item.id === selectedId) ?? offers[0];

  return (
    <section className="relative h-[100svh] max-h-[100svh] min-h-0 overflow-hidden">
      <div className="absolute inset-y-0 right-0 z-[1] hidden h-full w-[min(58vw,820px)] items-center lg:flex">
        <div className="hero-video-frame relative w-full">
          <div className="relative aspect-video w-full">
            <div className="hero-video-blend absolute inset-0">
              <HeroVideo ariaLabel={content.hero.chameleonLabel} cover />
            </div>
            <div aria-hidden="true" className="hero-video-edge-top" />
            <div aria-hidden="true" className="hero-video-edge-bottom" />
          </div>
        </div>
      </div>

      <div className="relative z-10 mx-auto flex h-full min-h-0 max-w-[90rem] flex-col overflow-hidden px-5 pb-4 pt-[4.75rem] sm:px-8 sm:pb-6 lg:pointer-events-none lg:px-12 lg:pb-8 lg:pr-[min(52vw,34rem)]">
        <div className="hologram-panel w-full max-w-xl shrink-0 lg:pointer-events-auto">
          <div
            className="hologram-reveal flex flex-wrap items-baseline gap-x-4 gap-y-1"
            style={{ animationDelay: "0ms" }}
          >
            <span className="font-[family-name:var(--font-jetbrains)] text-[11px] uppercase tracking-[0.18em] text-accent-bright">
              {content.hero.status}
            </span>
            <span className="text-sm text-muted">{content.hero.statusMeta}</span>
          </div>

          <h1
            className="hologram-glow mt-4 max-w-full font-[family-name:var(--font-exo2)] text-[clamp(1.75rem,4.4vw,3.35rem)] font-extrabold leading-[1.08] tracking-[-0.04em] text-balance text-surface-warm lg:mt-6"
            style={{ animationDelay: "220ms" }}
          >
            {heading || content.hero.title}
          </h1>

          <p
            className="hologram-reveal mt-3 max-w-md text-sm text-surface-warm-muted sm:text-base"
            style={{ animationDelay: "480ms" }}
          >
            {content.hero.hint}
          </p>
        </div>

        <div className="relative mx-auto min-h-0 w-full max-w-sm flex-1 lg:hidden">
          <HeroVideo ariaLabel={content.hero.chameleonLabel} />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-x-0 top-0 h-16 bg-gradient-to-b from-background to-transparent"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-x-0 bottom-0 h-16 bg-gradient-to-t from-background to-transparent"
          />
        </div>

        <div className="w-full max-w-xl shrink-0 pt-3 lg:pointer-events-auto lg:mt-auto lg:pt-6">
          <div
            className="hologram-reveal border-t border-[var(--card-border)]"
            style={{ animationDelay: "720ms" }}
            role="listbox"
            aria-label="Тип проєкту"
          >
            {offers.map((item, index) => {
              const isActive = item.id === selectedId;

              return (
                <button
                  key={item.id}
                  type="button"
                  role="option"
                  aria-selected={isActive}
                  onClick={() => setSelectedId(item.id)}
                  className={cn(
                    "grid w-full grid-cols-[auto_1fr_auto] items-baseline gap-3 border-b border-[var(--card-border)] py-2 text-left transition-colors sm:gap-6 sm:py-3 lg:py-3.5",
                    isActive ? "text-foreground" : "text-muted hover:text-foreground",
                  )}
                >
                  <span className="font-[family-name:var(--font-jetbrains)] text-[11px] text-accent-bright">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <span
                    className={cn(
                      "font-[family-name:var(--font-exo2)] text-xl tracking-tight sm:text-2xl lg:text-3xl",
                      isActive && "text-accent-bright",
                    )}
                  >
                    {item.label}
                  </span>
                  <span className="hidden text-sm sm:block">
                    {item.duration}
                    <span className="mx-2 text-muted">·</span>
                    {content.sections.pricing.from} {formatSitePrice(item.price, content)}
                  </span>
                </button>
              );
            })}
          </div>

          <div className="hologram-reveal mt-4 sm:mt-6" style={{ animationDelay: "960ms" }}>
            <p className="max-w-md text-sm leading-relaxed text-surface-warm-muted">
              {selected?.includes}
            </p>
            {selected ? (
              <p className="mt-2 font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-[0.14em] text-muted sm:hidden">
                {selected.duration} · {content.sections.pricing.from}{" "}
                {formatSitePrice(selected.price, content)}
              </p>
            ) : null}

            <div className="mt-4 flex items-center gap-3">
              <a
                href={`?plan=${selected?.plan ?? ""}&need=${selected?.id ?? ""}#contact`}
                className="btn-primary h-11 min-w-[10.5rem] px-6"
              >
                {content.hero.primaryCta}
              </a>
              <a href="#portfolio" className="btn-secondary h-11 min-w-[10.5rem] px-6">
                {content.hero.secondaryCta}
              </a>
            </div>
          </div>

          <ul className="mt-4 hidden flex-wrap gap-x-6 gap-y-2 border-t border-[var(--card-border)] pt-3 text-xs text-muted sm:mt-5 sm:flex sm:pt-4">
            {content.hero.conditions.map((item) => (
              <li key={item} className="flex items-center gap-2">
                <span className="h-1 w-1 rounded-full bg-accent" />
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
