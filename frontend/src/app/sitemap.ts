import type { MetadataRoute } from "next";
import { getBlogPosts } from "@/lib/blog-api";
import { SERVICE_PAGES } from "@/lib/marketing-pages";
import { getPortfolioProjects } from "@/lib/portfolio-api";
import { absoluteUrl } from "@/lib/seo/site-url";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const [posts, projects] = await Promise.all([
    getBlogPosts().then((items) => items.filter((post) => !post.noindex)),
    getPortfolioProjects(),
  ]);

  return [
    {
      url: absoluteUrl("/"),
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 1,
    },
    {
      url: absoluteUrl("/poslugy"),
      lastModified: new Date(),
      changeFrequency: "monthly",
      priority: 0.9,
    },
    ...SERVICE_PAGES.map((page) => ({
      url: absoluteUrl(page.href),
      lastModified: new Date(),
      changeFrequency: "monthly" as const,
      priority: 0.9,
    })),
    {
      url: absoluteUrl("/works"),
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.85,
    },
    ...projects.map((project) => ({
      url: absoluteUrl(`/works/${project.slug}`),
      lastModified: new Date(),
      changeFrequency: "monthly" as const,
      priority: 0.7,
    })),
    {
      url: absoluteUrl("/blog"),
      lastModified: new Date(),
      changeFrequency: "weekly",
      priority: 0.8,
    },
    {
      url: absoluteUrl("/privacy"),
      lastModified: new Date(),
      changeFrequency: "yearly" as const,
      priority: 0.2,
    },
    {
      url: absoluteUrl("/oferta"),
      lastModified: new Date(),
      changeFrequency: "yearly" as const,
      priority: 0.2,
    },
    ...posts.map((post) => ({
      url: absoluteUrl(`/blog/${post.slug}`),
      lastModified: new Date(post.date),
      changeFrequency: "monthly" as const,
      priority: 0.6,
    })),
  ];
}
