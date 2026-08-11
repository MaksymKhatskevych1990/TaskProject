import Image from "next/image";
import emblem from "@/image/emblem.png";
import logo from "@/image/logo1.png";
import { SITE } from "@/lib/site-data";
import { cn } from "@/lib/utils";

const emblemSizes = {
  sm: "h-9 w-9",
  md: "h-11 w-11",
  lg: "h-20 w-20",
} as const;

type BrandLogoProps = {
  showText?: boolean;
  emblemSize?: keyof typeof emblemSizes;
  /** Header: full chameleon fits inside the emblem box. */
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
    <span className={cn("flex items-center gap-3", className)}>
      <span
        className={cn(
          "relative shrink-0 overflow-hidden rounded-lg rounded-tr-none border border-cyan/25 bg-[#0a1020] shadow-lg shadow-cyan/15 ring-1 ring-white/10",
          emblemSizes[emblemSize],
        )}
        aria-hidden="true"
      >
        <Image
          src={isHeaderEmblem ? emblem : logo}
          alt=""
          fill
          sizes={emblemSize === "lg" ? "80px" : "44px"}
          className={
            isHeaderEmblem
              ? "object-contain p-2"
              : "scale-[2.2] object-cover object-[center_76%]"
          }
          priority
        />
      </span>

      {showText ? (
        <span className="leading-tight">
          <span className="block font-[family-name:var(--font-exo2)] text-base font-bold tracking-tight text-foreground sm:text-lg">
            {SITE.brandShort}
          </span>
          <span className="block font-[family-name:var(--font-jetbrains)] text-[9px] uppercase tracking-[0.22em] text-cyan/90 sm:text-[10px]">
            Digital Studio
          </span>
        </span>
      ) : null}
    </span>
  );
}
