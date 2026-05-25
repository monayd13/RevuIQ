/** @type {import('next').NextConfig} */
const nextConfig = {
  // Allow backend API calls from Vercel
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/:path*`,
      },
    ]
  },
  images: {
    domains: ['localhost'],
  },
  // Needed for standalone output on Vercel
  output: 'standalone',
}

module.exports = nextConfig
