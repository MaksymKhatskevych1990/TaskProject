"use client";

import { FormEvent, useEffect, useState } from "react";
import { buildTelegramContactUrl, submitContact } from "@/lib/contact";
import { CONTACT, PRICING_PLANS, SITE } from "@/lib/site-data";

export function ContactSection() {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [plan, setPlan] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const planParam = params.get("plan");
    if (!planParam) return;

    const matchedPlan = PRICING_PLANS.find((item) => item.slug === planParam);
    setPlan(matchedPlan?.name ?? planParam);
  }, []);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData(event.currentTarget);
    const payload = {
      name: String(formData.get("name") ?? "").trim(),
      phone: String(formData.get("phone") ?? "").trim(),
      project: String(formData.get("project") ?? "").trim(),
      plan: plan || undefined,
    };

    const telegramUrl = buildTelegramContactUrl(payload);

    try {
      await submitContact(payload);
      setSubmitted(true);
      window.setTimeout(() => {
        window.open(telegramUrl, "_blank");
      }, 1200);
    } catch {
      setError(CONTACT.errorMessage);
      window.open(telegramUrl, "_blank");
    } finally {
      setLoading(false);
    }
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
            <a
              href={SITE.telegramUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-6 inline-flex rounded-full border border-cyan/30 px-5 py-2 text-sm font-medium text-cyan transition-colors hover:bg-cyan/10"
            >
              {SITE.brand} Telegram
            </a>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            data-snap-ignore
            className="space-y-4 rounded-2xl border border-white/5 bg-card p-6"
          >
            {plan && (
              <div className="rounded-xl border border-cyan/20 bg-cyan/5 px-4 py-3 text-sm">
                <span className="text-muted">{CONTACT.fields.plan.label}: </span>
                <span className="font-medium text-cyan">{plan}</span>
              </div>
            )}

            <div>
              <label htmlFor="name" className="mb-1.5 block text-sm font-medium">
                {CONTACT.fields.name.label}
              </label>
              <input
                id="name"
                name="name"
                required
                autoComplete="name"
                className="w-full rounded-xl border border-white/10 bg-[#070b18] px-4 py-3 text-sm outline-none transition-colors focus:border-cyan/50"
                placeholder={CONTACT.fields.name.placeholder}
              />
            </div>

            <div>
              <label htmlFor="phone" className="mb-1.5 block text-sm font-medium">
                {CONTACT.fields.phone.label}
              </label>
              <input
                id="phone"
                name="phone"
                required
                autoComplete="tel"
                className="w-full rounded-xl border border-white/10 bg-[#070b18] px-4 py-3 text-sm outline-none transition-colors focus:border-cyan/50"
                placeholder={CONTACT.fields.phone.placeholder}
              />
            </div>

            <div>
              <label htmlFor="project" className="mb-1.5 block text-sm font-medium">
                {CONTACT.fields.project.label}
              </label>
              <textarea
                id="project"
                name="project"
                required
                rows={4}
                className="w-full resize-none rounded-xl border border-white/10 bg-[#070b18] px-4 py-3 text-sm outline-none transition-colors focus:border-cyan/50"
                placeholder={CONTACT.fields.project.placeholder}
              />
            </div>

            {error && (
              <p className="rounded-xl border border-red-400/30 bg-red-400/5 px-4 py-3 text-sm text-red-300">
                {error}
              </p>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-full bg-gradient-to-r from-cyan to-violet py-3 text-sm font-semibold text-[#070b18] transition-opacity hover:opacity-90 disabled:opacity-60"
            >
              {loading ? CONTACT.submitting : CONTACT.submit}
            </button>
          </form>
        )}
      </div>
    </section>
  );
}
