"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Navbar() {
  const pathname = usePathname();

  const isActive = (path: string) => {
    return pathname === path
      ? "bg-blue-700 text-white"
      : "text-gray-300 hover:bg-blue-600 hover:text-white";
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo/Brand */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-white">RevuIQ</span>
              <span className="text-xs bg-green-400 text-green-900 px-2 py-1 rounded-full font-semibold">
                AI
              </span>
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="flex space-x-2">
            <Link
              href="/dashboard"
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive(
                "/dashboard"
              )}`}
            >
              📈 Dashboard
            </Link>
            <Link
              href="/restaurants"
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive(
                "/restaurants"
              )}`}
            >
              🏪 Restaurants
            </Link>
            <Link
              href="/reviews/approve"
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive(
                "/reviews/approve"
              )}`}
            >
              ✅ Approve Reviews
            </Link>
            <Link
              href="/responses/approve"
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive(
                "/responses/approve"
              )}`}
            >
              💬 Approve Responses
            </Link>
            <Link
              href="/analytics"
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive(
                "/analytics"
              )}`}
            >
              📊 Analytics
            </Link>
          </div>

          {/* Status Indicator */}
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1">
              <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
              <span className="text-xs text-gray-300">Live</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
