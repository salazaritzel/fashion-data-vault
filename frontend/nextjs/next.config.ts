import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  /* config options here */
};

export default nextConfig;
// What next.config.ts has done here, is that it forwarded the calls to the port localhost:3000 which have a specific FastAPI ending /api/py/docs to the port 8000 (which is the port that the Uvicorn server listens to).