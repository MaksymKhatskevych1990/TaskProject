"""Seed initial portfolio projects."""

from django.db import migrations


def seed_portfolio(apps, schema_editor) -> None:
    """Create starter portfolio content for the marketing site."""
    PortfolioProject = apps.get_model("website", "PortfolioProject")

    projects = [
        {
            "slug": "glow-beauty",
            "title": "Glow Beauty",
            "category": "E-commerce",
            "description": "Інтернет-магазин косметики з каталогом, оплатою та інтеграцією доставки.",
            "tags": ["Дизайн", "E-commerce", "SEO"],
            "gradient": "from-violet/60 to-cyan/40",
            "accent": "violet",
            "featured": True,
            "sort_order": 1,
            "metric": "+640%",
            "before_label": "12 замовлень/міс",
            "after_label": "89 замовлень/міс",
            "case_description": (
                "Повний цикл: UX-дослідження, дизайн каталогу, інтеграція LiqPay та Нової Пошти. "
                "Після запуску налаштували технічне SEO та Google Analytics 4."
            ),
        },
        {
            "slug": "techflow-saas",
            "title": "TechFlow SaaS",
            "category": "Лендинг",
            "description": "Продажний лендинг для B2B SaaS з A/B-тестами та аналітикою конверсій.",
            "tags": ["UI/UX", "Розробка", "A/B"],
            "gradient": "from-cyan/50 to-blue-500/30",
            "accent": "cyan",
            "featured": False,
            "sort_order": 2,
            "metric": "+180%",
            "before_label": "1.2% конверсія",
            "after_label": "3.4% конверсія",
            "case_description": (
                "Створили лендинг з чітким value proposition, соціальним доказом і формою заявки. "
                "Підключили Hotjar та A/B-тести для оптимізації CTA."
            ),
        },
        {
            "slug": "salon-pro",
            "title": "Salon Pro",
            "category": "Telegram-бот",
            "description": "Сайт салону краси та Telegram-бот для автозапису і нагадувань.",
            "tags": ["Дизайн", "Бот", "CRM"],
            "gradient": "from-pink-500/40 to-violet/50",
            "accent": "violet",
            "featured": False,
            "sort_order": 3,
            "metric": "-80%",
            "before_label": "15 дзвінків/день",
            "after_label": "3 дзвінки/день",
            "case_description": (
                "Сайт-візитка + Telegram-бот з автозаписом, нагадуваннями та upsell-послугами. "
                "Адміністратор економить 2 години щодня."
            ),
        },
        {
            "slug": "legal-partners",
            "title": "Legal Partners",
            "category": "Корпоративний сайт",
            "description": "Багатосторінковий сайт юридичної фірми з CMS та формами заявок.",
            "tags": ["Дизайн", "CMS", "SEO"],
            "gradient": "from-slate-500/40 to-cyan/30",
            "accent": "cyan",
            "featured": False,
            "sort_order": 4,
            "metric": "+95%",
            "before_label": "8 заявок/міс",
            "after_label": "16 заявок/міс",
            "case_description": (
                "Корпоративний сайт з CMS для самостійного редагування контенту, "
                "формами заявок та базовим SEO для локального пошуку."
            ),
        },
        {
            "slug": "fitclub",
            "title": "FitClub",
            "category": "Лендинг + SEO",
            "description": "Лендинг фітнес-клубу з технічним SEO та підключенням Google Analytics.",
            "tags": ["Лендинг", "SEO", "Аналітика"],
            "gradient": "from-emerald-500/40 to-cyan/30",
            "accent": "green",
            "featured": False,
            "sort_order": 5,
            "metric": "+420%",
            "before_label": "120 відвід/міс",
            "after_label": "620 відвід/міс",
            "case_description": (
                "Лендинг з оптимізацією Core Web Vitals, schema.org розміткою "
                "та підключенням Search Console для органічного трафіку."
            ),
        },
        {
            "slug": "coffee-house",
            "title": "Coffee House",
            "category": "Брендинг + сайт",
            "description": "Фірмовий стиль, меню онлайн та система попередніх замовлень.",
            "tags": ["UI/UX", "Брендинг", "Розробка"],
            "gradient": "from-orange-500/40 to-amber-500/30",
            "accent": "orange",
            "featured": False,
            "sort_order": 6,
            "metric": "+210%",
            "before_label": "45 замовлень/тиж",
            "after_label": "140 замовлень/тиж",
            "case_description": (
                "Фірмовий стиль, меню онлайн з попереднім замовленням та інтеграцією "
                "з Telegram для сповіщень бариста."
            ),
        },
    ]

    for project in projects:
        PortfolioProject.objects.create(
            title=project["title"],
            slug=project["slug"],
            category=project["category"],
            description=project["description"],
            tags=project["tags"],
            gradient=project["gradient"],
            accent=project["accent"],
            featured=project["featured"],
            sort_order=project["sort_order"],
            metric=project["metric"],
            before_label=project["before_label"],
            after_label=project["after_label"],
            case_description=project["case_description"],
            status="published",
        )


def unseed_portfolio(apps, schema_editor) -> None:
    """Remove seeded portfolio content."""
    PortfolioProject = apps.get_model("website", "PortfolioProject")
    PortfolioProject.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_portfolio_models"),
    ]

    operations = [
        migrations.RunPython(seed_portfolio, unseed_portfolio),
    ]
