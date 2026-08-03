import { getPortfolioProjects, getPortfolioProject } from "@/lib/portfolio-api";
import { PortfolioSectionClient } from "@/components/sections/PortfolioSectionClient";
import type { PortfolioProjectDetail } from "@/lib/portfolio-api";

export async function PortfolioSection() {
  const projects = await getPortfolioProjects();
  const details = await Promise.all(
    projects.map((project) => getPortfolioProject(project.slug)),
  );
  const detailsBySlug = projects.reduce<Record<string, PortfolioProjectDetail>>(
    (accumulator, project, index) => {
      const detail = details[index];
      if (detail) {
        accumulator[project.slug] = detail;
      }
      return accumulator;
    },
    {},
  );

  return (
    <PortfolioSectionClient projects={projects} detailsBySlug={detailsBySlug} />
  );
}
