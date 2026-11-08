import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  images: {
    remotePatterns: [
      {
        protocol: "http",
        hostname: "127.0.0.1",
      },
      {
        protocol: "http",
        hostname: "localhost",
      },
      {
        protocol: "http",
        hostname: "minio",
      },
      {
        protocol: "https",
        hostname: "**.ngrok-free.app",
      },
      {
        protocol: "https",
        hostname: "**.ngrok.app",
      },
      {
        protocol: "https",
        hostname: "**.ngrok-free.dev",
      },
    ],
  },
};

export default nextConfig;
