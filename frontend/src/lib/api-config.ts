/** Backend base URL for server-side API calls. */
export function getBackendApiUrl(): string {
  return process.env.API_URL ?? "http://127.0.0.1:8080";
}
