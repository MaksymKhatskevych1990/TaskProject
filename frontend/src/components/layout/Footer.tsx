import { SITE } from "@/lib/site-data";

export function Footer() {
  return (
    <footer className="border-t border-white/5 py-10">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-4 px-4 sm:flex-row sm:px-6">
        <div className="flex items-center gap-2.5">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-cyan to-violet text-sm">
            ⚡
          </span>
          <span className="font-[family-name:var(--font-exo2)] font-bold">
            {SITE.brand}
          </span>
        </div>
        <p className="text-sm text-muted">
          © {new Date().getFullYear()} {SITE.brand}. Все права защищены.
        </p>
        <a
          href={SITE.telegramUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-cyan transition-opacity hover:opacity-80"
        >
          Telegram
        </a>
      </div>
    </footer>
  );
}
