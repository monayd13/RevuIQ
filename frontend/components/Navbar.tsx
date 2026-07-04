"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { User, LogOut } from "lucide-react";
import { isAuthenticated, getUserDataFromCookie, logout } from "@/lib/auth";

export default function Navbar() {
  const pathname = usePathname();
  const [authed, setAuthed] = useState(false);
  const [userName, setUserName] = useState("");

  useEffect(() => {
    const auth = isAuthenticated();
    setAuthed(auth);
    if (auth) {
      const userData = getUserDataFromCookie();
      setUserName((userData?.full_name as string) || (userData?.name as string) || (userData?.email as string) || 'User');
    } else {
      setUserName('');
    }
  }, [pathname]);

  const handleLogout = async () => {
    await logout();
    window.location.href = '/login';
  };

  const isActive = (path: string) => {
    return pathname === path
      ? "bg-blue-700 text-white"
      : "text-gray-300 hover:bg-blue-600 hover:text-white";
  };

  return (
    <nav className="bg-gradient-to-r from-blue-600 to-blue-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <span className="text-2xl font-bold text-white">RevuIQ</span>
              <span className="text-xs bg-green-400 text-green-900 px-2 py-1 rounded-full font-semibold">AI</span>
            </Link>
          </div>
          {authed && (
            <div className="flex space-x-2">
              <Link href="/dashboard" className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive("/dashboard")}`}>Dashboard</Link>
              <Link href="/restaurants" className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive("/restaurants")}`}>Restaurants</Link>
              <Link href="/responses/approve" className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive("/responses/approve")}`}>Approve Responses</Link>
              <Link href="/live-monitor" className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${isActive("/live-monitor")}`}>Live Monitor</Link>
            </div>
          )}
          <div className="flex items-center space-x-3">
            {authed ? (
              <>
                <div className="flex items-center space-x-2 px-3 py-2 bg-blue-700 rounded-md">
                  <User className="w-4 h-4 text-white" />
                  <span className="text-sm font-medium text-white">{userName}</span>
                </div>
                <button onClick={handleLogout} className="flex items-center space-x-2 px-4 py-2 bg-red-500 text-white rounded-md text-sm font-bold hover:bg-red-600 transition-colors shadow-md">
                  <LogOut className="w-4 h-4" />
                  <span>Logout</span>
                </button>
              </>
            ) : (
              <div className="flex items-center space-x-3">
                <Link href="/login" className="px-6 py-2 text-white rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">Login</Link>
                <Link href="/signup" className="px-6 py-2 bg-white text-blue-600 rounded-md text-sm font-bold hover:bg-gray-100 transition-colors shadow-md">Sign Up</Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
