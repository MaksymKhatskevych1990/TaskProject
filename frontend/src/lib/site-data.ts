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
  phone: "+380441234567",
  tagline: "IT-студія | Сайти, магазини, Telegram-боти",
  description:
    "Запустимо ваш бізнес онлайн за 14 днів. Сайти, інтернет-магазини, Telegram-боти та автоматизація під ключ.",
  keywords: [
    "веб-студія Україна",
    "розробка сайтів",
    "інтернет-магазин під ключ",
    "Telegram-боти",
    "UI/UX дизайн",
    "SEO просування",
    "digital агенція Київ",
  ],
  sameAs: ["https://t.me/devcraft_studio"] as const,
} as const;

/** GEO-локації для локального SEO (як на loungelizard.com — кілька офісів у @graph). */
export const GEO_LOCATIONS = [
  {
    id: "kyiv",
    name: "Київ",
    label: "Kyiv — головний офіс",
    streetAddress: "вул. Хрещатик, 22",
    addressLocality: "Київ",
    addressRegion: "м. Київ",
    postalCode: "01001",
    addressCountry: "UA",
    geo: { latitude: 50.4501, longitude: 30.5234 },
    telephone: "+380441234567",
    isHeadquarters: true,
  },
  {
    id: "lviv",
    name: "Львів",
    label: "Lviv",
    streetAddress: "просп. Свободи, 7",
    addressLocality: "Львів",
    addressRegion: "Львівська область",
    postalCode: "79000",
    addressCountry: "UA",
    geo: { latitude: 49.8397, longitude: 24.0297 },
    telephone: "+380321234567",
    isHeadquarters: false,
  },
  {
    id: "odesa",
    name: "Одеса",
    label: "Odesa",
    streetAddress: "вул. Дерибасівська, 16",
    addressLocality: "Одеса",
    addressRegion: "Одеська область",
    postalCode: "65000",
    addressCountry: "UA",
    geo: { latitude: 46.4825, longitude: 30.7233 },
    telephone: "+380481234567",
    isHeadquarters: false,
  },
  {
    id: "kharkiv",
    name: "Харків",
    label: "Kharkiv",
    streetAddress: "просп. Науки, 27",
    addressLocality: "Харків",
    addressRegion: "Харківська область",
    postalCode: "61000",
    addressCountry: "UA",
    geo: { latitude: 49.9935, longitude: 36.2304 },
    telephone: "+380571234567",
    isHeadquarters: false,
  },
] as const;

