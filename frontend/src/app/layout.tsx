import type { Metadata } from "next";
import { dmSans, exo2, jetbrains } from "@/app/fonts";
import { JsonLd } from "@/components/seo/JsonLd";
import { SiteContentProvider } from "@/components/site-content/SiteContentProvider";
import { createPageMetadata } from "@/lib/seo/metadata";
import { buildSchemaGraph, buildWebSiteNode, buildOrganizationNode } from "@/lib/seo/schema";
import { getSiteSeo } from "@/lib/seo/site-seo-api";
import { getSiteContent } from "@/lib/site-content";
import "./globals.css";

export async function generateMetadata(): Promise<Metadata> {
  const siteSeo = await getSiteSeo();
  return createPageMetadata({
    title: siteSeo.seo.title,
    description: siteSeo.seo.description,
    ogImage: siteSeo.seo.ogImage,
    googleVerification: siteSeo.googleSiteVerification,
  });
}

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const content = await getSiteContent();
  const globalSchema = buildSchemaGraph([
    buildOrganizationNode(content),
    buildWebSiteNode(content),
  ]);

  return (
    <html lang="uk" className={`${exo2.variable} ${dmSans.variable} ${jetbrains.variable} h-full`}>
      <body className="min-h-full antialiased">
        <SiteContentProvider value={content}>
          <JsonLd data={globalSchema} />
          {children}
        </SiteContentProvider>
      </body>
    </html>
  );
}
