import { getBackendApiUrl } from "@/lib/api-config";

export type BlogPostListItem = {
  slug: string;
  title: string;
  excerpt: string;
  date: string;
  readTime: number;
  category: string;
};

export type BlogPostDetail = BlogPostListItem & {
  content: string[];
};

type ApiResponse<T> = {
  success: boolean;
  data: T;
};

function buildWebsiteApiUrl(path: string): string {
  return new URL(`/api/v1/website${path}`, getBackendApiUrl()).href;
}

async function fetchBlogApi<T>(path: string): Promise<T | null> {
  try {
    const response = await fetch(buildWebsiteApiUrl(path), {
      cache: "no-store",
    });

    if (!response.ok) {
      return null;
    }

    const payload = (await response.json()) as ApiResponse<T>;
    return payload.success ? payload.data : null;
  } catch {
    return null;
  }
}

export async function getBlogPosts(): Promise<BlogPostListItem[]> {
  const posts = await fetchBlogApi<BlogPostListItem[]>("/blog/");
  return posts ?? [];
}

export async function getBlogPost(slug: string): Promise<BlogPostDetail | null> {
  const normalizedSlug = decodeURIComponent(slug);
  return fetchBlogApi<BlogPostDetail>(`/blog/${normalizedSlug}/`);
}

export function formatBlogDate(isoDate: string): string {
  return new Date(isoDate).toLocaleDateString("uk-UA", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
