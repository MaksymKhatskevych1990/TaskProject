function renderInline(text: string) {
  const parts = text.split(/(\*\*.+?\*\*)/g);

  return parts.map((part, index) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={index}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
}

function isListBlock(block: string): boolean {
  const lines = block.split("\n").filter((line) => line.trim());
  return lines.length > 0 && lines.every((line) => /^[*-]\s+/.test(line.trim()));
}

function parseListItems(block: string): string[] {
  return block
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => line.replace(/^[*-]\s+/, ""));
}

export function ArticleContent({ content }: { content: readonly string[] }) {
  return (
    <div className="space-y-4">
      {content.map((block, index) => {
        const trimmed = block.trim();

        if (trimmed.startsWith("## ")) {
          return (
            <h2
              key={index}
              className="pt-4 font-[family-name:var(--font-exo2)] text-xl font-semibold"
            >
              {trimmed.slice(3)}
            </h2>
          );
        }

        if (isListBlock(trimmed)) {
          return (
            <ul key={index} className="list-disc space-y-3 pl-5 text-muted">
              {parseListItems(trimmed).map((item, itemIndex) => (
                <li key={itemIndex} className="leading-relaxed">
                  {renderInline(item)}
                </li>
              ))}
            </ul>
          );
        }

        return (
          <p key={index} className="text-base leading-relaxed text-muted">
            {renderInline(trimmed)}
          </p>
        );
      })}
    </div>
  );
}
