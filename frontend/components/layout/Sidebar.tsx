import React from "react";
import { useSupabaseClient } from "@supabase/auth-helpers-react";
import Link from "next/link";
import { useRouter } from "next/router";
import {
  LayoutDashboard,
  FileText,
  Calendar,
  Settings,
  LogOut,
  LucideIcon, // Import LucideIcon for typing
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Skeleton } from "../components/ui/skeleton";

// Define the type for a navigation item
interface NavItem {
  label: string;
  icon: LucideIcon;
  path: string;
}

// Define the navigation items with the correct type
const navItems: NavItem[] = [
  { label: "Dashboard", icon: LayoutDashboard, path: "/dashboard" },
  { label: "Applications", icon: FileText, path: "/applications" },
  { label: "Calendar", icon: Calendar, path: "/calendar" },
  { label: "Settings", icon: Settings, path: "/settings" },
];

interface SidebarProps {
  profile?: {
    full_name?: string;
    avatar_url?: string;
  };
}

const Sidebar = ({ profile }: SidebarProps) => {
  const supabase = useSupabaseClient();
  const router = useRouter();

  const getInitials = (name?: string) => {
    return (
      name
        ?.split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase() || ""
    );
  };

  return (
    <aside className="h-screen bg-background border-r border-border flex flex-col justify-between p-4">
      <div>
        <div className="font-bold text-xl mb-10">Joblight</div>
        <nav>
          <ul>
            {navItems.map(({ label, icon: Icon, path }) => (
              <li key={label}>
                <Link href={path} passHref legacyBehavior>
                  <a
                    className={`flex items-center p-3 rounded-lg hover:bg-accent hover:text-accent-foreground transition-colors duration-200 ${
                      router.pathname === path
                        ? "bg-accent text-accent-foreground"
                        : "text-muted-foreground"
                    }`}
                  >
                    <Icon size={20} />
                    <span className="ml-4 font-medium">{label}</span>
                  </a>
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      <div className="border-t border-border pt-4">
        <div className="flex items-center space-x-3 mb-4">
          {profile ? (
            <>
              <Avatar>
                <AvatarImage src={profile.avatar_url} alt={profile.full_name} />
                <AvatarFallback>
                  {getInitials(profile.full_name)}
                </AvatarFallback>
              </Avatar>
              <div>
                <p className="text-sm font-semibold text-foreground">
                  {profile.full_name || "New User"}
                </p>
              </div>
            </>
          ) : (
            <>
              <Skeleton className="h-10 w-10 rounded-full" />
              <div className="space-y-2">
                <Skeleton className="h-4 w-[120px]" />
              </div>
            </>
          )}
        </div>
        <Button
          variant="ghost"
          size="sm"
          className="w-full justify-start text-muted-foreground hover:text-foreground"
          onClick={() => supabase.auth.signOut()}
        >
          <LogOut size={16} className="mr-2" />
          Sign Out
        </Button>
      </div>
    </aside>
  );
};

export default Sidebar;