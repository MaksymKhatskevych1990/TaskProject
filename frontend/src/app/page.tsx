import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
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
import { SectionScrollSnap } from "@/components/ui/SectionScrollSnap";
import { SnapSection } from "@/components/ui/SnapSection";

export default function HomePage() {
  return (
    <SectionScrollSnap>
      <Header />
      <main>
        <SnapSection>
          <HeroSection />
        </SnapSection>
        <SnapSection>
          <SocialProofSection />
        </SnapSection>
        <SnapSection>
          <ServicesSection />
        </SnapSection>
        <SnapSection>
          <PortfolioSection />
        </SnapSection>
        <SnapSection>
          <CaseStudiesSection />
        </SnapSection>
        <SnapSection>
          <ProcessSection />
        </SnapSection>
        <SnapSection>
          <PricingSection />
        </SnapSection>
        <SnapSection>
          <GuaranteesSection />
        </SnapSection>
        <SnapSection>
          <FAQSection />
        </SnapSection>
        <SnapSection>
          <ContactSection />
        </SnapSection>
      </main>
      <SnapSection>
        <Footer />
      </SnapSection>
      <FloatingTelegramButton />
    </SectionScrollSnap>
  );
}
