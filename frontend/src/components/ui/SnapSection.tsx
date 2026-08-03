import { cn } from "@/lib/utils";

export function SnapSection({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div data-snap-section className={cn("snap-section", className)}>
      {children}
    </div>
  );
}
