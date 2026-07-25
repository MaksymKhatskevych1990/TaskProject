import type { Metadata } from "next";
import { DM_Sans, Exo_2, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const exo2 = Exo_2({
  variable: "--font-exo2",
  subsets: ["latin", "cyrillic"],
  weight: ["400", "600", "700", "800"],
});

const dmSans = DM_Sans({
  variable: "--font-dm-sans",
  subsets: ["latin", "latin-ext"],
  weight: ["400", "500", "600", "700"],
});

const jetbrains = JetBrains_Mono({
  variable: "--font-jetbrains",
  subsets: ["latin", "cyrillic"],
  weight: ["400", "500"],
});

export const metadata: Metadata = {
  title: "Devcraft — IT-студия | Сайты, магазины, Telegram-боты",
  description:
    "Запустим ваш бизнес онлайн за 14 дней. Сайты, интернет-магазины, Telegram-боты и автоматизация под ключ.",
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
