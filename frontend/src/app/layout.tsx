import type { Metadata } from "next";
import { dmSans, exo2, jetbrains } from "@/app/fonts";
import { JsonLd } from "@/components/seo/JsonLd";
import { createPageMetadata } from "@/lib/seo/metadata";
import { buildSchemaGraph, buildWebSiteNode, buildOrganizationNode } from "@/lib/seo/schema";
import "./globals.css";

export const metadata: Metadata = createPageMetadata();

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const globalSchema = buildSchemaGraph([buildOrganizationNode(), buildWebSiteNode()]);

  return (
    <html lang="uk" className={`${exo2.variable} ${dmSans.variable} ${jetbrains.variable} h-full`}>
      <body className="dot-grid min-h-full antialiased">
        <JsonLd data={globalSchema} />
        {children}
      </body>
    </html>
  );
}
