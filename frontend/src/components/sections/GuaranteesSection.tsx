import Image, { type StaticImageData } from "next/image";
import { getSiteContent, type SiteGuarantee } from "@/lib/site-content";
import guaranteePrice from "@/image/guarantee-price.png";
import guaranteeTerm from "@/image/guarantee-term.png";
import guaranteeEdits from "@/image/guarantee-edits.png";
import guaranteeSupport from "@/image/guarantee-support.png";

const guaranteeImages: Record<SiteGuarantee["image"], StaticImageData> = {
  price: guaranteePrice,
  term: guaranteeTerm,
  edits: guaranteeEdits,
  support: guaranteeSupport,
};

export async function GuaranteesSection() {
  const content = await getSiteContent();

  return (
    <section id="guarantees" className="py-24 sm:py-32">
      <div className="mx-auto max-w-[90rem] px-5 sm:px-8 lg:px-12">
        <div className="mb-16">
          <p className="section-number mb-4">06</p>
          <h2 className="editorial-heading text-3xl sm:text-4xl">
            {content.sections.guarantees.title}
          </h2>
        </div>

        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">
          {content.guarantees.map((item, index) => (
            <article key={item.title} className="max-w-xs">
              <Image
                src={guaranteeImages[item.image] ?? guaranteePrice}
                alt=""
                className="mb-6 h-28 w-28 object-contain mix-blend-lighten sm:h-32 sm:w-32"
              />
              <p className="section-number mb-3">
                {String(index + 1).padStart(2, "0")}
              </p>
              <h3 className="text-lg font-semibold">{item.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">
                {item.description}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
