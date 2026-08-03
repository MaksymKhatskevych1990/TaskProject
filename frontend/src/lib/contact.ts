import { SITE } from "@/lib/site-data";

export type ContactPayload = {
  name: string;
  phone: string;
  project: string;
  plan?: string;
};

export function buildTelegramContactUrl(payload: ContactPayload): string {
  const lines = [
    "Нова заявка з сайту Devcraft",
    "",
    `Ім'я: ${payload.name}`,
    `Контакт: ${payload.phone}`,
    payload.plan ? `Тариф: ${payload.plan}` : null,
    "",
    `Опис: ${payload.project}`,
  ].filter(Boolean);

  const text = encodeURIComponent(lines.join("\n"));
  return `https://t.me/${SITE.telegramUsername}?text=${text}`;
}

export async function submitContact(payload: ContactPayload): Promise<void> {
  const response = await fetch("/api/contact", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Contact submission failed");
  }
}
