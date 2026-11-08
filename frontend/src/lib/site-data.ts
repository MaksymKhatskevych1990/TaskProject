export const SITE = {
  brand: "Chameleon Digital Studio",
  brandShort: "Chameleon",
  domain: "chameleon.digital",
  telegramUrl: "https://t.me/devcraft_studio",
  telegramUsername: "devcraft_studio",
  currency: "₴",
  locale: "uk-UA",
  language: "uk",
  foundingYear: 2020,
  email: "hello@chameleon.digital",
  phone: "+380937090317",
  tagline: "Сайти, магазини, Telegram-боти під ключ",
  description:
    "Розробка сайтів та інтернет-магазинів під ключ: договір, фіксована ціна від 29 000 ₴, живе портфоліо. Відповідаємо в Telegram за 30 хвилин.",
  keywords: [
    "розробка сайтів під ключ",
    "замовити сайт",
    "інтернет-магазин під ключ",
    "створення сайту ціна",
    "SEO просування сайту",
    "контекстна реклама Google Ads",
    "Telegram-бот для бізнесу",
    "розробка CRM на замовлення",
    "веб-студія Україна",
    "розробка сайтів Дніпро",
  ],
  sameAs: ["https://t.me/devcraft_studio"] as const,
} as const;

/** GEO-локації для локального SEO (як на loungelizard.com — кілька офісів у @graph). */
export const GEO_LOCATIONS = [
  {
    id: "dnipro",
    name: "Дніпро",
    label: "Дніпро — віддалений офіс",
    streetAddress: "",
    addressLocality: "Дніпро",
    addressRegion: "Дніпропетровська область",
    postalCode: "49000",
    addressCountry: "UA",
    geo: { latitude: 48.4647, longitude: 35.0462 },
    telephone: "+380937090317",
    isHeadquarters: true,
  },
] as const;

export const SEO = {
  defaultTitle: `${SITE.brand} — ${SITE.tagline}`,
  titleTemplate: `%s — ${SITE.brand}`,
  ogImagePath: "/og-image.png",
  geoRegion: "UA-12",
  geoPlacename: "Dnipro, Ukraine",
  geoPosition: "48.4647;35.0462",
  icbm: "48.4647, 35.0462",
  areaServed: ["Україна", "Дніпро", "Київ", "Львів", "Одеса", "Харків", "Європа"],
  knowsAbout: [
    "Web Design",
    "Web Development",
    "E-commerce",
    "SEO",
    "Telegram Bots",
    "UI/UX Design",
    "Google Ads",
    "Custom CRM",
    "Mobile Apps",
    "Schema.org markup",
    "Local SEO",
    "Answer Engine Optimization",
  ],
  openingHours: {
    days: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    opens: "09:00",
    closes: "18:00",
  },
} as const;

/** Ринкові ціни в гривнях. Тимчасові статичні значення — пізніше підвантаження з API. */
export const MARKET_PRICES = {
  start: 29_000,
  business: 89_000,
  premium: 169_000,
  clientRevenueMln: 2,
} as const;

export function formatPrice(amount: number): string {
  return `${amount.toLocaleString(SITE.locale)} ${SITE.currency}`;
}

export const NAV_LINKS = [
  { href: "/poslugy", label: "Послуги" },
  { href: "/works", label: "Роботи" },
  { href: "/#pricing", label: "Ціни" },
  { href: "/blog", label: "Блог" },
] as const;

export const SECTIONS = {
  services: {
    eyebrow: "Послуги",
    title: "Що ми робимо",
    subtitle:
      "Дизайн, розробка та SEO-фундамент — повний цикл до запуску. Фіксована ціна, живі кейси, договір до старту.",
    also: "Також",
  },
  cases: {
    eyebrow: "Кейси",
    title: "Результати клієнтів",
    subtitle: "Одна схема для кожного кейсу: що було, що стало і який ефект.",
    before: "Було",
    after: "Стало",
    result: "Результат",
  },
  portfolio: {
    eyebrow: "Портфоліо",
    title: "Наші роботи",
    subtitle: "Робочі сайти клієнтів: можна відкрити URL і перевірити, а не дивитись на мокап.",
    viewAll: "Обговорити схожий проєкт",
  },
  process: { eyebrow: "Процес", title: "Як ми працюємо" },
  pricing: {
    eyebrow: "Ціни",
    title: "Прозорі тарифи",
    subtitle: "У гривнях, у договорі. 50% на старті, 50% після здачі. Хостинг і домен — окремо.",
    from: "від",
    choosePlan: "Обрати тариф",
  },
  guarantees: { eyebrow: "Гарантії", title: "Працюємо без ризиків" },
  faq: { eyebrow: "FAQ", title: "Часті запитання" },
} as const;

