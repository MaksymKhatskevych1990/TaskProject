import type { Metadata } from "next";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { BlogCard } from "@/components/blog/BlogCard";
import { FloatingTelegramButton } from "@/components/sections/FloatingTelegramButton";
import { getBlogPosts } from "@/lib/blog-api";
import { BLOG_PAGE } from "@/lib/site-data";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Блог — Devcraft",
  description:
    "Поради з дизайну, розробки сайтів та SEO від команди Devcraft. Корисні матеріали для бізнесу.",
};

export default async function BlogPage() {
  const posts = await getBlogPosts();
  const [featured, ...rest] = posts;

  return (
    <>
      <Header />
      <main className="pt-24 pb-20">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <div className="mb-12 text-center">
            <p className="font-[family-name:var(--font-jetbrains)] text-xs uppercase tracking-widest text-cyan">
              {BLOG_PAGE.eyebrow}
            </p>
            <h1 className="mt-3 font-[family-name:var(--font-exo2)] text-3xl font-bold sm:text-4xl lg:text-5xl">
              {BLOG_PAGE.title}
            </h1>
            <p className="mx-auto mt-3 max-w-2xl text-sm leading-relaxed text-muted">
              {BLOG_PAGE.subtitle}
            </p>
          </div>

          {posts.length === 0 ? (
            <p className="text-center text-sm text-muted">{BLOG_PAGE.empty}</p>
          ) : (
            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {featured ? <BlogCard post={featured} featured /> : null}
              {rest.map((post) => (
                <BlogCard key={post.slug} post={post} />
              ))}
            </div>
          )}
        </div>
      </main>
      <Footer />
      <FloatingTelegramButton />
    </>
  );
}