export const SEO = {
  defaultTitle: `${SITE.brand} — ${SITE.tagline}`,
  titleTemplate: `%s — ${SITE.brand}`,
  ogImagePath: "/og-image.png",
  geoRegion: "UA-30",
  geoPlacename: "Kyiv, Ukraine",
  geoPosition: "50.4501;30.5234",
  icbm: "50.4501, 30.5234",
  areaServed: ["Україна", "Київ", "Львів", "Одеса", "Харків", "Європа"],
  knowsAbout: [
    "Web Design",
    "Web Development",
    "E-commerce",
    "SEO",
    "Telegram Bots",
    "UI/UX Design",
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
  { href: "/#services", label: "Послуги" },
  { href: "/#portfolio", label: "Роботи" },
  { href: "/#pricing", label: "Ціни" },
  { href: "/blog", label: "Блог" },
] as const;

export const SECTIONS = {
  services: {
    eyebrow: "Послуги",
    title: "Що ми робимо",
    subtitle:
      "Дизайн, розробка та просування — три напрямки, які закривають повний цикл вашого digital-проєкту.",
    also: "Також",
  },
  cases: { eyebrow: "Кейси", title: "Результати клієнтів", before: "Було", after: "Стало" },
  portfolio: {
    eyebrow: "Портфоліо",
    title: "Наші роботи",
    subtitle: "Реальні проєкти — від дизайну та лендингів до інтернет-магазинів і SEO.",
    viewAll: "Обговорити схожий проєкт",
  },
  process: { eyebrow: "Процес", title: "Як ми працюємо" },
  pricing: {
    eyebrow: "Ціни",
    title: "Прозорі тарифи",
    subtitle: "Усі ціни вказані в гривнях. Фіксуємо вартість у договорі.",
    from: "від",
    choosePlan: "Обрати тариф",
  },
  guarantees: { eyebrow: "Гарантії", title: "Працюємо без ризиків" },
  faq: { eyebrow: "FAQ", title: "Часті запитання" },
} as const;

export const HERO = {
  status: "2 вільні слоти",
  statusMeta: "серпень · наступний потік — вересень",
  title: "Що запускаємо?",
  hint: "Оберіть задачу — одразу побачите термін, склад і ціну.",
  primaryCta: "Забронювати слот",
  secondaryCta: "Роботи",
  conditions: [
    "Ціна фіксується в договорі",
    "2 раунди правок",
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
  { value: 47, suffix: "+", label: "запущених проєктів" },
  { value: 98, suffix: "%", label: "задоволених клієнтів" },
  { value: 4.9, suffix: "★", label: "середній рейтинг", decimals: 1 },
  { value: MARKET_PRICES.clientRevenueMln, suffix: " млн+", label: "виручки клієнтів" },
] as const;

export const TESTIMONIALS = [
  {
    name: "Анна К.",
    role: "Засновниця інтернет-магазину",
    text: "Запустили магазин за 12 днів. Продажі зросли в 3 рази вже в перший місяць.",
    rating: 5,
  },
  {
    name: "Дмитро М.",
    role: "CEO SaaS-стартапу",
    text: "Чіткий процес, прозорі терміни. Лендинг конвертує краще, ніж очікували.",
    rating: 5,
  },
  {
    name: "Ольга С.",
    role: "Власниця салону краси",
    text: "Telegram-бот автоматизував запис. Економимо 2 години щодня.",
    rating: 5,
  },
] as const;

export const SERVICES = [
  {
    title: "UI/UX дизайн",
    description:
      "Проєктуємо інтерфейси будь-якої складності — від лендингу до багатосторінкових платформ і web-додатків.",
    features: [
      "Wireframes та інтерактивні прототипи",
      "UI-kit і дизайн-система у Figma",
      "Mobile-first адаптив",
      "Анімації та мікровзаємодії",
    ],
    featured: true,
  },
  {
    title: "Розробка сайтів",
    description:
      "Лендинги, корпоративні сайти та інтернет-магазини — від ідеї до запуску під ключ.",
    features: [
      "Лендинги та promo-сторінки",
      "Корпоративні багатосторінкові сайти",
      "Інтернет-магазини з оплатою та доставкою",
      "CMS, CRM та API-інтеграції",
    ],
    featured: true,
  },
  {
    title: "SEO та просування",
    description:
      "Налаштовуємо видимість у Google та аналітику — щоб клієнтів було більше, а результат — вимірюваним.",
    features: [
      "Технічний SEO-аудит",
      "Meta-теги та семантична розмітка",
      "Оптимізація швидкості (Core Web Vitals)",
      "Google Analytics і Search Console",
    ],
    featured: true,
  },
  {
    title: "Telegram-боти",
    description:
      "Запис, замовлення, сповіщення та інтеграції — автоматизація бізнес-процесів у месенджері.",
    featured: false,
  },
  {
    title: "Автоматизація",
    description:
      "CRM, таблиці, API та внутрішні інструменти — менше рутини, більше зростання.",
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
    title: "E-commerce: зростання продажів",
    emoji: "📈",
    before: "12 замовлень/міс",
    after: "89 замовлень/міс",
    metric: "+640%",
    description: "Інтернет-магазин косметики з інтеграцією оплати та доставки.",
  },
  {
    title: "Telegram-бот для салону",
    emoji: "💅",
    before: "15 дзвінків/день",
    after: "3 дзвінки/день",
    metric: "-80%",
    description: "Автозапис, нагадування та upsell через бота.",
  },
  {
    title: "Лендинг для SaaS",
    emoji: "🚀",
    before: "1.2% CR",
    after: "4.8% CR",
    metric: "×4",
    description: "Перезапуск лендингу з A/B-тестами та новим позиціонуванням.",
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
  },
  {
    title: "Термін 14 днів",
    description: "Стандартний проєкт запускаємо за два тижні.",
  },
  {
    title: "Правки включено",
    description: "2 раунди правок за дизайном і функціоналом — безкоштовно.",
  },
  {
    title: "30 днів підтримки",
    description: "Виправляємо баги та допомагаємо з запуском після здачі.",
  },
] as const;

export const FAQ_ITEMS = [
  {
    question: "Скільки часу займає розробка?",
    answer:
      "Стандартний лендинг — 14 днів. Інтернет-магазин або бот — 3–4 тижні. Точні терміни фіксуємо після брифу.",
  },
  {
    question: "Чи можна оплатити частинами?",
    answer:
      "Так. 50% передоплата на старті, 50% після здачі проєкту. Для великих проєктів — поетапна оплата.",
  },
  {
    question: "Що входить у вартість?",
    answer:
      "Дизайн, верстка, програмування, базове SEO, деплой і 30 днів підтримки. Хостинг і домен оплачуються окремо.",
  },
  {
    question: "Чи працюєте з клієнтами з інших міст?",
    answer:
      "Так, 100% роботи віддалено. Спілкуємось у Telegram, зустрічаємось по відеозв'язку, показуємо проміжні версії онлайн.",
  },
  {
    question: "Що якщо результат не сподобається?",
    answer:
      "2 раунди правок включено у вартість. Якщо після цього не влаштовує — повертаємо передоплату.",
  },
] as const;

export const CONTACT = {
  title: "Готові запустити проєкт?",
  subtitle: "Залиште заявку — відповімо в Telegram протягом 30 хвилин.",
  successTitle: "Заявку надіслано!",
  successSubtitle: "Перенаправляємо вас у Telegram для продовження діалогу…",
  errorMessage: "Не вдалося надіслати заявку. Спробуйте написати нам у Telegram.",
  fields: {
    name: { label: "Ім'я", placeholder: "Як до вас звертатись?" },
    phone: { label: "Телефон або Telegram", placeholder: "@username або +380..." },
    project: { label: "Про проєкт", placeholder: "Коротко опишіть задачу..." },
    plan: { label: "Тариф" },
  },
  submit: "Надіслати заявку",
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