export const HERO = {
  status: "2 вільні слоти",
  statusMeta: "вересень 2026 · старт можна узгодити цього тижня",
  title: "Розробка сайтів під ключ",
  hint: "Оберіть задачу — одразу побачите термін, склад і ціну. Договір до старту, відповідь у Telegram за 30 хвилин.",
  primaryCta: "Отримати розрахунок",
  secondaryCta: "Живі сайти",
  conditions: [
    "Ціна фіксується в договорі",
    "2 раунди правок у вартості",
    "30 днів підтримки після запуску",
  ],
  chameleon: {
    ariaLabel: "Chameleon Digital Studio — наведи курсор, щоб хамелеон повернув голову",
  },
} as const;

export const HERO_BRIEF = [
  {
    id: "site",
    label: "Сайт",
    duration: "14 днів",
    price: MARKET_PRICES.start,
    plan: "start",
    includes: "Структура, дизайн, верстка, форма заявок, базове SEO, запуск.",
  },
  {
    id: "shop",
    label: "Магазин",
    duration: "3–4 тижні",
    price: MARKET_PRICES.business,
    plan: "business",
    includes: "Каталог, оплата, доставка, CMS, аналітика, запуск під ключ.",
  },
  {
    id: "bot",
    label: "Telegram-бот",
    duration: "3–4 тижні",
    price: MARKET_PRICES.business,
    plan: "business",
    includes: "Сценарії, запис або замовлення, сповіщення, інтеграція з CRM.",
  },
] as const;

export const STATS = [
  { value: 47, suffix: "+", label: "запущених проєктів", decimals: 0 },
  { value: 6, suffix: "+", label: "років на ринку", decimals: 0 },
  { value: 30, suffix: " хв", label: "на відповідь у робочий час", decimals: 0 },
  { value: 30, suffix: " днів", label: "підтримки після запуску", decimals: 0 },
] as const;

export const TESTIMONIALS = [
  {
    name: "Ліза",
    role: "Elvet Group",
    text: "Запустили магазин за 45 днів. Вигляд має фантастичний. Elvet.shop",
    rating: 5,
  },
  {
    name: "Команда RudWood",
    role: "Інтернет-магазин матеріалів",
    text: "Замість замовлень у месенджері з’явився каталог, кошик і робота 24/7. Менеджери більше не збирають позиції руками.",
    rating: 5,
  },
  {
    name: "Нотаріус Надія Корнєєнкова",
    role: "Корпоративний сайт",
    text: "Сайт закриває послуги, запис і довіру ще до дзвінка. Клієнти приходять уже з розумінням, що ми робимо.",
    rating: 5,
  },
] as const;

export const SERVICES = [
  {
    title: "Розробка сайтів",
    description:
      "Лендинги, корпоративні сайти з CMS і посадкові під рекламу — від ідеї до запуску під ключ.",
    features: [
      "Лендинги під заявку з реклами",
      "Корпоративні багатосторінкові сайти",
      "CMS, форми, аналітика",
      "Технічне SEO на старті",
    ],
    featured: true,
  },
  {
    title: "Інтернет-магазини",
    description:
      "Каталог, оплата, доставка й кабінет — B2C і B2B, як RudWood, Elvet Group і Артмагія.",
    features: [
      "Фільтри, картка товару, кошик",
      "Оплата та доставка по Україні",
      "SEO категорій і товарів",
      "Імпорт прайсу та CMS замовлень",
    ],
    featured: true,
  },
  {
    title: "SEO та просування",
    description:
      "Технічне SEO, посадкові під запити й супровід у Google — плюс контекстна реклама, коли органіка ще не тягне.",
    features: [
      "Технічний SEO-аудит",
      "Посадкові, meta, schema, Search Console",
      "Контент під комерційні запити",
      "Google Ads: кампанії та ведення",
    ],
    featured: true,
  },
  {
    title: "UI/UX дизайн",
    description: "Прототип і інтерфейс під розробку — від лендингу до вітрини бренду.",
    featured: false,
  },
  {
    title: "Telegram-боти",
    description:
      "Запис, замовлення, сповіщення та інтеграції — автоматизація бізнес-процесів у месенджері.",
    featured: false,
  },
  {
    title: "Контекстна реклама",
    description: "Google Ads: семантика, оголошення, посадкова й звіт по вартості заявки.",
    featured: false,
  },
  {
    title: "CRM та внутрішні системи",
    description: "Кабінети, склад, статуси й API під ваш процес — не коробка «для всіх».",
    featured: false,
  },
  {
    title: "Мобільні застосунки",
    description: "iOS і Android з одним кодом: кабінет, пошук, пуші до вашого API.",
    featured: false,
  },
] as const;

