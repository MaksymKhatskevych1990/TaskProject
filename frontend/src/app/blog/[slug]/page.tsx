import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { FloatingTelegramButton } from "@/components/sections/FloatingTelegramButton";
import { ArticleContent } from "@/components/blog/ArticleContent";
import { formatBlogDate, getBlogPost } from "@/lib/blog-api";
import { BLOG_PAGE, SITE } from "@/lib/site-data";
import { cn } from "@/lib/utils";

const categoryColors: Record<string, string> = {
  SEO: "bg-emerald-400/10 text-emerald-400",
  Розробка: "bg-cyan/10 text-cyan",
  Дизайн: "bg-violet/10 text-violet",
  "E-commerce": "bg-orange-400/10 text-orange-400",
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

  return {
    title: `${post.title} — ${SITE.brand}`,
    description: post.excerpt,
  };
}

export default async function BlogPostPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getBlogPost(slug);
  if (!post) notFound();

  return (
    <>
      <Header />
      <main className="pt-24 pb-20">
        <article className="mx-auto max-w-3xl px-4 sm:px-6">
          <Link
            href="/blog"
            className="inline-flex text-sm text-cyan transition-opacity hover:opacity-80"
          >
            {BLOG_PAGE.backToBlog}
          </Link>

          <header className="mt-6">
            <div className="flex flex-wrap items-center gap-3">
              <span
                className={cn(
                  "rounded-full px-2.5 py-0.5 text-[11px] font-medium",
                  categoryColors[post.category] ?? "bg-white/5 text-muted",
                )}
              >
                {post.category}
              </span>
              <span className="font-[family-name:var(--font-jetbrains)] text-xs text-muted">
                {formatBlogDate(post.date)} · {post.readTime} {BLOG_PAGE.readTime}
              </span>
            </div>

            <h1 className="mt-4 font-[family-name:var(--font-exo2)] text-3xl font-bold leading-tight sm:text-4xl">
              {post.title}
            </h1>
            <p className="mt-4 text-lg leading-relaxed text-muted">{post.excerpt}</p>
          </header>

          <div className="mt-10 border-t border-white/5 pt-10">
            <ArticleContent content={post.content} />
          </div>

          <div className="mt-12 rounded-2xl border border-white/5 bg-card p-6 text-center">
            <p className="font-[family-name:var(--font-exo2)] text-lg font-semibold">
              Потрібна допомога з проєктом?
            </p>
            <p className="mt-2 text-sm text-muted">
              Розкажіть про задачу — відповімо в Telegram протягом 30 хвилин.
            </p>
            <Link
              href="/#contact"
              className="mt-4 inline-flex rounded-full bg-gradient-to-r from-cyan to-violet px-6 py-3 text-sm font-semibold text-[#070b18] transition-opacity hover:opacity-90"
            >
              Обговорити проєкт
            </Link>
          </div>
        </article>
      </main>
      <Footer />
      <FloatingTelegramButton />
    </>
  );
}
