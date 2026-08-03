import { getBackendApiUrl } from "@/lib/api-config";
import { PORTFOLIO } from "@/lib/site-data";

export type PortfolioAccent = "cyan" | "violet" | "green" | "orange";

export type PortfolioGalleryImage = {
  imageUrl: string | null;
  caption: string;
  ordering: number;
};

export type PortfolioProjectListItem = {
  slug: string;
  title: string;
  category: string;
  description: string;
  tags: string[];
  accent: PortfolioAccent;
  gradient: string;
  coverImage: string | null;
  featured: boolean;
  metric: string;
  before: string;
  after: string;
  clientUrl: string;
  hasCaseStudy: boolean;
};

export type PortfolioProjectDetail = PortfolioProjectListItem & {
  caseDescription: string;
  gallery: PortfolioGalleryImage[];
};

type ApiResponse<T> = {
  success: boolean;
  data: T;
};

const FALLBACK_PROJECTS: PortfolioProjectListItem[] = PORTFOLIO.map((project) => ({
  slug: project.slug,
  title: project.title,
  category: project.category,
  description: project.description,
  tags: [...project.tags],
  accent: project.accent as PortfolioAccent,
  gradient: project.gradient,
  coverImage: null,
  featured: project.slug === "glow-beauty",
  metric: "",
  before: "",
  after: "",
  clientUrl: "",
  hasCaseStudy: false,
}));

function buildWebsiteApiUrl(path: string): string {
  return new URL(`/api/v1/website${path}`, getBackendApiUrl()).href;
}

async function fetchPortfolioApi<T>(path: string): Promise<T | null> {
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

export async function getPortfolioProjects(): Promise<PortfolioProjectListItem[]> {
  const projects = await fetchPortfolioApi<PortfolioProjectListItem[]>("/portfolio/");
  return projects?.length ? projects : FALLBACK_PROJECTS;
}

export async function getPortfolioProject(
  slug: string,
): Promise<PortfolioProjectDetail | null> {
  const normalizedSlug = decodeURIComponent(slug);
  const project = await fetchPortfolioApi<PortfolioProjectDetail>(
    `/portfolio/${normalizedSlug}/`,
  );
  if (project) {
    return project;
  }

  const fallback = FALLBACK_PROJECTS.find((item) => item.slug === normalizedSlug);
  if (!fallback) {
    return null;
  }

  return {
    ...fallback,
    caseDescription: fallback.description,
    gallery: [],
  };
}
