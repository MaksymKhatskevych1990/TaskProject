import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { JsonLd } from "@/components/seo/JsonLd";
import { CaseStudiesSection } from "@/components/sections/CaseStudiesSection";
import { ContactSection } from "@/components/sections/ContactSection";
import { FAQSection } from "@/components/sections/FAQSection";
import { FloatingTelegramButton } from "@/components/sections/FloatingTelegramButton";
import { GuaranteesSection } from "@/components/sections/GuaranteesSection";
import { HeroSection } from "@/components/sections/HeroSection";
import { PortfolioSection } from "@/components/sections/PortfolioSection";
import { PricingSection } from "@/components/sections/PricingSection";
import { ProcessSection } from "@/components/sections/ProcessSection";
import { ServicesSection } from "@/components/sections/ServicesSection";
import { SocialProofSection } from "@/components/sections/SocialProofSection";
import { buildHomePageGraph, buildSchemaGraph } from "@/lib/seo/schema";

export default function HomePage() {
  const homeSchema = buildSchemaGraph(buildHomePageGraph());

  return (
    <>
      <JsonLd data={homeSchema} />
      <Header />
      <main>
        <HeroSection />
        <SocialProofSection />
        <ServicesSection />
        <PortfolioSection />
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
