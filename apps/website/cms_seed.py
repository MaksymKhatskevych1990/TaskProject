"""Default landing-page blocks seeded into site settings."""


def seed_site_content(apps=None, schema_editor=None) -> None:
    """Fill the singleton settings row and its blocks when they are empty."""
    if apps is None:
        from django.apps import apps as django_apps

        apps = django_apps
    SiteSeoSettings = apps.get_model("website", "SiteSeoSettings")
    settings, _created = SiteSeoSettings.objects.get_or_create(pk=1)
    _seed_if_empty(apps, "SiteNavLink", settings, _NAV)
    _seed_if_empty(apps, "SiteHeroOffer", settings, _HERO_OFFERS)
    _seed_if_empty(apps, "SiteService", settings, _SERVICES)
    _seed_if_empty(apps, "SiteStat", settings, _STATS)
    _seed_if_empty(apps, "SiteTestimonial", settings, _TESTIMONIALS)
    _seed_if_empty(apps, "SiteCaseStudy", settings, _CASES)
    _seed_if_empty(apps, "SiteProcessStep", settings, _PROCESS)
    _seed_if_empty(apps, "SitePricingPlan", settings, _PRICING)
    _seed_if_empty(apps, "SiteGuarantee", settings, _GUARANTEES)
    _seed_if_empty(apps, "SiteFaqItem", settings, _FAQ)
    _seed_if_empty(apps, "SiteOffice", settings, _OFFICES)


def _seed_if_empty(apps, model_name: str, settings, rows: list[dict]) -> None:
    model = apps.get_model("website", model_name)
    if model.objects.filter(site=settings).exists():
        return
    for index, row in enumerate(rows):
        model.objects.create(site=settings, ordering=index, **row)


_NAV = [
    {"href": "/poslugy", "label": "Послуги"},
    {"href": "/works", "label": "Роботи"},
    {"href": "/#pricing", "label": "Ціни"},
    {"href": "/blog", "label": "Блог"},
]

_HERO_OFFERS = [
    {
        "slug": "site",
        "label": "Сайт",
        "duration": "14 днів",
        "price": 29000,
        "plan": "start",
        "includes": "Структура, дизайн, верстка, форма заявок, базове SEO, запуск.",
    },
    {
        "slug": "shop",
        "label": "Магазин",
        "duration": "3–4 тижні",
        "price": 89000,
        "plan": "business",
        "includes": "Каталог, оплата, доставка, CMS, аналітика, запуск під ключ.",
    },
    {
        "slug": "bot",
        "label": "Telegram-бот",
        "duration": "3–4 тижні",
        "price": 89000,
        "plan": "business",
        "includes": "Сценарії, запис або замовлення, сповіщення, інтеграція з CRM.",
    },
]

_SERVICES = [
    {
        "title": "Розробка сайтів",
        "description": (
            "Лендинги, корпоративні сайти з CMS і посадкові під рекламу — "
            "від ідеї до запуску під ключ."
        ),
        "features": (
            "Лендинги під заявку з реклами\n"
            "Корпоративні багатосторінкові сайти\n"
            "CMS, форми, аналітика\n"
            "Технічне SEO на старті"
        ),
        "featured": True,
    },
    {
        "title": "Інтернет-магазини",
        "description": (
            "Каталог, оплата, доставка й кабінет — B2C і B2B, як RudWood, "
            "Elvet Group і Артмагія."
        ),
        "features": (
            "Фільтри, картка товару, кошик\n"
            "Оплата та доставка по Україні\n"
            "SEO категорій і товарів\n"
            "Імпорт прайсу та CMS замовлень"
        ),
        "featured": True,
    },
    {
        "title": "SEO та просування",
        "description": (
            "Технічне SEO, посадкові під запити й супровід у Google — "
            "плюс контекстна реклама, коли органіка ще не тягне."
        ),
        "features": (
            "Технічний SEO-аудит\n"
            "Посадкові, meta, schema, Search Console\n"
            "Контент під комерційні запити\n"
            "Google Ads: кампанії та ведення"
        ),
        "featured": True,
    },
    {
        "title": "UI/UX дизайн",
        "description": (
            "Прототип і інтерфейс під розробку — від лендингу до вітрини бренду."
        ),
        "features": "",
        "featured": False,
    },
    {
        "title": "Telegram-боти",
        "description": (
            "Запис, замовлення, сповіщення та інтеграції — "
            "автоматизація бізнес-процесів у месенджері."
        ),
        "features": "",
        "featured": False,
    },
    {
        "title": "Контекстна реклама",
        "description": (
            "Google Ads: семантика, оголошення, посадкова й звіт по вартості заявки."
        ),
        "features": "",
        "featured": False,
    },
    {
        "title": "CRM та внутрішні системи",
        "description": (
            "Кабінети, склад, статуси й API під ваш процес — не коробка «для всіх»."
        ),
        "features": "",
        "featured": False,
    },
    {
        "title": "Мобільні застосунки",
        "description": (
            "iOS і Android з одним кодом: кабінет, пошук, пуші до вашого API."
        ),
        "features": "",
        "featured": False,
    },
]

