"use client";

import { useEffect, useState } from "react";
import { SITE } from "@/lib/site-data";

export function FloatingTelegramButton() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 400);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  if (!visible) return null;

  return (
    <a
      href={SITE.telegramUrl}
      target="_blank"
      rel="noopener noreferrer"
      aria-label="Написать в Telegram"
      className="animate-pulse-glow fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-gradient-to-br from-cyan to-violet text-2xl shadow-lg transition-transform hover:scale-110"
    >
      ✈️
    </a>
  );
}
