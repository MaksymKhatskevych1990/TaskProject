"""Load real portfolio cases with cover and inner-page screenshots."""

from __future__ import annotations

from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from apps.website.choices import PortfolioAccent
from apps.website.models import PortfolioGalleryImage, PortfolioProject

SEED_DIR = Path(__file__).resolve().parents[2] / "seed_media" / "portfolio"

CASES = [
    {
        "slug": "artmagic",
        "legacy_slugs": (),
        "title": "Артмагія",
        "category": "E-commerce",
        "description": (
            "Інтернет-магазин художніх матеріалів: каталог, фільтри, картки товарів, "
            "кошик і доставка по Україні."
        ),
        "tags": ["E-commerce", "Каталог", "Django", "SEO"],
        "accent": PortfolioAccent.ORANGE,
        "gradient": "from-amber-900/40 to-stone-700/30",
        "featured": True,
        "sort_order": 1,
        "metric": "+4.1×",
        "before_label": "Роздріб без каталогу",
        "after_label": "Онлайн-вітрина 15 000+ SKU",
        "case_description": (
            "Зібрали e-commerce для художнього магазину: ієрархія категорій, "
            "фільтри, картка товару з характеристиками, кошик і оплата."
        ),
        "client_url": "",
        "cover": "artmagic.png",
        "gallery": (
            ("artmagic.png", "Головна"),
            ("artmagic-inner.png", "Каталог «Живопис»"),
            ("artmagic-detail.png", "Картка товару"),
        ),
        "status": "published",
    },
    {
        "slug": "luxmeb",
        "legacy_slugs": ("glow-beauty",),
        "title": "LuxMeb",
        "category": "Корпоративний сайт",
        "description": (
            "Преміальний сайт студії інтерʼєру та меблів: hero, вибрані проєкти "
            "і детальні кейси з галереєю етапів."
        ),
        "tags": ["UI/UX", "Next.js", "CMS", "SEO"],
        "accent": PortfolioAccent.ORANGE,
        "gradient": "from-stone-800/60 to-amber-700/30",
        "featured": True,
        "sort_order": 2,
        "metric": "+3.2×",
        "before_label": "Заявки з Instagram",
        "after_label": "Органічний трафік + форма",
        "case_description": (
            "Атмосферний корпоративний сайт: кінематографічний перший екран, "
            "bento-сітка проєктів і модальне портфоліо з етапами виробництва."
        ),
        "client_url": "",
        "cover": "luxmeb.png",
        "gallery": (
            ("luxmeb.png", "Головна"),
            ("luxmeb-inner.png", "Проєкти"),
            ("luxmeb-detail.png", "Деталі проєкту"),
        ),
        "status": "published",
    },
    {
        "slug": "rudwood",
        "legacy_slugs": ("elven", "techflow-saas"),
        "title": "RudWood",
        "category": "E-commerce",
        "description": (
            "Інтернет-магазин плитних матеріалів, фурнітури та меблів: каталог, "
            "пошук, картка товару, кошик і доставка по Дніпру."
        ),
        "tags": ["E-commerce", "Каталог", "Next.js", "CRM"],
        "accent": PortfolioAccent.GREEN,
        "gradient": "from-emerald-900/50 to-stone-700/30",
        "featured": True,
        "sort_order": 3,
        "metric": "+210%",
        "before_label": "Замовлення в месенджері",
        "after_label": "Онлайн-каталог 24/7",
        "case_description": (
            "Повноцінний B2B/B2C storefront: фільтри, наявність, картки товарів "
            "і адміністративний контур під склад."
        ),
        "client_url": "https://rudwood.com.ua/",
        "cover": "rudwood.png",
        "gallery": (
            ("rudwood.png", "Головна"),
            ("rudwood-inner.png", "Каталог меблів"),
            ("rudwood-detail.png", "Картка товару"),
        ),
        "status": "published",
    },
    {
        "slug": "elvet-group",
        "legacy_slugs": ("salon-pro",),
        "title": "Elvet Group",
        "category": "E-commerce",
        "description": (
            "B2B-магазин філерів і естетичної медицини: каталог брендів, "
            "фільтри, картки товарів, кошик і мультивалютність."
        ),
        "tags": ["E-commerce", "Каталог", "Next.js", "B2B"],
        "accent": PortfolioAccent.ORANGE,
        "gradient": "from-stone-800/50 to-amber-800/25",
        "featured": True,
        "sort_order": 4,
        "metric": "+3.8×",
        "before_label": "Прайс у PDF і месенджері",
        "after_label": "Онлайн-каталог для клінік",
        "case_description": (
            "Преміальний e-commerce для дистрибʼютора філерів: вітрина брендів, "
            "фільтри за протоколами, картка SKU з фасовками і B2B-кошик."
        ),
        "client_url": "",
        "cover": "elvet.png",
        "gallery": (
            ("elvet.png", "Головна"),
            ("elvet-inner.png", "Каталог філерів"),
            ("elvet-detail.png", "Картка товару"),
        ),
        "status": "published",
    },
    {
        "slug": "ac-clean",
        "legacy_slugs": (),
        "title": "AS clean",
        "category": "Лендинг",
        "description": (
            "Сайт клінінгової компанії: герой з офером, процес роботи, "
            "форма заявки за 2 хвилини та контакти з картою."
        ),
        "tags": ["Лендинг", "CMS", "Конверсія", "SEO"],
        "accent": PortfolioAccent.CYAN,
        "gradient": "from-sky-900/40 to-slate-800/30",
        "featured": False,
        "sort_order": 5,
        "metric": "+2.4×",
        "before_label": "Заявки лише з телефону",
        "after_label": "Заявки з форми 24/7",
        "case_description": (
            "Конверсійний лендинг для клінінгу: чіткий офер, докази довіри, "
            "покрокова форма замовлення та CMS для самостійного оновлення."
        ),
        "client_url": "",
        "cover": "ac-clean.png",
        "gallery": (
            ("ac-clean.png", "Головна"),
            ("ac-clean-inner.png", "Як ми працюємо"),
            ("ac-clean-detail.png", "Форма заявки"),
        ),
        "status": "published",
    },
]