export const PORTFOLIO = [
  {
    slug: "glow-beauty",
    title: "Glow Beauty",
    category: "E-commerce",
    description: "Інтернет-магазин косметики з каталогом, оплатою та інтеграцією доставки.",
    tags: ["Дизайн", "E-commerce", "SEO"],
    gradient: "from-emerald-900/60 to-emerald-700/30",
    accent: "green",
  },
  {
    slug: "techflow-saas",
    title: "TechFlow SaaS",
    category: "Лендинг",
    description: "Продажний лендинг для B2B SaaS з A/B-тестами та аналітикою конверсій.",
    tags: ["UI/UX", "Розробка", "A/B"],
    gradient: "from-stone-800/60 to-stone-600/30",
    accent: "cyan",
  },
  {
    slug: "salon-pro",
    title: "Salon Pro",
    category: "Telegram-бот",
    description: "Сайт салону краси та Telegram-бот для автозапису і нагадувань.",
    tags: ["Дизайн", "Бот", "CRM"],
    gradient: "from-amber-900/50 to-amber-700/30",
    accent: "orange",
  },
  {
    slug: "legal-partners",
    title: "Legal Partners",
    category: "Корпоративний сайт",
    description: "Багатосторінковий сайт юридичної фірми з CMS та формами заявок.",
    tags: ["Дизайн", "CMS", "SEO"],
    gradient: "from-neutral-800/50 to-neutral-600/30",
    accent: "cyan",
  },
  {
    slug: "fitclub",
    title: "FitClub",
    category: "Лендинг + SEO",
    description: "Лендинг фітнес-клубу з технічним SEO та підключенням Google Analytics.",
    tags: ["Лендинг", "SEO", "Аналітика"],
    gradient: "from-emerald-800/50 to-emerald-600/30",
    accent: "green",
  },
  {
    slug: "coffee-house",
    title: "Coffee House",
    category: "Брендинг + сайт",
    description: "Фірмовий стиль, меню онлайн та система попередніх замовлень.",
    tags: ["UI/UX", "Брендинг", "Розробка"],
    gradient: "from-orange-500/40 to-amber-500/30",
    accent: "orange",
  },
] as const;

export const CASES = [
  {
    category: "E-commerce",
    title: "RudWood",
    before: "Замовлення в месенджері",
    after: "Онлайн-каталог 24/7",
    metric: "+210%",
    metricLabel: "замовлень з сайту",
    description: "Каталог плитних матеріалів, кошик, доставка по Україні.",
  },
  {
    category: "E-commerce",
    title: "Elvet Group",
    before: "Офлайн-продажі",
    after: "Каталог + SEO",
    metric: "+180%",
    metricLabel: "онлайн-заявок",
    description: "Магазин професійної косметики з кабінетом і протоколами.",
  },
  {
    category: "Корпоративний сайт",
    title: "LuxMeb / Форма Studio",
    before: "Заявки з Instagram",
    after: "Органіка + форма",
    metric: "+3.2×",
    metricLabel: "заявок із сайту",
    description: "Преміальний сайт меблів на замовлення з галереєю проєктів.",
  },
] as const;

export const PROCESS_STEPS = [
  {
    step: 1,
    title: "Бриф і аудит",
    description: "Розбираємо задачу, цілі та конкурентів. Фіксуємо KPI та терміни.",
  },
  {
    step: 2,
    title: "Прототип і дизайн",
    description: "Погоджуємо структуру та візуал до початку розробки.",
  },
  {
    step: 3,
    title: "Розробка",
    description: "Пишемо код, підключаємо інтеграції, показуємо проміжні версії.",
  },
  {
    step: 4,
    title: "Тестування",
    description: "Перевіряємо на всіх пристроях, швидкість і безпеку.",
  },
  {
    step: 5,
    title: "Запуск і підтримка",
    description: "Деплой, навчання команди та 30 днів безкоштовної підтримки.",
  },
] as const;

export const PRICING_PLANS = [
  {
    slug: "start",
    name: "Старт",
    price: MARKET_PRICES.start,
    description: "Лендинг або невеликий сайт для швидкого старту.",
    features: [
      "До 5 секцій",
      "Адаптивний дизайн",
      "Форма заявки",
      "Базове SEO",
      "14 днів розробки",
    ],
    highlighted: false,
  },
  {
    slug: "business",
    name: "Бізнес",
    price: MARKET_PRICES.business,
    description: "Повноцінний сайт або магазин з інтеграціями.",
    features: [
      "До 15 сторінок",
      "CMS / адмінка",
      "CRM-інтеграція",
      "Аналітика та A/B",
      "Telegram-сповіщення",
      "30 днів підтримки",
    ],
    highlighted: true,
    badge: "Рекомендуємо",
  },
  {
    slug: "premium",
    name: "Преміум",
    price: MARKET_PRICES.premium,
    description: "Комплексне рішення під ключ з автоматизацією.",
    features: [
      "Без обмежень за обсягом",
      "Telegram-бот",
      "API-інтеграції",
      "Пріоритетна підтримка",
      "Навчання команди",
      "60 днів підтримки",
    ],
    highlighted: false,
  },
] as const;

