import type { Metadata } from "next";
import Link from "next/link";
import { MarketingChrome } from "@/components/layout/MarketingChrome";
import { Breadcrumbs } from "@/components/layout/Breadcrumbs";
import { createPageMetadata } from "@/lib/seo/metadata";
import { PRIVACY_PAGE } from "@/lib/marketing-pages";
import { getSiteContent } from "@/lib/site-content";

export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  return createPageMetadata({
    title: PRIVACY_PAGE.seoTitle,
    description: PRIVACY_PAGE.seoDescription,
    path: "/privacy",
    absoluteTitle: true,
  });
}

export default async function PrivacyPage() {
  const content = await getSiteContent();

  return (
    <MarketingChrome>
      <main className="pt-28 pb-20">
        <article className="mx-auto max-w-3xl px-5 sm:px-8">
          <Breadcrumbs
            items={[
              { href: "/", label: "Головна" },
              { href: "/privacy", label: "Конфіденційність" },
            ]}
          />
          <h1 className="editorial-heading mt-10 text-4xl">{PRIVACY_PAGE.h1}</h1>
          <p className="mt-4 text-sm text-muted">
            Оновлено 15 вересня 2026. Контролер даних: {content.brand}, {content.email}.
          </p>
          <div className="mt-10 space-y-8 text-sm leading-relaxed text-muted">
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Що збираємо</h2>
              <p>
                Ім’я, телефон або нік у Telegram і короткий опис задачі — лише якщо ви самі
                надіслали форму або написали нам. Технічні логи (IP, браузер) можуть зберігатись
                коротко для безпеки сайту.
              </p>
            </section>
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Навіщо</h2>
              <p>
                Щоб відповісти на заявку, підготувати кошторис і виконати договір. Не продаємо
                контакти третім особам і не додаємо в рекламні розсилки без окремої згоди.
              </p>
            </section>
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Cookies і аналітика</h2>
              <p>
                Можемо використовувати Google Analytics / Search Console для розуміння, які сторінки
                працюють. Це агреговані дані, не для спаму.
              </p>
            </section>
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Ваші права</h2>
              <p>
                Можете попросити видалити заявку або уточнити дані: напишіть на {content.email} або в{" "}
                <a href={content.telegramUrl} className="text-foreground hover:text-accent-bright">
                  Telegram
                </a>
                . Строк відповіді — до 14 днів.
              </p>
            </section>
            <p>
              Користуючись сайтом і формою, ви підтверджуєте, що ознайомились із цією політикою. Умови
              робіт — у{" "}
              <Link href="/oferta" className="text-foreground hover:text-accent-bright">
                публічній оферті
              </Link>
              .
            </p>
          </div>
        </article>
      </main>
    </MarketingChrome>
  );
}
