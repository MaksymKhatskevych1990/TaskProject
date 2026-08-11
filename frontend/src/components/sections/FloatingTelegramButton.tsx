"use client";

import { useEffect, useState } from "react";
import { FOOTER, SITE } from "@/lib/site-data";

export function FloatingTelegramButton() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const onScroll = () => setVisible(window.scrollY > 400);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <a
      href={SITE.telegramUrl}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={FOOTER.writeInTelegram}
      className={`animate-pulse-glow fixed bottom-6 left-6 z-50 flex h-14 w-14 items-center justify-center rounded-xl rounded-tr-none bg-gradient-to-br from-cyan to-violet text-2xl shadow-lg transition-all duration-500 hover:scale-105 ${
        visible
          ? "translate-y-0 scale-100 opacity-100"
          : "pointer-events-none translate-y-4 scale-90 opacity-0"
      }`}
    >
      ✈️
    </a>
  );
}
