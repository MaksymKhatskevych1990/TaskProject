import type { Metadata } from "next";
import Link from "next/link";
import { MarketingChrome } from "@/components/layout/MarketingChrome";
import { Breadcrumbs } from "@/components/layout/Breadcrumbs";
import { createPageMetadata } from "@/lib/seo/metadata";
import { OFFER_PAGE } from "@/lib/marketing-pages";
import { getSiteContent } from "@/lib/site-content";

export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  return createPageMetadata({
    title: OFFER_PAGE.seoTitle,
    description: OFFER_PAGE.seoDescription,
    path: "/oferta",
    absoluteTitle: true,
  });
}

export default async function OfferPage() {
  const content = await getSiteContent();

  return (
    <MarketingChrome>
      <main className="pt-28 pb-20">
        <article className="mx-auto max-w-3xl px-5 sm:px-8">
          <Breadcrumbs
            items={[
              { href: "/", label: "Головна" },
              { href: "/oferta", label: "Оферта" },
            ]}
          />
          <h1 className="editorial-heading mt-10 text-4xl">{OFFER_PAGE.h1}</h1>
          <p className="mt-4 text-sm text-muted">
            {content.brand}. Заявка з сайту — акцепт оферти на консультацію. Договір на розробку
            підписуємо окремо до старту робіт.
          </p>
          <div className="mt-10 space-y-8 text-sm leading-relaxed text-muted">
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Предмет</h2>
              <p>
                Розробка сайтів, інтернет-магазинів, Telegram-ботів та супутніх інтеграцій за
                погодженим брифом. Публічні тарифи на сайті — орієнтир «від», не рахунок.
              </p>
            </section>
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Оплата</h2>
              <p>
                50% передоплата після підписання договору, 50% після здачі на тестовому стенді.
                Великі проєкти можна розбити по етапах. Хостинг, домен і комісії платіжних систем
                клієнт оплачує окремо, якщо інше не зазначено в додатку.
              </p>
            </section>
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Терміни і правки</h2>
              <p>
                Термін фіксуємо в договорі. У вартість входять 2 раунди правок у межах узгодженого
                прототипу. Нові розділи й інтеграції — додаткова угода.
              </p>
            </section>
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Підтримка і гарантія</h2>
              <p>
                30 днів після запуску виправляємо помилки, що виникли з нашої вини. Зміни контенту й
                нові функції після цього — за окремим запитом.
              </p>
            </section>
            <section>
              <h2 className="mb-3 text-lg font-semibold text-foreground">Відмова</h2>
              <p>
                Якщо після узгодженого прототипу й двох раундів правок ви не приймаєте результат —
                повертаємо оплату за невиконаний обсяг. Виконана й прийнята робота не повертається.
              </p>
            </section>
            <p>
              Персональні дані — за{" "}
              <Link href="/privacy" className="text-foreground hover:text-accent-bright">
                політикою конфіденційності
              </Link>
              . Контакт: {content.email}, Telegram @{content.telegramUsername}.
            </p>
          </div>
        </article>
      </main>
    </MarketingChrome>
  );
}
