import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { FloatingTelegramButton } from "@/components/sections/FloatingTelegramButton";
import { ArticleContent } from "@/components/blog/ArticleContent";
import { JsonLd } from "@/components/seo/JsonLd";
import { formatBlogDate, getBlogPost } from "@/lib/blog-api";
import { createPageMetadata } from "@/lib/seo/metadata";
import { buildBlogPostGraph, buildSchemaGraph } from "@/lib/seo/schema";
import { BLOG_PAGE } from "@/lib/site-data";
import { cn } from "@/lib/utils";

const categoryColors: Record<string, string> = {
  SEO: "border-accent/30 text-accent-bright",
  Розробка: "border-accent-warm/30 text-accent-warm-bright",
  Дизайн: "border-[var(--card-border)] text-foreground",
  "E-commerce": "border-accent-warm/30 text-accent-warm-bright",
};

export const dynamic = "force-dynamic";

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const post = await getBlogPost(slug);
  if (!post) return { title: "Стаття не знайдена" };

  return createPageMetadata({
    title: post.title,
    description: post.excerpt,
    path: `/blog/${post.slug}`,
    type: "article",
    publishedTime: post.date,
  });
}

export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getBlogPost(slug);
  if (!post) notFound();

  const articleSchema = buildSchemaGraph(buildBlogPostGraph(post));

  return (
    <>
      <JsonLd data={articleSchema} />
      <Header />
      <main className="pt-28 pb-20">
        <article className="mx-auto max-w-3xl px-5 sm:px-8">
          <Link
            href="/blog"
            className="label-mono inline-flex transition-colors hover:text-foreground"
          >
            {BLOG_PAGE.backToBlog}
          </Link>

          <header className="mt-8">
            <div className="flex flex-wrap items-center gap-3">
              <span
                className={cn(
                  "border px-2 py-0.5 text-[11px] font-medium",
                  categoryColors[post.category] ?? "border-[var(--card-border)] text-muted",
                )}
              >
                {post.category}
              </span>
              <span className="font-[family-name:var(--font-jetbrains)] text-xs text-muted">
                {formatBlogDate(post.date)} · {post.readTime} {BLOG_PAGE.readTime}
              </span>
            </div>

            <h1 className="mt-6 editorial-heading text-3xl sm:text-4xl">
              {post.title}
            </h1>
            <p className="mt-4 text-lg leading-relaxed text-muted">{post.excerpt}</p>
          </header>

          <div className="mt-10 border-t border-[var(--card-border)] pt-10">
            <ArticleContent content={post.content} />
          </div>

          <div className="mt-16 border-l-2 border-accent-warm py-2 pl-6">
            <p className="font-[family-name:var(--font-exo2)] text-lg font-semibold">
              Потрібна допомога з проєктом?
            </p>
            <p className="mt-2 text-sm text-muted">
              Розкажіть про задачу — відповімо в Telegram протягом 30 хвилин.
            </p>
            <Link href="/#contact" className="btn-primary mt-4 inline-flex">
              Розпочати проєкт
            </Link>
          </div>
        </article>
      </main>
      <Footer />
      <FloatingTelegramButton />
    </>
  );
}
