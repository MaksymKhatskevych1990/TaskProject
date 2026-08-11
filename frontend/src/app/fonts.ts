import localFont from "next/font/local";

export const exo2 = localFont({
  src: [
    { path: "../fonts/exo-2-latin-400.woff2", weight: "400", style: "normal" },
    { path: "../fonts/exo-2-cyrillic-400.woff2", weight: "400", style: "normal" },
    { path: "../fonts/exo-2-latin-600.woff2", weight: "600", style: "normal" },
    { path: "../fonts/exo-2-cyrillic-600.woff2", weight: "600", style: "normal" },
    { path: "../fonts/exo-2-latin-700.woff2", weight: "700", style: "normal" },
    { path: "../fonts/exo-2-cyrillic-700.woff2", weight: "700", style: "normal" },
    { path: "../fonts/exo-2-latin-800.woff2", weight: "800", style: "normal" },
    { path: "../fonts/exo-2-cyrillic-800.woff2", weight: "800", style: "normal" },
  ],
  variable: "--font-exo2",
  display: "swap",
});

export const dmSans = localFont({
  src: [
    { path: "../fonts/dm-sans-latin-400.woff2", weight: "400", style: "normal" },
    { path: "../fonts/dm-sans-latin-ext-400.woff2", weight: "400", style: "normal" },
    { path: "../fonts/dm-sans-latin-500.woff2", weight: "500", style: "normal" },
    { path: "../fonts/dm-sans-latin-ext-500.woff2", weight: "500", style: "normal" },
    { path: "../fonts/dm-sans-latin-600.woff2", weight: "600", style: "normal" },
    { path: "../fonts/dm-sans-latin-ext-600.woff2", weight: "600", style: "normal" },
    { path: "../fonts/dm-sans-latin-700.woff2", weight: "700", style: "normal" },
    { path: "../fonts/dm-sans-latin-ext-700.woff2", weight: "700", style: "normal" },
  ],
  variable: "--font-dm-sans",
  display: "swap",
});

export const jetbrains = localFont({
  src: [
    { path: "../fonts/jetbrains-mono-latin-400.woff2", weight: "400", style: "normal" },
    { path: "../fonts/jetbrains-mono-cyrillic-400.woff2", weight: "400", style: "normal" },
    { path: "../fonts/jetbrains-mono-latin-500.woff2", weight: "500", style: "normal" },
    { path: "../fonts/jetbrains-mono-cyrillic-500.woff2", weight: "500", style: "normal" },
  ],
  variable: "--font-jetbrains",
  display: "swap",
});