class Command(BaseCommand):
    """Upsert studio cases with homepage, inner and detail screenshots."""

    help = "Load Artmagic, LuxMeb, RudWood, Elvet Group and AS clean portfolio cards with galleries"

    def handle(self, *args, **options) -> None:
        if not SEED_DIR.exists():
            raise SystemExit(f"Seed media directory missing: {SEED_DIR}")

        for case in CASES:
            project = self._resolve_project(case)
            cover_path = SEED_DIR / case["cover"]
            if not cover_path.exists():
                raise SystemExit(f"Cover missing: {cover_path}")

            for field in (
                "title",
                "category",
                "description",
                "tags",
                "accent",
                "gradient",
                "featured",
                "sort_order",
                "metric",
                "before_label",
                "after_label",
                "case_description",
                "client_url",
                "status",
            ):
                setattr(project, field, case[field])

            project.slug = case["slug"]
            project.save()

            with cover_path.open("rb") as handle:
                project.cover_image.save(cover_path.name, File(handle), save=True)

            project.gallery_images.all().delete()
            for order, (filename, caption) in enumerate(case["gallery"]):
                image_path = SEED_DIR / filename
                if not image_path.exists():
                    raise SystemExit(f"Gallery image missing: {image_path}")
                gallery = PortfolioGalleryImage(
                    project=project,
                    caption=caption,
                    ordering=order,
                )
                with image_path.open("rb") as handle:
                    gallery.image.save(filename, File(handle), save=True)

            self.stdout.write(
                self.style.SUCCESS(f"Updated {project.slug} ← {cover_path.name}")
            )

        keep = [case["slug"] for case in CASES]
        PortfolioProject.objects.exclude(slug__in=keep).update(
            featured=False,
            status="draft",
        )

        self.stdout.write(self.style.SUCCESS("Portfolio cases loaded."))

    def _resolve_project(self, case: dict) -> PortfolioProject:
        project = PortfolioProject.objects.filter(slug=case["slug"]).first()
        if project:
            return project

        for legacy in case.get("legacy_slugs", ()):
            project = PortfolioProject.objects.filter(slug=legacy).first()
            if project:
                return project

        return PortfolioProject(slug=case["slug"])
