import type { Metadata } from "next";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { JsonLd } from "@/components/seo/JsonLd";
import { CaseStudiesSection } from "@/components/sections/CaseStudiesSection";
import { ComparisonSection } from "@/components/sections/ComparisonSection";
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
import { WhyUsSection } from "@/components/sections/WhyUsSection";
import { createPageMetadata } from "@/lib/seo/metadata";
import { buildHomePageGraph, buildSchemaGraph } from "@/lib/seo/schema";
import { getSiteSeo } from "@/lib/seo/site-seo-api";
import { getSiteContent } from "@/lib/site-content";

export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  const siteSeo = await getSiteSeo();
  const seo = siteSeo.seo;
  return createPageMetadata({
    title: seo.title,
    description: seo.description,
    path: "/",
    noIndex: seo.noindex,
    ogImage: seo.ogImage,
    ogTitle: seo.ogTitle,
    ogDescription: seo.ogDescription,
    canonical: seo.canonicalUrl || undefined,
    absoluteTitle: Boolean(seo.title),
    googleVerification: siteSeo.googleSiteVerification,
  });
}

export default async function HomePage() {
  const [siteSeo, content] = await Promise.all([getSiteSeo(), getSiteContent()]);
  const homeSchema = buildSchemaGraph(
    buildHomePageGraph(
      {
        name: siteSeo.seo.title,
        description: siteSeo.seo.description,
      },
      content,
    ),
  );

  return (
    <>
      <JsonLd data={homeSchema} />
      <Header />
      <main>
        <HeroSection heading={siteSeo.seo.h1} />
        <SocialProofSection />
        <WhyUsSection />
        <ServicesSection />
        <PortfolioSection />
        <CaseStudiesSection />
        <ProcessSection />
        <PricingSection />
        <ComparisonSection />
        <GuaranteesSection />
        <FAQSection />
        <ContactSection />
      </main>
      <Footer />
      <FloatingTelegramButton />
    </>
  );
}
