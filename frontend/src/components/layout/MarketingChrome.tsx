import { Header } from "@/components/layout/Header";
import { Footer } from "@/components/layout/Footer";
import { FloatingTelegramButton } from "@/components/sections/FloatingTelegramButton";

export function MarketingChrome({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Header />
      {children}
      <Footer />
      <FloatingTelegramButton />
    </>
  );
}