_STATS = [
    {"value": 47, "suffix": "+", "label": "запущених проєктів", "decimals": 0},
    {"value": 6, "suffix": "+", "label": "років на ринку", "decimals": 0},
    {"value": 30, "suffix": " хв", "label": "на відповідь у робочий час", "decimals": 0},
    {"value": 30, "suffix": " днів", "label": "підтримки після запуску", "decimals": 0},
]

_TESTIMONIALS = [
    {
        "name": "Ліза",
        "role": "Elvet Group",
        "text": "Запустили магазин за 45 днів. Вигляд має фантастичний. Elvet.shop",
        "rating": 5,
    },
    {
        "name": "Команда RudWood",
        "role": "Інтернет-магазин матеріалів",
        "text": (
            "Замість замовлень у месенджері з’явився каталог, кошик і робота 24/7. "
            "Менеджери більше не збирають позиції руками."
        ),
        "rating": 5,
    },
    {
        "name": "Нотаріус Надія Корнєєнкова",
        "role": "Корпоративний сайт",
        "text": (
            "Сайт закриває послуги, запис і довіру ще до дзвінка. "
            "Клієнти приходять уже з розумінням, що ми робимо."
        ),
        "rating": 5,
    },
]

_CASES = [
    {
        "category": "E-commerce",
        "title": "RudWood",
        "description": "Каталог плитних матеріалів, кошик, доставка по Україні.",
        "before_value": "Замовлення в месенджері",
        "after_value": "Онлайн-каталог 24/7",
        "metric": "+210%",
        "metric_label": "замовлень з сайту",
    },
    {
        "category": "E-commerce",
        "title": "Elvet Group",
        "description": "Магазин професійної косметики з кабінетом і протоколами.",
        "before_value": "Офлайн-продажі",
        "after_value": "Каталог + SEO",
        "metric": "+180%",
        "metric_label": "онлайн-заявок",
    },
    {
        "category": "Корпоративний сайт",
        "title": "LuxMeb / Форма Studio",
        "description": "Преміальний сайт меблів на замовлення з галереєю проєктів.",
        "before_value": "Заявки з Instagram",
        "after_value": "Органіка + форма",
        "metric": "+3.2×",
        "metric_label": "заявок із сайту",
    },
]

_PROCESS = [
    {
        "title": "Бриф і аудит",
        "description": "Розбираємо задачу, цілі та конкурентів. Фіксуємо KPI та терміни.",
    },
    {
        "title": "Прототип і дизайн",
        "description": "Погоджуємо структуру та візуал до початку розробки.",
    },
    {
        "title": "Розробка",
        "description": "Пишемо код, підключаємо інтеграції, показуємо проміжні версії.",
    },
    {
        "title": "Тестування",
        "description": "Перевіряємо на всіх пристроях, швидкість і безпеку.",
    },
    {
        "title": "Запуск і підтримка",
        "description": "Деплой, навчання команди та 30 днів безкоштовної підтримки.",
    },
]

