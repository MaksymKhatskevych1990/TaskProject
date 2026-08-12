import Image from "next/image";
import emblem from "@/image/emblem.png";
import logo from "@/image/logo1.png";
import { SITE } from "@/lib/site-data";
import { cn } from "@/lib/utils";

const emblemSizes = {
  sm: "h-8 w-8",
  md: "h-10 w-10",
  lg: "h-16 w-16",
} as const;

type BrandLogoProps = {
  showText?: boolean;
  emblemSize?: keyof typeof emblemSizes;
  emblemVariant?: "default" | "header";
  className?: string;
};

export function BrandLogo({
  showText = true,
  emblemSize = "md",
  emblemVariant = "default",
  className,
}: BrandLogoProps) {
  const isHeaderEmblem = emblemVariant === "header";

  return (
    <span className={cn("flex items-center gap-2.5", className)}>
      <span
        className={cn(
          "relative shrink-0 overflow-hidden",
          emblemSizes[emblemSize],
        )}
        aria-hidden="true"
      >
        <Image
          src={isHeaderEmblem ? emblem : logo}
          alt=""
          fill
          sizes={emblemSize === "lg" ? "64px" : "40px"}
          className={
            isHeaderEmblem
              ? "object-contain"
              : "scale-[2.2] object-cover object-[center_76%]"
          }
          priority
        />
      </span>

      {showText ? (
        <span className="leading-none">
          <span className="block font-[family-name:var(--font-exo2)] text-[15px] font-bold tracking-tight text-foreground">
            {SITE.brandShort}
          </span>
          <span className="mt-0.5 block font-[family-name:var(--font-jetbrains)] text-[8px] uppercase tracking-[0.2em] text-muted">
            studio
          </span>
        </span>
      ) : null}
    </span>
  );
}
