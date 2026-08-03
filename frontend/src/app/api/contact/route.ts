import { NextRequest, NextResponse } from "next/server";

import { getBackendApiUrl } from "@/lib/api-config";

type ContactBody = {
  name?: string;
  phone?: string;
  project?: string;
  plan?: string;
};

export async function POST(request: NextRequest) {
  let body: ContactBody;

  try {
    body = (await request.json()) as ContactBody;
  } catch {
    return NextResponse.json({ success: false, error: "Invalid JSON" }, { status: 400 });
  }

  const { name, phone, project, plan } = body;

  if (!name?.trim() || !phone?.trim() || !project?.trim()) {
    return NextResponse.json(
      { success: false, error: "Missing required fields" },
      { status: 400 },
    );
  }

  const payload = {
    name: name.trim(),
    phone: phone.trim(),
    project: project.trim(),
    plan: plan?.trim() ?? "",
  };

  try {
    const response = await fetch(`${getBackendApiUrl()}/api/v1/website/contact/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      return NextResponse.json({ success: true });
    }
  } catch {
    // Fall through to client-side Telegram fallback.
  }

  return NextResponse.json({ success: true, fallback: "telegram" });
}
