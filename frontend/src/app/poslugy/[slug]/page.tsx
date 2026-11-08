import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ServicePageView } from "@/components/site-content/ServicePageView";
import { getServicePage, SERVICE_PAGES } from "@/lib/marketing-pages";
import { createPageMetadata } from "@/lib/seo/metadata";

export const dynamic = "force-dynamic";

export function generateStaticParams() {
  return SERVICE_PAGES.map((page) => ({ slug: page.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const page = getServicePage(slug);
  if (!page) return { title: "Послугу не знайдено" };
  return createPageMetadata({
    title: page.seoTitle,
    description: page.seoDescription,
    path: page.href,
    absoluteTitle: true,
  });
}

export default async function ServiceSlugPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const page = getServicePage(slug);
  if (!page) notFound();
  return <ServicePageView page={page} />;
}
