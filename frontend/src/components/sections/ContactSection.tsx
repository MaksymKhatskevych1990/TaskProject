"use client";

import Image from "next/image";
import Link from "next/link";
import { FormEvent, useEffect, useState } from "react";
import { buildTelegramContactUrl, submitContact } from "@/lib/contact";
import { useSiteContent } from "@/components/site-content/SiteContentProvider";
import { NEXT_STEPS } from "@/lib/marketing-pages";
import { formatUaPhone, isPlaceholderPhone, toTelHref } from "@/lib/phone";
import order from "@/image/order.png";

export function ContactSection() {
  const content = useSiteContent();
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
      const matchedPlan = content.pricing.find((item) => item.slug === planParam);
      setPlan(matchedPlan?.name ?? planParam);
    }

    if (needParam) {
      const matchedNeed = content.hero.offers.find((item) => item.id === needParam);
      setNeed(matchedNeed?.label ?? needParam);
    }
  }, [content.hero.offers, content.pricing]);

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

    const telegramUrl = buildTelegramContactUrl(payload, {
      brand: content.brand,
      telegramUsername: content.telegramUsername,
    });

    try {
      await submitContact(payload);
      setSubmitted(true);
      window.setTimeout(() => {
        window.open(telegramUrl, "_blank");
      }, 1200);
    } catch {
      setError(content.contact.errorMessage);
      window.open(telegramUrl, "_blank");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="contact" className="overflow-hidden border-t border-[var(--card-border)] py-20 sm:py-28">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="grid items-end gap-10 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)_minmax(0,0.95fr)] lg:gap-6 xl:gap-10">
          <div className="lg:pb-8">
            <p className="section-number mb-4">08</p>
            <h2 className="editorial-heading text-3xl sm:text-4xl lg:text-[2.75rem]">
              {content.contact.title}
            </h2>
            <p className="mt-4 max-w-sm text-sm leading-relaxed text-muted">
              {content.contact.subtitle}
            </p>

            <div className="mt-10 space-y-3 text-sm">
              {!isPlaceholderPhone(content.phone) ? (
                <a
                  href={toTelHref(content.phone)}
                  className="block text-foreground transition-colors hover:text-accent-bright"
                >
                  {formatUaPhone(content.phone)}
                </a>
              ) : null}
              <a
                href={content.telegramUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="block text-foreground transition-colors hover:text-accent-bright"
              >
                Telegram — @{content.telegramUsername}
              </a>
              <a
                href={`mailto:${content.email}`}
                className="block text-muted transition-colors hover:text-foreground"
              >
                {content.email}
              </a>
            </div>
            <ol className="mt-10 max-w-sm space-y-3 text-sm text-muted">
              {NEXT_STEPS.map((step, index) => (
                <li key={step} className="grid grid-cols-[1.5rem_1fr] gap-2">
                  <span className="font-[family-name:var(--font-jetbrains)] text-xs text-accent">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  {step}
                </li>
              ))}
            </ol>
          </div>

          <div className="relative mx-auto w-full max-w-[420px] lg:max-w-none lg:-mb-8">
            <Image
              src={order}
              alt="Chameleon з брифом проєкту"
              className="h-auto w-full object-contain object-bottom mix-blend-lighten"
              sizes="(max-width: 1024px) 420px, 40vw"
            />
          </div>

          <div className="lg:pb-8">
            {submitted ? (
              <div className="border-l-2 border-accent py-4 pl-6">
                <h3 className="text-xl font-semibold">{content.contact.successTitle}</h3>
                <p className="mt-2 text-sm text-muted">{content.contact.successSubtitle}</p>
                <a
                  href={content.telegramUrl}
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
                    {content.contact.fields.name.label}
                  </label>
                  <input
                    id="name"
                    name="name"
                    required
                    autoComplete="name"
                    className="input-field"
                    placeholder={content.contact.fields.name.placeholder}
                  />
                </div>

                <div>
                  <label htmlFor="phone" className="label-mono mb-2 block">
                    {content.contact.fields.phone.label}
                  </label>
                  <input
                    id="phone"
                    name="phone"
                    required
                    autoComplete="tel"
                    className="input-field"
                    placeholder={content.contact.fields.phone.placeholder}
                  />
                </div>

                <div>
                  <label htmlFor="project" className="label-mono mb-2 block">
                    {content.contact.fields.project.label}
                  </label>
                  <textarea
                    id="project"
                    name="project"
                    required
                    rows={3}
                    className="input-field resize-none"
                    placeholder={content.contact.fields.project.placeholder}
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
                  {loading ? content.contact.submitting : content.contact.submit}
                </button>
                <p className="text-xs leading-relaxed text-muted">
                  Натискаючи кнопку, ви погоджуєтесь з{" "}
                  <Link href="/privacy" className="underline hover:text-foreground">
                    політикою конфіденційності
                  </Link>{" "}
                  і{" "}
                  <Link href="/oferta" className="underline hover:text-foreground">
                    офертою
                  </Link>
                  . Без розсилок.
                </p>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
