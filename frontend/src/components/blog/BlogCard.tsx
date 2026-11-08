import Link from "next/link";
import { getSiteContent } from "@/lib/site-content";
import { formatBlogDate, type BlogPostListItem } from "@/lib/blog-api";
import { cn } from "@/lib/utils";

const categoryColors: Record<string, string> = {
  SEO: "border-accent/30 text-accent-bright",
  Розробка: "border-accent-warm/30 text-accent-warm-bright",
  Дизайн: "border-[var(--card-border)] text-foreground",
  "E-commerce": "border-accent-warm/30 text-accent-warm-bright",
};

export async function BlogCard({
  post,
  featured = false,
}: {
  post: BlogPostListItem;
  featured?: boolean;
}) {
  const content = await getSiteContent();
  return (
    <Link
      href={`/blog/${post.slug}`}
      className={cn(
        "group flex h-full flex-col border-t border-[var(--card-border)] py-8 transition-colors hover:border-accent/30",
        featured && "sm:col-span-2 lg:col-span-1",
      )}
    >
      <div className="flex items-center gap-3">
        <span
          className={cn(
            "border px-2 py-0.5 text-[11px] font-medium",
            categoryColors[post.category] ?? "border-[var(--card-border)] text-muted",
          )}
        >
          {post.category}
        </span>
        <span className="font-[family-name:var(--font-jetbrains)] text-[11px] text-muted">
          {formatBlogDate(post.date)}
        </span>
      </div>

      <h2
        className={cn(
          "mt-4 font-[family-name:var(--font-exo2)] font-semibold leading-snug transition-colors group-hover:text-accent-bright",
          featured ? "text-2xl" : "text-lg",
        )}
      >
        {post.title}
      </h2>

      <p className="mt-3 flex-1 text-sm leading-relaxed text-muted">
        {post.excerpt}
      </p>

      <div className="mt-5 flex items-center justify-between pt-4">
        <span className="font-[family-name:var(--font-jetbrains)] text-xs text-muted">
          {post.readTime} {content.blogPage.readTime}
        </span>
        <span className="text-sm font-medium text-muted transition-colors group-hover:text-accent-bright">
          {content.blogPage.readMore} →
        </span>
      </div>
    </Link>
  );
}
