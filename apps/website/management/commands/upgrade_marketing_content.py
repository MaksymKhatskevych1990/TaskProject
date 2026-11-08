"""Upgrade public marketing copy, NAP, FAQ, and SEO landing pages."""

from __future__ import annotations

from datetime import datetime
from datetime import timezone as dt_timezone

from django.core.management.base import BaseCommand

from apps.website.cms_seed import _CASES, _FAQ, _SERVICES, _STATS, _TESTIMONIALS
from apps.website.models import (
    BlogCategory,
    BlogPost,
    PortfolioProject,
    SiteCaseStudy,
    SiteFaqItem,
    SiteNavLink,
    SiteOffice,
    SiteSeoSettings,
    SiteService,
    SiteStat,
    SiteTestimonial,
)
from apps.website.seo_defaults import HOME_DESCRIPTION, HOME_TITLE


class Command(BaseCommand):
    """Apply conversion and SEO copy without wiping custom contacts."""

    help = "Refresh landing SEO, trust copy, FAQ, and remove fake office NAP."

    def handle(self, *args, **options) -> None:
        settings, _ = SiteSeoSettings.objects.get_or_create(pk=1)
        self._update_settings(settings)
        self._update_nav(settings)
        self._replace_block(SiteStat, settings, _STATS)
        self._replace_block(SiteTestimonial, settings, _TESTIMONIALS)
        self._replace_block(SiteCaseStudy, settings, _CASES)
        self._replace_block(SiteFaqItem, settings, _FAQ)
        self._replace_block(SiteService, settings, _SERVICES)
        self._fix_offices(settings)
        self._fix_portfolio_urls()
        self._ensure_blog_posts()
        self.stdout.write(self.style.SUCCESS("Marketing content upgraded."))

    def _update_settings(self, settings: SiteSeoSettings) -> None:
        settings.seo_title = HOME_TITLE
        settings.seo_description = HOME_DESCRIPTION
        settings.seo_h1 = "Розробка сайтів під ключ"
        settings.og_title = HOME_TITLE
        settings.og_description = HOME_DESCRIPTION
        settings.focus_keyword = "розробка сайтів під ключ"
        settings.hero_status = "2 вільні слоти"
        settings.hero_status_meta = "вересень 2026 · старт можна узгодити цього тижня"
        settings.hero_title = "Розробка сайтів під ключ"
        settings.hero_hint = (
            "Оберіть задачу — одразу побачите термін, склад і ціну. "
            "Договір до старту, відповідь у Telegram за 30 хвилин."
        )
        settings.hero_primary_cta = "Отримати розрахунок"
        settings.hero_secondary_cta = "Живі сайти"
        settings.hero_conditions = (
            "Ціна фіксується в договорі\n"
            "2 раунди правок у вартості\n"
            "30 днів підтримки після запуску"
        )
        settings.services_subtitle = (
            "Дизайн, розробка та SEO-фундамент — повний цикл до запуску. "
            "Фіксована ціна, живі кейси, договір до старту."
        )
        settings.portfolio_subtitle = (
            "Робочі сайти клієнтів: можна відкрити URL і перевірити, а не дивитись на мокап."
        )
        settings.pricing_subtitle = (
            "У гривнях, у договорі. 50% на старті, 50% після здачі. Хостинг і домен — окремо."
        )
        settings.contact_title = "Отримайте розрахунок сьогодні"
        settings.contact_subtitle = (
            "Ім’я та контакт. Відповімо в Telegram протягом 30 хвилин у робочий час "
            "— без розсилок і «менеджерів-роботів»."
        )
        settings.contact_submit = "Отримати розрахунок"
        settings.footer_about = (
            "Digital-студія з Дніпра. Сайти, магазини й боти під ключ для клієнтів "
            "по Україні та ЄС — повністю онлайн."
        )
        settings.footer_offices_label = "Локація"
        settings.blog_title = "Блог про розробку сайтів — Chameleon Digital Studio"
        settings.blog_description = (
            "Як замовити сайт, скільки коштує магазин і що закласти в SEO до запуску."
        )
        settings.blog_h1 = "Блог про сайти, магазини та SEO"
        settings.tagline = "Сайти, магазини, Telegram-боти під ключ"
        settings.site_description = HOME_DESCRIPTION
        settings.save()

    def _update_nav(self, settings: SiteSeoSettings) -> None:
        SiteNavLink.objects.filter(site=settings, href="/#services").update(href="/poslugy")
        if not SiteNavLink.objects.filter(site=settings, href="/poslugy").exists():
            first = SiteNavLink.objects.filter(site=settings).order_by("ordering").first()
            SiteNavLink.objects.create(
                site=settings,
                href="/poslugy",
                label="Послуги",
                ordering=first.ordering if first else 0,
            )

    def _replace_block(self, model, settings: SiteSeoSettings, rows: list[dict]) -> None:
        model.objects.filter(site=settings).delete()
        seen = set()
        for index, row in enumerate(rows):
            key = tuple(sorted((k, str(v)) for k, v in row.items() if k in {"question", "title", "name", "label"}))
            if key in seen:
                continue
            seen.add(key)
            model.objects.create(site=settings, ordering=index, **row)

    def _fix_offices(self, settings: SiteSeoSettings) -> None:
        SiteOffice.objects.filter(site=settings).exclude(slug="dnipro").delete()
        office, created = SiteOffice.objects.get_or_create(
            site=settings,
            slug="dnipro",
            defaults={
                "name": "Дніпро",
                "label": "Дніпро — віддалений офіс",
                "street_address": "",
                "address_locality": "Дніпро",
                "address_region": "Дніпропетровська область",
                "postal_code": "49000",
                "address_country": "UA",
                "latitude": 48.4647,
                "longitude": 35.0462,
                "telephone": settings.phone or "+380937090317",
                "is_headquarters": True,
                "ordering": 0,
            },
        )
        if not created:
            office.name = "Дніпро"
            office.label = "Дніпро — віддалений офіс"
            office.street_address = ""
            office.address_locality = "Дніпро"
            office.address_region = "Дніпропетровська область"
            office.postal_code = "49000"
            office.latitude = 48.4647
            office.longitude = 35.0462
            office.telephone = settings.phone or office.telephone
            office.is_headquarters = True
            office.save()

    def _fix_portfolio_urls(self) -> None:
        for project in PortfolioProject.objects.all():
            url = (project.client_url or "").strip()
            if "localhost" in url or "127.0.0.1" in url:
                project.client_url = ""
                project.save(update_fields=["client_url"])

    def _ensure_blog_posts(self) -> None:
        category, _ = BlogCategory.objects.get_or_create(
            slug="development",
            defaults={"name": "Розробка", "ordering": 2},
        )
        posts = [
            {
                "slug": "skilky-koshtuie-sait-pid-kliuch",
                "title": "Скільки коштує сайт під ключ у 2026 році",
                "excerpt": (
                    "Реальні вилки по лендингу, корпоративному сайту й магазину: "
                    "що входить у ціну і де бізнес зазвичай переплачує."
                ),
                "published_at": datetime(2026, 9, 10, tzinfo=dt_timezone.utc),
                "read_time_minutes": 8,
                "seo_title": "Скільки коштує сайт під ключ — ціни 2026",
                "seo_h1": "Скільки коштує сайт під ключ",
                "focus_keyword": "скільки коштує сайт",
                "content": "\n\n".join(
                    [
                        "Ціна сайту — не «від 5 000», якщо в комплекті дизайн, верстка, форми, SEO-фундамент і запуск. Нижче — вилки, з якими ми працюємо в Chameleon Digital Studio.",
                        "## Лендинг",
                        "Від 29 000 ₴. До п’яти секцій, адаптив, форма заявки, базове SEO, запуск. Підходить, коли одна послуга і одна дія.",
                        "## Корпоративний сайт або магазин",
                        "Від 89 000 ₴. CMS, кілька сторінок або каталог, аналітика, інтеграції. Це робочий канал продажів, не візитка.",
                        "## Що не входить",
                        "Домен, хостинг, еквайринг, контент-зйомка. Це прописуємо в кошторисі до старту, щоб не було доплат «по ходу».",
                        "## Як не помилитись",
                        "Дивіться живі URL у портфоліо, фіксуйте ціну в договорі, просіть проміжні демо. Якщо потрібен розрахунок під вашу задачу — напишіть у Telegram.",
                    ]
                ),
            },
            {
                "slug": "internet-magazyn-pid-kliuch",
                "title": "Інтернет-магазин під ключ: що має бути в першій версії",
                "excerpt": (
                    "Каталог, кошик, оплата, доставка й SEO-шаблони — мінімум, "
                    "без якого магазин не продає сам."
                ),
                "published_at": datetime(2026, 9, 8, tzinfo=dt_timezone.utc),
                "read_time_minutes": 7,
                "seo_title": "Інтернет-магазин під ключ — що входить",
                "seo_h1": "Інтернет-магазин під ключ",
                "focus_keyword": "інтернет-магазин під ключ",
                "content": "\n\n".join(
                    [
                        "Магазин у месенджері не масштабується: менеджер спить — продажі стоять. Перша версія storefront має закривати покупку без дзвінка.",
                        "## Обов’язковий склад",
                        "Каталог і фільтри, картка товару, кошик, доставка по Україні, оплата, адмінка, сповіщення про замовлення.",
                        "## SEO з першого дня",
                        "ЧПУ категорій, унікальні title, sitemap, розмітка Product. Інакше через пів року доведеться переписувати URL і втрачати індекс.",
                        "## Живі приклади",
                        "У портфоліо — RudWood і Elvet Group. Це не концепції, а сайти з оплатою й каталогом.",
                    ]
                ),
            },
            {
                "slug": "telegram-bot-dlia-biznesu",
                "title": "Telegram-бот для бізнесу: коли він замінює ресепшн",
                "excerpt": (
                    "Запис, замовлення, статуси й CRM. Коли бот окупається, "
                    "а коли дешевше залишити форму на сайті."
                ),
                "published_at": datetime(2026, 9, 5, tzinfo=dt_timezone.utc),
                "read_time_minutes": 6,
                "seo_title": "Telegram-бот для бізнесу — коли замовляти",
                "seo_h1": "Telegram-бот для бізнесу",
                "focus_keyword": "telegram бот для бізнесу",
                "content": "\n\n".join(
                    [
                        "Бот має сенс, якщо одна й та сама розмова повторюється десятки разів на день: слот, наявність, статус замовлення.",
                        "## Що автоматизуємо першим",
                        "Кваліфікація заявки, запис, нагадування, передача в CRM. Не «штучний інтелект заради прези».",
                        "## Сайт усе одно потрібен",
                        "Google не індексує чат. Бот закриває сервіс, сайт — пошук і довіру. Часто робимо обидва в одному договорі.",
                    ]
                ),
            },
        ]
        for payload in posts:
            BlogPost.objects.update_or_create(
                slug=payload["slug"],
                defaults={
                    "title": payload["title"],
                    "excerpt": payload["excerpt"],
                    "content": payload["content"],
                    "category": category,
                    "status": "published",
                    "published_at": payload["published_at"],
                    "read_time_minutes": payload["read_time_minutes"],
                    "seo_title": payload["seo_title"],
                    "seo_h1": payload["seo_h1"],
                    "focus_keyword": payload["focus_keyword"],
                    "seo_description": payload["excerpt"],
                },
            )
