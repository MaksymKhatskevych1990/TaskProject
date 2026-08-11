import type { Metadata } from "next";
import { dmSans, exo2, jetbrains } from "@/app/fonts";
import { SITE } from "@/lib/site-data";
import "./globals.css";

export const metadata: Metadata = {
  title: `${SITE.brand} — IT-студія | Сайти, магазини, Telegram-боти`,
  description:
    "Запустимо ваш бізнес онлайн за 14 днів. Сайти, інтернет-магазини, Telegram-боти та автоматизація під ключ.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="uk" className={`${exo2.variable} ${dmSans.variable} ${jetbrains.variable} h-full`}>
      <body className="dot-grid min-h-full antialiased">{children}</body>
    </html>
  );
}
