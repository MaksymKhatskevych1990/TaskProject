export function toTelHref(phone: string): string {
  const compact = phone.replace(/[^\d+]/g, "");
  return `tel:${compact.startsWith("+") ? compact : `+${compact}`}`;
}

export function formatUaPhone(phone: string): string {
  const digits = phone.replace(/\D/g, "");
  if (digits.length === 12 && digits.startsWith("380")) {
    return `+380 ${digits.slice(3, 5)} ${digits.slice(5, 8)} ${digits.slice(8, 10)} ${digits.slice(10, 12)}`;
  }
  return phone;
}

export function isPlaceholderPhone(phone: string): boolean {
  return /1234567/.test(phone.replace(/\D/g, ""));
}
