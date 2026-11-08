import type { SiteOffice } from "@/lib/site-content";
import { isPlaceholderPhone } from "@/lib/phone";

function haystack(office: SiteOffice): string {
  return `${office.streetAddress} ${office.addressLocality} ${office.postalCode}`.toLowerCase();
}

export function isCredibleOffice(office: SiteOffice): boolean {
  const text = haystack(office);
  const street = office.streetAddress.toLowerCase();
  const city = office.addressLocality.toLowerCase();
  if (isPlaceholderPhone(office.telephone)) return false;
  if (street.includes("хрещатик") && !city.includes("київ") && !city.includes("kyiv")) {
    return false;
  }
  if (office.postalCode === "01001" && city.includes("дніпр")) return false;
  if (text.includes("1234567")) return false;
  return Boolean(office.addressLocality);
}

export function isRemoteOffice(office: SiteOffice): boolean {
  if (!office.streetAddress.trim()) return true;
  return !isCredibleOffice(office);
}
