export const SITE = {
  brand: "Devcraft",
  telegramUrl: "https://t.me/devcraft_studio",
  currency: "₴",
  locale: "uk-UA",
} as const;

/** Рыночные цены в гривнах. Временные статические значения — позже подгрузка с API. */
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
  { href: "#services", label: "Услуги" },
  { href: "#cases", label: "Кейсы" },
  { href: "#pricing", label: "Цены" },
  { href: "#faq", label: "FAQ" },
] as const;

export const HERO = {
  badge: "Осталось 2 места в июле — следующий поток в августе",
  title: "Запустим ваш бизнес онлайн",
  titleAccent: "за 14 дней",
  subtitle:
    "Сайты, интернет-магазины, Telegram-боты и автоматизация — под ключ с фиксированной ценой и гарантией результата.",
  primaryCta: "Обсудить проект",
  secondaryCta: "Смотреть кейсы",
} as const;

export const STATS = [
  { value: 47, suffix: "+", label: "запущенных проектов" },
  { value: 98, suffix: "%", label: "довольных клиентов" },
  { value: 4.9, suffix: "★", label: "средний рейтинг", decimals: 1 },
  { value: MARKET_PRICES.clientRevenueMln, suffix: " млн+", label: "выручки клиентов" },
] as const;

export const TESTIMONIALS = [
  {
    name: "Анна К.",
    role: "Основатель интернет-магазина",
    text: "Запустили магазин за 12 дней. Продажи выросли в 3 раза уже в первый месяц.",
    rating: 5,
  },
  {
    name: "Дмитрий М.",
    role: "CEO SaaS-стартапа",
    text: "Чёткий процесс, прозрачные сроки. Лендинг конвертирует лучше, чем ожидали.",
    rating: 5,
  },
  {
    name: "Ольга С.",
    role: "Владелица салона красоты",
    text: "Telegram-бот автоматизировал запись. Экономим 2 часа каждый день.",
    rating: 5,
  },
] as const;

export const SERVICES = [
  {
    title: "Лендинги и сайты",
    description:
      "Продающие страницы и корпоративные сайты с адаптивом, SEO и аналитикой.",
    icon: "🌐",
    glow: "cyan",
  },
  {
    title: "Интернет-магазины",
    description:
      "Каталог, корзина, оплата и CRM — полный цикл e-commerce под ваш бизнес.",
    icon: "🛒",
    glow: "violet",
  },
  {
    title: "Telegram-боты",
    description:
      "Запись, заказы, уведомления и интеграции — автоматизация в мессенджере.",
    icon: "🤖",
    glow: "green",
  },
  {
    title: "Автоматизация",
    description:
      "CRM, таблицы, API и внутренние инструменты — меньше рутины, больше роста.",
    icon: "⚡",
    glow: "orange",
  },
] as const;

export const CASES = [
  {
    title: "E-commerce: рост продаж",
    emoji: "📈",
    before: "12 заказов/мес",
    after: "89 заказов/мес",
    metric: "+640%",
    description: "Интернет-магазин косметики с интеграцией оплаты и доставки.",
  },
  {
    title: "Telegram-бот для салона",
    emoji: "💅",
    before: "15 звонков/день",
    after: "3 звонка/день",
    metric: "-80%",
    description: "Автозапись, напоминания и upsell через бота.",
  },
  {
    title: "Лендинг для SaaS",
    emoji: "🚀",
    before: "1.2% CR",
    after: "4.8% CR",
    metric: "×4",
    description: "Перезапуск лендинга с A/B-тестами и новым позиционированием.",
  },
] as const;

export const PROCESS_STEPS = [
  {
    step: 1,
    title: "Бриф и аудит",
    description: "Разбираем задачу, цели и конкурентов. Фиксируем KPI и сроки.",
  },
  {
    step: 2,
    title: "Прототип и дизайн",
    description: "Согласуем структуру и визуал до начала разработки.",
  },
  {
    step: 3,
    title: "Разработка",
    description: "Пишем код, подключаем интеграции, показываем промежуточные версии.",
  },
  {
    step: 4,
    title: "Тестирование",
    description: "Проверяем на всех устройствах, скорость и безопасность.",
  },
  {
    step: 5,
    title: "Запуск и поддержка",
    description: "Деплой, обучение команды и 30 дней бесплатной поддержки.",
  },
] as const;

export const PRICING_PLANS = [
  {
    name: "Старт",
    price: MARKET_PRICES.start,
    description: "Лендинг или небольшой сайт для быстрого старта.",
    features: [
      "До 5 секций",
      "Адаптивный дизайн",
      "Форма заявки",
      "Базовое SEO",
      "14 дней разработки",
    ],
    highlighted: false,
  },
  {
    name: "Бизнес",
    price: MARKET_PRICES.business,
    description: "Полноценный сайт или магазин с интеграциями.",
    features: [
      "До 15 страниц",
      "CMS / админка",
      "CRM-интеграция",
      "Аналитика и A/B",
      "Telegram-уведомления",
      "30 дней поддержки",
    ],
    highlighted: true,
    badge: "Рекомендуем",
  },
  {
    name: "Премиум",
    price: MARKET_PRICES.premium,
    description: "Комплексное решение под ключ с автоматизацией.",
    features: [
      "Без ограничений по объёму",
      "Telegram-бот",
      "API-интеграции",
      "Приоритетная поддержка",
      "Обучение команды",
      "60 дней поддержки",
    ],
    highlighted: false,
  },
] as const;

export const GUARANTEES = [
  {
    title: "Фиксированная цена",
    description: "Стоимость фиксируется в договоре — без скрытых доплат.",
    icon: "💰",
  },
  {
    title: "Срок 14 дней",
    description: "Стандартный проект запускаем за две недели.",
    icon: "⏱️",
  },
  {
    title: "Правки включены",
    description: "2 раунда правок по дизайну и функционалу — бесплатно.",
    icon: "✏️",
  },
  {
    title: "30 дней поддержки",
    description: "Исправляем баги и помогаем с запуском после сдачи.",
    icon: "🛡️",
  },
] as const;

export const FAQ_ITEMS = [
  {
    question: "Сколько времени занимает разработка?",
    answer:
      "Стандартный лендинг — 14 дней. Интернет-магазин или бот — 3–4 недели. Точные сроки фиксируем после брифа.",
  },
  {
    question: "Можно ли оплатить частями?",
    answer:
      "Да. 50% предоплата при старте, 50% после сдачи проекта. Для крупных проектов — поэтапная оплата.",
  },
  {
    question: "Что входит в стоимость?",
    answer:
      "Дизайн, вёрстка, программирование, базовое SEO, деплой и 30 дней поддержки. Хостинг и домен оплачиваются отдельно.",
  },
  {
    question: "Работаете ли вы с клиентами из других городов?",
    answer:
      "Да, 100% работы удалённо. Общаемся в Telegram, созваниваемся по видеосвязи, показываем промежуточные версии онлайн.",
  },
  {
    question: "Что если результат не понравится?",
    answer:
      "2 раунда правок включены в стоимость. Если после этого не устраивает — возвращаем предоплату.",
  },
] as const;

export const CONTACT = {
  title: "Готовы запустить проект?",
  subtitle: "Оставьте заявку — ответим в Telegram в течение 30 минут.",
  successTitle: "Заявка отправлена!",
  successSubtitle: "Перенаправляем вас в Telegram для продолжения диалога…",
} as const;
