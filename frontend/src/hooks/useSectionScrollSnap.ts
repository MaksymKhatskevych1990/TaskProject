"use client";

import { useEffect, useRef } from "react";

const HEADER_OFFSET = 64;
const SCROLL_DURATION_MS = 1100;
const COOLDOWN_MS = SCROLL_DURATION_MS + 150;
const WHEEL_THRESHOLD = 40;

function easeInOutCubic(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2;
}

function animateScrollTo(
  targetY: number,
  duration: number,
  onFrame: () => void,
): { promise: Promise<void>; cancel: () => void } {
  let frameId = 0;
  let cancelled = false;

  const promise = new Promise<void>((resolve) => {
    const startY = window.scrollY;
    const distance = targetY - startY;
    const startTime = performance.now();

    const step = (now: number) => {
      if (cancelled) {
        resolve();
        return;
      }

      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const eased = easeInOutCubic(progress);

      window.scrollTo(0, startY + distance * eased);
      onFrame();

      if (progress < 1) {
        frameId = requestAnimationFrame(step);
      } else {
        resolve();
      }
    };

    frameId = requestAnimationFrame(step);
  });

  return {
    promise,
    cancel: () => {
      cancelled = true;
      cancelAnimationFrame(frameId);
    },
  };
}

export function useSectionScrollSnap(enabled = true) {
  const locked = useRef(false);
  const accumulated = useRef(0);
  const lockTimer = useRef<number | undefined>(undefined);
  const scrollAnimation = useRef<{ cancel: () => void } | null>(null);

  useEffect(() => {
    if (!enabled) return;

    document.documentElement.classList.add("snap-scroll");

    const getSections = () =>
      Array.from(document.querySelectorAll<HTMLElement>("[data-snap-section]"));

    const getCurrentIndex = (sections: HTMLElement[]) => {
      const marker = window.scrollY + HEADER_OFFSET + 2;
      let index = 0;

      for (let i = 0; i < sections.length; i++) {
        if (sections[i].offsetTop <= marker) index = i;
      }

      return index;
    };

    const scrollToSection = (section: HTMLElement) => {
      scrollAnimation.current?.cancel();
      locked.current = true;
      accumulated.current = 0;

      const targetY = Math.max(0, section.offsetTop - HEADER_OFFSET);
      const animation = animateScrollTo(targetY, SCROLL_DURATION_MS, () => {});

      scrollAnimation.current = animation;

      clearTimeout(lockTimer.current);
      animation.promise.then(() => {
        lockTimer.current = window.setTimeout(() => {
          locked.current = false;
        }, 150);
      });
    };

    const onWheel = (e: WheelEvent) => {
      if (e.target instanceof Element && e.target.closest("[data-snap-ignore]")) {
        return;
      }

      const sections = getSections();
      if (sections.length === 0) return;

      if (locked.current) {
        e.preventDefault();
        return;
      }

      accumulated.current += e.deltaY;
      if (Math.abs(accumulated.current) < WHEEL_THRESHOLD) return;

      const direction = accumulated.current > 0 ? 1 : -1;
      accumulated.current = 0;

      const index = getCurrentIndex(sections);
      const current = sections[index];
      const currentTop = current.offsetTop - HEADER_OFFSET;
      const currentBottom = currentTop + current.offsetHeight;
      const viewportBottom = window.scrollY + window.innerHeight;

      if (direction > 0 && viewportBottom < currentBottom - 8) {
        return;
      }

      if (direction < 0 && window.scrollY > currentTop + 8) {
        return;
      }

      const targetIndex = index + direction;
      if (targetIndex < 0 || targetIndex >= sections.length) return;

      e.preventDefault();
      scrollToSection(sections[targetIndex]);
    };

    const onAnchorClick = (e: MouseEvent) => {
      const target = e.target;
      if (!(target instanceof Element)) return;

      const link = target.closest<HTMLAnchorElement>("a[href*='#']");
      if (!link) return;

      const url = new URL(link.href, window.location.href);
      if (url.pathname !== window.location.pathname || !url.hash) return;

      const el = document.querySelector(url.hash);
      if (!(el instanceof HTMLElement)) return;

      const section = el.closest<HTMLElement>("[data-snap-section]");
      if (!section) return;

      e.preventDefault();
      scrollToSection(section);
      history.pushState(null, "", url.hash);
    };

    window.addEventListener("wheel", onWheel, { passive: false });
    document.addEventListener("click", onAnchorClick);

    return () => {
      document.documentElement.classList.remove("snap-scroll");
      window.removeEventListener("wheel", onWheel);
      document.removeEventListener("click", onAnchorClick);
      scrollAnimation.current?.cancel();
      clearTimeout(lockTimer.current);
    };
  }, [enabled]);
}
