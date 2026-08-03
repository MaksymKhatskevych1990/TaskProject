import Link from "next/link";
import { BLOG_PAGE } from "@/lib/site-data";
import { formatBlogDate, type BlogPostListItem } from "@/lib/blog-api";
import { cn } from "@/lib/utils";

const categoryColors: Record<string, string> = {
  SEO: "bg-emerald-400/10 text-emerald-400",
  Розробка: "bg-cyan/10 text-cyan",
  Дизайн: "bg-violet/10 text-violet",
  "E-commerce": "bg-orange-400/10 text-orange-400",
};

export function BlogCard({
  post,
  featured = false,
}: {
  post: BlogPostListItem;
  featured?: boolean;
}) {
  return (
    <Link
      href={`/blog/${post.slug}`}
      className={cn(
        "group flex h-full flex-col rounded-2xl border border-white/5 bg-card p-6 transition-all duration-300 hover:border-white/10 hover:shadow-lg hover:shadow-cyan/5",
        featured && "sm:col-span-2 lg:col-span-1",
      )}
    >
      <div className="flex items-center gap-3">
        <span
          className={cn(
            "rounded-full px-2.5 py-0.5 text-[11px] font-medium",
            categoryColors[post.category] ?? "bg-white/5 text-muted",
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
          "mt-4 font-[family-name:var(--font-exo2)] font-semibold leading-snug transition-colors group-hover:text-cyan",
          featured ? "text-2xl" : "text-lg",
        )}
      >
        {post.title}
      </h2>

      <p className="mt-3 flex-1 text-sm leading-relaxed text-muted">
        {post.excerpt}
      </p>

      <div className="mt-5 flex items-center justify-between border-t border-white/5 pt-4">
        <span className="font-[family-name:var(--font-jetbrains)] text-xs text-muted">
          {post.readTime} {BLOG_PAGE.readTime}
        </span>
        <span className="text-sm font-medium text-cyan transition-transform group-hover:translate-x-1">
          {BLOG_PAGE.readMore} →
        </span>
      </div>
    </Link>
  );
}
