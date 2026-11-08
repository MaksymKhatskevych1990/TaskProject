import type { Metadata } from "next";
import { Footer } from "@/components/layout/Footer";
import { Header } from "@/components/layout/Header";
import { BlogCard } from "@/components/blog/BlogCard";
import { JsonLd } from "@/components/seo/JsonLd";
import { FloatingTelegramButton } from "@/components/sections/FloatingTelegramButton";
import { getBlogPosts } from "@/lib/blog-api";
import { createPageMetadata } from "@/lib/seo/metadata";
import { buildBlogListGraph, buildSchemaGraph } from "@/lib/seo/schema";
import { getSiteSeo } from "@/lib/seo/site-seo-api";
import { getSiteContent } from "@/lib/site-content";

export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  const content = await getSiteContent();
  const siteSeo = await getSiteSeo();
  const title = siteSeo.blogTitle || `Блог — ${content.brand}`;
  const description =
    siteSeo.blogDescription ||
    `Поради з дизайну, розробки сайтів та SEO від команди ${content.brandShort}. Корисні матеріали для бізнесу.`;

  return createPageMetadata({
    title,
    description,
    path: "/blog",
    absoluteTitle: Boolean(siteSeo.blogTitle),
  });
}

export default async function BlogPage() {
  const [posts, siteSeo, content] = await Promise.all([
    getBlogPosts(),
    getSiteSeo(),
    getSiteContent(),
  ]);
  const [featured, ...rest] = posts;
  const blogSchema = buildSchemaGraph(buildBlogListGraph(posts, content));
  const heading = siteSeo.blogH1 || content.blogPage.title;

  return (
    <>
      <JsonLd data={blogSchema} />
      <Header />
      <main className="pt-28 pb-20">
        <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
          <div className="mb-16 max-w-lg">
            <p className="label-mono mb-4">{content.blogPage.eyebrow}</p>
            <h1 className="editorial-heading text-3xl sm:text-4xl lg:text-5xl">
              {heading}
            </h1>
            <p className="mt-4 text-sm leading-relaxed text-muted">
              {content.blogPage.subtitle}
            </p>
          </div>

          {posts.length === 0 ? (
            <p className="text-sm text-muted">{content.blogPage.empty}</p>
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