export const GUARANTEES = [
  {
    title: "Фіксована ціна",
    description: "Вартість фіксується в договорі — без прихованих доплат.",
    image: "price",
  },
  {
    title: "Термін 14 днів",
    description: "Стандартний проєкт запускаємо за два тижні.",
    image: "term",
  },
  {
    title: "Правки включено",
    description: "2 раунди правок за дизайном і функціоналом — безкоштовно.",
    image: "edits",
  },
  {
    title: "30 днів підтримки",
    description: "Виправляємо баги та допомагаємо з запуском після здачі.",
    image: "support",
  },
] as const;

export const FAQ_ITEMS = [
  {
    question: "Скільки коштує сайт під ключ?",
    answer:
      "Лендинг — від 29 000 ₴, сайт або магазин з CMS — від 89 000 ₴, комплекс з ботом і інтеграціями — від 169 000 ₴. Суму фіксуємо в договорі після брифу.",
  },
  {
    question: "Скільки часу займає розробка?",
    answer:
      "Лендинг — від 15 робочих днів. Інтернет-магазин або бот — 3–4 тижні. Точний дедлайн прописуємо в договорі до старту.",
  },
  {
    question: "Чи можна оплатити частинами?",
    answer:
      "Так. 50% на старті, 50% після здачі. Для великих проєктів ділимо оплату по етапах: прототип, розробка, запуск.",
  },
  {
    question: "Що входить у вартість?",
    answer:
      "Дизайн, верстка, програмування, базове SEO, запуск і 30 днів підтримки. Хостинг, домен і платні API (оплата, SMS) — окремо, прозоро в кошторисі.",
  },
  {
    question: "Працюєте не лише з Дніпром?",
    answer:
      "Так, повністю віддалено по Україні та з клієнтами в ЄС. Спілкування в Telegram, демо на тестовому стенді, договір електронно.",
  },
  {
    question: "Що якщо результат не сподобається?",
    answer:
      "Два раунди правок уже в ціні. Якщо після узгодженого прототипу й правок проєкт не приймаєте — повертаємо передоплату за невиконаний обсяг.",
  },
  {
    question: "Хто писатиме код — студія чи підрядники?",
    answer:
      "Проєкт веде студія: один відповідальний, проміжні демо, код і доступи передаємо вам. Не продаємо «години невідомого фрилансера».",
  },
  {
    question: "Чи буде сайт у Google?",
    answer:
      "Так: коректна індексація, sitemap, robots, title/description, швидкість і schema. Просування трафіком — окрема послуга, фундамент входить у розробку.",
  },
] as const;

export const CONTACT = {
  title: "Отримайте розрахунок сьогодні",
  subtitle: "Ім’я та контакт. Відповімо в Telegram протягом 30 хвилин у робочий час — без розсилок і «менеджерів-роботів».",
  successTitle: "Заявку надіслано!",
  successSubtitle: "Перенаправляємо вас у Telegram для продовження діалогу…",
  errorMessage: "Не вдалося надіслати заявку. Спробуйте написати нам у Telegram.",
  fields: {
    name: { label: "Ім'я", placeholder: "Як до вас звертатись?" },
    phone: { label: "Телефон або Telegram", placeholder: "@username або +380..." },
    project: { label: "Про проєкт", placeholder: "Коротко опишіть задачу..." },
    plan: { label: "Тариф" },
  },
  submit: "Отримати розрахунок",
  submitting: "Надсилаємо...",
} as const;

export const FOOTER = {
  rights: "Усі права захищені.",
  telegram: "Telegram",
  writeInTelegram: "Написати в Telegram",
  blog: "Блог",
} as const;

export const BLOG_PAGE = {
  eyebrow: "Блог",
  title: "Корисні матеріали",
  subtitle: "Поради з дизайну, розробки та SEO — від нашої команди.",
  readMore: "Читати далі",
  backToBlog: "← До блогу",
  readTime: "хв читання",
  empty: "Статті з'являться незабаром.",
} as const;

export const HEADER = {
  openMenu: "Відкрити меню",
  closeMenu: "Закрити меню",
  navigation: "Навігація",
} as const;
