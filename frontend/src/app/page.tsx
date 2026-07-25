import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { CaseStudiesSection } from "@/components/sections/CaseStudiesSection";
import { ContactSection } from "@/components/sections/ContactSection";
import { FAQSection } from "@/components/sections/FAQSection";
import { FloatingTelegramButton } from "@/components/sections/FloatingTelegramButton";
import { GuaranteesSection } from "@/components/sections/GuaranteesSection";
import { HeroSection } from "@/components/sections/HeroSection";
import { PricingSection } from "@/components/sections/PricingSection";
import { ProcessSection } from "@/components/sections/ProcessSection";
import { ServicesSection } from "@/components/sections/ServicesSection";
import { SocialProofSection } from "@/components/sections/SocialProofSection";

export default function HomePage() {
  return (
    <>
      <Header />
      <main>
        <HeroSection />
        <SocialProofSection />
        <ServicesSection />
        <CaseStudiesSection />
        <ProcessSection />
        <PricingSection />
        <GuaranteesSection />
        <FAQSection />
        <ContactSection />
      </main>
      <Footer />
      <FloatingTelegramButton />
    </>
  );
}
