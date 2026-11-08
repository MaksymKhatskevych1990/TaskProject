import { getPortfolioProjects } from "@/lib/portfolio-api";
import { PortfolioSectionClient } from "@/components/sections/PortfolioSectionClient";

export async function PortfolioSection() {
  const projects = await getPortfolioProjects();
  return <PortfolioSectionClient projects={projects} />;
}
