"use client";

import { useEffect, useRef, useState } from "react";

type UseScrollRevealOptions = {
  threshold?: number;
  rootMargin?: string;
};

export function useScrollReveal<T extends HTMLElement = HTMLElement>({
  threshold = 0.15,
  rootMargin = "0px 0px -40px 0px",
}: UseScrollRevealOptions = {}) {
  const ref = useRef<T>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
          observer.disconnect();
        }
      },
      { threshold, rootMargin },
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, [rootMargin, threshold]);

  return { ref, visible };
}
