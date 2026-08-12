"use client";

import { FormEvent, useEffect, useState } from "react";
import { buildTelegramContactUrl, submitContact } from "@/lib/contact";
import { CONTACT, HERO_BRIEF, PRICING_PLANS, SITE } from "@/lib/site-data";

export function ContactSection() {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [plan, setPlan] = useState("");
  const [need, setNeed] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const planParam = params.get("plan");
    const needParam = params.get("need");

    if (planParam) {
      const matchedPlan = PRICING_PLANS.find((item) => item.slug === planParam);
      setPlan(matchedPlan?.name ?? planParam);
    }

    if (needParam) {
      const matchedNeed = HERO_BRIEF.find((item) => item.id === needParam);
      setNeed(matchedNeed?.label ?? needParam);
    }
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
      plan: [need, plan].filter(Boolean).join(" · ") || undefined,
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
    <section id="contact" className="border-t border-[var(--card-border)] bg-[var(--card)] py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="grid gap-16 lg:grid-cols-2 lg:gap-24">
          <div>
            <p className="section-number mb-4">08</p>
            <h2 className="editorial-heading text-3xl sm:text-4xl">
              {CONTACT.title}
            </h2>
            <p className="mt-4 max-w-sm text-sm leading-relaxed text-muted">
              {CONTACT.subtitle}
            </p>

            <div className="mt-12 space-y-4 text-sm">
              <a
                href={SITE.telegramUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="block text-foreground transition-colors hover:text-accent-bright"
              >
                Telegram — @{SITE.telegramUsername}
              </a>
              <a
                href={`mailto:${SITE.email}`}
                className="block text-muted transition-colors hover:text-foreground"
              >
                {SITE.email}
              </a>
            </div>
          </div>

          <div>
            {submitted ? (
              <div className="border-l-2 border-accent py-4 pl-6">
                <h3 className="text-xl font-semibold">{CONTACT.successTitle}</h3>
                <p className="mt-2 text-sm text-muted">{CONTACT.successSubtitle}</p>
                <a
                  href={SITE.telegramUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-ghost mt-6"
                >
                  Відкрити Telegram
                </a>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-8">
                {(need || plan) && (
                  <p className="text-sm">
                    <span className="text-muted">Запит: </span>
                    <span className="font-medium accent-text">
                      {[need, plan].filter(Boolean).join(" · ")}
                    </span>
                  </p>
                )}

                <div>
                  <label htmlFor="name" className="label-mono mb-2 block">
                    {CONTACT.fields.name.label}
                  </label>
                  <input
                    id="name"
                    name="name"
                    required
                    autoComplete="name"
                    className="input-field"
                    placeholder={CONTACT.fields.name.placeholder}
                  />
                </div>

                <div>
                  <label htmlFor="phone" className="label-mono mb-2 block">
                    {CONTACT.fields.phone.label}
                  </label>
                  <input
                    id="phone"
                    name="phone"
                    required
                    autoComplete="tel"
                    className="input-field"
                    placeholder={CONTACT.fields.phone.placeholder}
                  />
                </div>

                <div>
                  <label htmlFor="project" className="label-mono mb-2 block">
                    {CONTACT.fields.project.label}
                  </label>
                  <textarea
                    id="project"
                    name="project"
                    required
                    rows={3}
                    className="input-field resize-none"
                    placeholder={CONTACT.fields.project.placeholder}
                  />
                </div>

                {error && (
                  <p className="text-sm text-red-400">{error}</p>
                )}

                <button
                  type="submit"
                  disabled={loading}
                  className="btn-primary w-full py-3.5 disabled:opacity-60 sm:w-auto"
                >
                  {loading ? CONTACT.submitting : CONTACT.submit}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