_PRICING = [
    {
        "slug": "start",
        "name": "Старт",
        "price": 29000,
        "description": "Лендинг або невеликий сайт для швидкого старту.",
        "features": "До 5 секцій\nАдаптивний дизайн\nФорма заявки\nБазове SEO\n14 днів розробки",
        "highlighted": False,
        "badge": "",
    },
    {
        "slug": "business",
        "name": "Бізнес",
        "price": 89000,
        "description": "Повноцінний сайт або магазин з інтеграціями.",
        "features": (
            "До 15 сторінок\nCMS / адмінка\nCRM-інтеграція\nАналітика та A/B\n"
            "Telegram-сповіщення\n30 днів підтримки"
        ),
        "highlighted": True,
        "badge": "Рекомендуємо",
    },
    {
        "slug": "premium",
        "name": "Преміум",
        "price": 169000,
        "description": "Комплексне рішення під ключ з автоматизацією.",
        "features": (
            "Без обмежень за обсягом\nTelegram-бот\nAPI-інтеграції\n"
            "Пріоритетна підтримка\nНавчання команди\n60 днів підтримки"
        ),
        "highlighted": False,
        "badge": "",
    },
]

_GUARANTEES = [
    {
        "title": "Фіксована ціна",
        "description": "Вартість фіксується в договорі — без прихованих доплат.",
        "image_key": "price",
    },
    {
        "title": "Термін 14 днів",
        "description": "Стандартний проєкт запускаємо за два тижні.",
        "image_key": "term",
    },
    {
        "title": "Правки включено",
        "description": "2 раунди правок за дизайном і функціоналом — безкоштовно.",
        "image_key": "edits",
    },
    {
        "title": "30 днів підтримки",
        "description": "Виправляємо баги та допомагаємо з запуском після здачі.",
        "image_key": "support",
    },
]

_FAQ = [
    {
        "question": "Скільки коштує сайт під ключ?",
        "answer": (
            "Лендинг — від 29 000 ₴, сайт або магазин з CMS — від 89 000 ₴, "
            "комплекс з ботом і інтеграціями — від 169 000 ₴. Суму фіксуємо в договорі після брифу."
        ),
    },
    {
        "question": "Скільки часу займає розробка?",
        "answer": (
            "Лендинг — від 15 робочих днів. Інтернет-магазин або бот — 3–4 тижні. "
            "Точний дедлайн прописуємо в договорі до старту."
        ),
    },
    {
        "question": "Чи можна оплатити частинами?",
        "answer": (
            "Так. 50% на старті, 50% після здачі. Для великих проєктів ділимо оплату "
            "по етапах: прототип, розробка, запуск."
        ),
    },
    {
        "question": "Що входить у вартість?",
        "answer": (
            "Дизайн, верстка, програмування, базове SEO, запуск і 30 днів підтримки. "
            "Хостинг, домен і платні API оплачуються окремо, прозоро в кошторисі."
        ),
    },
    {
        "question": "Працюєте не лише з Дніпром?",
        "answer": (
            "Так, повністю віддалено по Україні та з клієнтами в ЄС. "
            "Спілкування в Telegram, демо на тестовому стенді, договір електронно."
        ),
    },
    {
        "question": "Що якщо результат не сподобається?",
        "answer": (
            "Два раунди правок уже в ціні. Якщо після узгодженого прототипу й правок "
            "проєкт не приймаєте — повертаємо передоплату за невиконаний обсяг."
        ),
    },
    {
        "question": "Хто писатиме код — студія чи підрядники?",
        "answer": (
            "Проєкт веде студія: один відповідальний, проміжні демо, код і доступи "
            "передаємо вам. Не продаємо години невідомого фрилансера."
        ),
    },
    {
        "question": "Чи буде сайт у Google?",
        "answer": (
            "Так: індексація, sitemap, robots, title/description, швидкість і schema. "
            "Закупівлю трафіку робимо окремо, фундамент входить у розробку."
        ),
    },
]

_OFFICES = [
    {
        "slug": "dnipro",
        "name": "Дніпро",
        "label": "Дніпро — віддалений офіс",
        "street_address": "",
        "address_locality": "Дніпро",
        "address_region": "Дніпропетровська область",
        "postal_code": "49000",
        "address_country": "UA",
        "latitude": 48.4647,
        "longitude": 35.0462,
        "telephone": "+380937090317",
        "is_headquarters": True,
    },
]
