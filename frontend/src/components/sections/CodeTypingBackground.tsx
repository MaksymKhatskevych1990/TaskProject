"use client";

import { useEffect, useState } from "react";
import {
  CODE_COLORS,
  highlightCode,
  splitLines,
  type CodeLanguage,
} from "@/lib/code-syntax";
import { cn } from "@/lib/utils";

const TYPING_INTERVAL_MS = 300;
const LOOP_PAUSE_MS = 2000;

const JS_CODE = `// Devcraft launch pipeline
const project = {
  name: "client-site",
  deadline: 14,
  stack: ["Next.js", "TG Bot"],
};

async function deploy() {
  await build();
  await test();
  return "Live!";
}`;

const PYTHON_CODE = `# Devcraft automation
def create_bot(token: str):
    bot = TelegramBot(token)
    bot.add_handler("/start", greet)
    return bot

class CRMIntegration:
    async def sync_leads(self, count=47):
        return count * 1.98`;

type CodePanelProps = {
  code: string;
  language: CodeLanguage;
  side: "left" | "right";
  delayMs?: number;
};

function CodePanel({ code, language, side, delayMs = 0 }: CodePanelProps) {
  const [charIndex, setCharIndex] = useState(0);
  const [cursorVisible, setCursorVisible] = useState(true);

  useEffect(() => {
    const blinkInterval = setInterval(() => {
      setCursorVisible((visible) => !visible);
    }, 530);

    return () => clearInterval(blinkInterval);
  }, []);

  useEffect(() => {
    let index = 0;
    let typingInterval: ReturnType<typeof setInterval> | undefined;
    let pauseTimeout: ReturnType<typeof setTimeout> | undefined;
    let startTimeout: ReturnType<typeof setTimeout> | undefined;

    const startTyping = () => {
      typingInterval = setInterval(() => {
        index += 1;
        setCharIndex(index);

        if (index >= code.length) {
          clearInterval(typingInterval);
          pauseTimeout = setTimeout(() => {
            index = 0;
            setCharIndex(0);
            startTyping();
          }, LOOP_PAUSE_MS);
        }
      }, TYPING_INTERVAL_MS);
    };

    startTimeout = setTimeout(startTyping, delayMs);

    return () => {
      clearTimeout(startTimeout);
      clearInterval(typingInterval);
      clearTimeout(pauseTimeout);
    };
  }, [code, delayMs]);

  const visibleCode = code.slice(0, charIndex);
  const lines = splitLines(visibleCode);

  const renderedLines = lines.map((line, lineIndex) => {
    const lineTokens = highlightCode(line, language);
    const isLastLine = lineIndex === lines.length - 1;

    return (
      <div key={`${lineIndex}-${line.length}`} className="flex">
        <span
          className="mr-4 w-5 shrink-0 select-none text-right tabular-nums"
          style={{ color: CODE_COLORS.lineNumber }}
        >
          {lineIndex + 1}
        </span>
        <span className="whitespace-pre">
          {lineTokens.map((token, tokenIndex) => (
            <span key={tokenIndex} style={{ color: token.color }}>
              {token.text}
            </span>
          ))}
          {isLastLine && (
            <span
              className="inline-block align-baseline"
              style={{
                color: CODE_COLORS.keyword,
                opacity: cursorVisible ? 1 : 0,
              }}
            >
              ▋
            </span>
          )}
        </span>
      </div>
    );
  });

  return (
    <div
      className={cn(
        "pointer-events-none absolute top-1/2 hidden w-[290px] -translate-y-1/2 lg:block",
        side === "left" ? "left-0" : "right-0",
      )}
    >
      <div className="relative overflow-hidden px-4 py-2">
        <pre className="font-[family-name:var(--font-jetbrains)] text-[11px] leading-[1.65]">
          {renderedLines}
        </pre>

        <div
          className={cn(
            "pointer-events-none absolute inset-y-0 w-20",
            side === "left"
              ? "right-0 bg-gradient-to-l from-[#070b18] to-transparent"
              : "left-0 bg-gradient-to-r from-[#070b18] to-transparent",
          )}
        />
      </div>
    </div>
  );
}

export function CodeTypingBackground() {
  return (
    <div className="pointer-events-none absolute inset-0 z-[1] overflow-hidden">
      <CodePanel code={PYTHON_CODE} language="python" side="left" delayMs={400} />
      <CodePanel code={JS_CODE} language="js" side="right" />

      <div className="pointer-events-none absolute inset-x-0 top-0 h-24 bg-gradient-to-b from-[#070b18] to-transparent" />
      <div className="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-[#070b18] to-transparent" />
    </div>
  );
}
