import type { Metadata } from "next";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { BlogCard } from "@/components/blog/BlogCard";
import { JsonLd } from "@/components/seo/JsonLd";
import { FloatingTelegramButton } from "@/components/sections/FloatingTelegramButton";
import { getBlogPosts } from "@/lib/blog-api";
import { createPageMetadata } from "@/lib/seo/metadata";
import { buildBlogListGraph, buildSchemaGraph } from "@/lib/seo/schema";
import { BLOG_PAGE, SITE } from "@/lib/site-data";

export const dynamic = "force-dynamic";

export const metadata: Metadata = createPageMetadata({
  title: `Блог — ${SITE.brand}`,
  description: `Поради з дизайну, розробки сайтів та SEO від команди ${SITE.brandShort}. Корисні матеріали для бізнесу.`,
  path: "/blog",
});

export default async function BlogPage() {
  const posts = await getBlogPosts();
  const [featured, ...rest] = posts;
  const blogSchema = buildSchemaGraph(buildBlogListGraph(posts));

  return (
    <>
      <JsonLd data={blogSchema} />
      <Header />
      <main className="pt-28 pb-20">
        <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
          <div className="mb-16 max-w-lg">
            <p className="label-mono mb-4">{BLOG_PAGE.eyebrow}</p>
            <h1 className="editorial-heading text-3xl sm:text-4xl lg:text-5xl">
              {BLOG_PAGE.title}
            </h1>
            <p className="mt-4 text-sm leading-relaxed text-muted">
              {BLOG_PAGE.subtitle}
            </p>
          </div>

          {posts.length === 0 ? (
            <p className="text-sm text-muted">{BLOG_PAGE.empty}</p>
          ) : (
            <div className="grid gap-x-8 sm:grid-cols-2 lg:grid-cols-3">
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
