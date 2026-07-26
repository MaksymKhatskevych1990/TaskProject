export const CODE_COLORS = {
  keyword: "rgba(134, 239, 172, 0.85)",
  number: "rgba(134, 239, 172, 0.65)",
  punctuation: "rgba(134, 239, 172, 0.42)",
  default: "rgba(134, 239, 172, 0.38)",
  comment: "rgba(134, 239, 172, 0.24)",
  lineNumber: "rgba(134, 239, 172, 0.11)",
} as const;

const JS_KEYWORDS = new Set([
  "const",
  "let",
  "var",
  "async",
  "await",
  "function",
  "class",
  "return",
  "import",
  "export",
  "from",
  "if",
  "else",
  "new",
  "true",
  "false",
  "null",
  "undefined",
  "typeof",
]);

const PY_KEYWORDS = new Set([
  "def",
  "class",
  "async",
  "await",
  "return",
  "import",
  "from",
  "if",
  "else",
  "elif",
  "for",
  "while",
  "True",
  "False",
  "None",
  "with",
  "as",
  "in",
  "pass",
  "self",
]);

const PUNCTUATION = new Set("{}[]().,:;<>+-=*/\\|&!?@#$%^&~`\"'");

export type CodeLanguage = "js" | "python";

export type HighlightToken = {
  text: string;
  color: string;
};

export function highlightCode(code: string, language: CodeLanguage): HighlightToken[] {
  const keywords = language === "js" ? JS_KEYWORDS : PY_KEYWORDS;
  const tokens: HighlightToken[] = [];
  let index = 0;

  while (index < code.length) {
    const rest = code.slice(index);

    if (language === "js" && rest.startsWith("//")) {
      const end = code.indexOf("\n", index);
      const text = end === -1 ? code.slice(index) : code.slice(index, end);
      tokens.push({ text, color: CODE_COLORS.comment });
      index += text.length;
      continue;
    }

    if (language === "python" && code[index] === "#") {
      const end = code.indexOf("\n", index);
      const text = end === -1 ? code.slice(index) : code.slice(index, end);
      tokens.push({ text, color: CODE_COLORS.comment });
      index += text.length;
      continue;
    }

    const wordMatch = rest.match(/^[A-Za-z_$][\w$]*/);
    if (wordMatch) {
      const text = wordMatch[0];
      tokens.push({
        text,
        color: keywords.has(text) ? CODE_COLORS.keyword : CODE_COLORS.default,
      });
      index += text.length;
      continue;
    }

    const numberMatch = rest.match(/^\d+(?:\.\d+)?/);
    if (numberMatch) {
      tokens.push({ text: numberMatch[0], color: CODE_COLORS.number });
      index += numberMatch[0].length;
      continue;
    }

    const char = code[index];
    if (PUNCTUATION.has(char)) {
      tokens.push({ text: char, color: CODE_COLORS.punctuation });
      index += 1;
      continue;
    }

    if (char === "\n") {
      tokens.push({ text: "\n", color: CODE_COLORS.default });
      index += 1;
      continue;
    }

    if (char === " " || char === "\t") {
      let whitespace = "";
      while (index < code.length && (code[index] === " " || code[index] === "\t")) {
        whitespace += code[index];
        index += 1;
      }
      tokens.push({ text: whitespace, color: CODE_COLORS.default });
      continue;
    }

    tokens.push({ text: char, color: CODE_COLORS.default });
    index += 1;
  }

  return tokens;
}

export function splitLines(code: string): string[] {
  return code.split("\n");
}
