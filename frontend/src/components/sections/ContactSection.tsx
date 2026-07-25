"use client";

import { FormEvent, useState } from "react";
import { CONTACT, SITE } from "@/lib/site-data";

export function ContactSection() {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);

    setTimeout(() => {
      setSubmitted(true);
      setLoading(false);

      setTimeout(() => {
        window.open(SITE.telegramUrl, "_blank");
      }, 1500);
    }, 800);
  };

  return (
    <section id="contact" className="relative py-20">
      <div className="glow-orb left-1/2 top-0 h-64 w-64 -translate-x-1/2 bg-violet/20" />

      <div className="relative mx-auto max-w-xl px-4 sm:px-6">
        <div className="mb-8 text-center">
          <h2 className="font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl">
            {CONTACT.title}
          </h2>
          <p className="mt-3 text-sm text-muted">{CONTACT.subtitle}</p>
        </div>

        {submitted ? (
          <div className="rounded-2xl border border-cyan/30 bg-cyan/5 p-8 text-center">
            <span className="text-4xl">✓</span>
            <h3 className="mt-4 font-[family-name:var(--font-exo2)] text-xl font-semibold">
              {CONTACT.successTitle}
            </h3>
            <p className="mt-2 text-sm text-muted">{CONTACT.successSubtitle}</p>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="space-y-4 rounded-2xl border border-white/5 bg-card p-6"
          >
            <div>
              <label htmlFor="name" className="mb-1.5 block text-sm font-medium">
                Имя
              </label>
              <input
                id="name"
                name="name"
                required
                className="w-full rounded-xl border border-white/10 bg-[#070b18] px-4 py-3 text-sm outline-none transition-colors focus:border-cyan/50"
                placeholder="Как к вам обращаться?"
              />
            </div>

            <div>
              <label htmlFor="phone" className="mb-1.5 block text-sm font-medium">
                Телефон или Telegram
              </label>
              <input
                id="phone"
                name="phone"
                required
                className="w-full rounded-xl border border-white/10 bg-[#070b18] px-4 py-3 text-sm outline-none transition-colors focus:border-cyan/50"
                placeholder="@username или +380..."
              />
            </div>

            <div>
              <label htmlFor="project" className="mb-1.5 block text-sm font-medium">
                О проекте
              </label>
              <textarea
                id="project"
                name="project"
                required
                rows={4}
                className="w-full resize-none rounded-xl border border-white/10 bg-[#070b18] px-4 py-3 text-sm outline-none transition-colors focus:border-cyan/50"
                placeholder="Кратко опишите задачу..."
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-full bg-gradient-to-r from-cyan to-violet py-3 text-sm font-semibold text-[#070b18] transition-opacity hover:opacity-90 disabled:opacity-60"
            >
              {loading ? "Отправляем..." : "Отправить заявку"}
            </button>
          </form>
        )}
      </div>
    </section>
  );
}
