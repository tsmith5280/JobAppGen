import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import {
  LayoutDashboard,
  FileText,
  Calendar,
  Settings,
  ChevronLeft,
  ChevronRight,
  LogOut,
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface SidebarProps {
  collapsed?: boolean;
  onToggle?: () => void;
}

const Sidebar = ({ collapsed = false, onToggle = () => {} }: SidebarProps) => {
  const [isCollapsed, setIsCollapsed] = useState(collapsed);
  const [warmMessage, setWarmMessage] = useState("You've got this!");

  const warmMessages = [
    "You've got this!",
    "Keep going, Alex!",
    "Stay motivated!",
    "Success is coming!",
    "One step at a time!",
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setWarmMessage(
        warmMessages[Math.floor(Math.random() * warmMessages.length)],
      );
    }, 10000); // Change message every 10 seconds

    return () => clearInterval(interval);
  }, []);

  const handleToggle = () => {
    setIsCollapsed(!isCollapsed);
    onToggle();
  };

  return (
    <div
      className={`h-screen bg-stone-50 border-r border-stone-200 flex flex-col transition-all duration-300 shadow-lg ${isCollapsed ? "w-16" : "w-64"}`}
    >
      {/* Logo */}
      <div className="p-4 flex items-center justify-between border-b border-stone-200">
        {!isCollapsed && (
          <div className="font-bold text-xl text-stone-800">JobTracker</div>
        )}
        <Button
          variant="ghost"
          size="icon"
          onClick={handleToggle}
          className={`hover:bg-stone-200 ${isCollapsed ? "mx-auto" : ""}`}
        >
          {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </Button>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 py-4">
        <TooltipProvider>
          <ul className="space-y-2 px-2">
            <li>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Link
                    to="/"
                    className={`flex items-center p-3 rounded-lg hover:bg-stone-200 hover:shadow-sm transition-all duration-200 group ${!isCollapsed ? "justify-start" : "justify-center"}`}
                  >
                    <LayoutDashboard size={20} className="text-stone-700" />
                    {!isCollapsed && (
                      <span className="ml-3 text-stone-800 font-medium">
                        Dashboard
                      </span>
                    )}
                  </Link>
                </TooltipTrigger>
                {isCollapsed && (
                  <TooltipContent side="right">Dashboard</TooltipContent>
                )}
              </Tooltip>
            </li>
            <li>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Link
                    to="/applications"
                    className={`flex items-center p-3 rounded-lg hover:bg-stone-200 hover:shadow-sm transition-all duration-200 group ${!isCollapsed ? "justify-start" : "justify-center"}`}
                  >
                    <FileText size={20} className="text-stone-700" />
                    {!isCollapsed && (
                      <span className="ml-3 text-stone-800 font-medium">
                        Applications
                      </span>
                    )}
                  </Link>
                </TooltipTrigger>
                {isCollapsed && (
                  <TooltipContent side="right">Applications</TooltipContent>
                )}
              </Tooltip>
            </li>
            <li>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Link
                    to="/calendar"
                    className={`flex items-center p-3 rounded-lg hover:bg-stone-200 hover:shadow-sm transition-all duration-200 group ${!isCollapsed ? "justify-start" : "justify-center"}`}
                  >
                    <Calendar size={20} className="text-stone-700" />
                    {!isCollapsed && (
                      <span className="ml-3 text-stone-800 font-medium">
                        Calendar
                      </span>
                    )}
                  </Link>
                </TooltipTrigger>
                {isCollapsed && (
                  <TooltipContent side="right">Calendar</TooltipContent>
                )}
              </Tooltip>
            </li>
            <li>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Link
                    to="/settings"
                    className={`flex items-center p-3 rounded-lg hover:bg-stone-200 hover:shadow-sm transition-all duration-200 group ${!isCollapsed ? "justify-start" : "justify-center"}`}
                  >
                    <Settings size={20} className="text-stone-700" />
                    {!isCollapsed && (
                      <span className="ml-3 text-stone-800 font-medium">
                        Settings
                      </span>
                    )}
                  </Link>
                </TooltipTrigger>
                {isCollapsed && (
                  <TooltipContent side="right">Settings</TooltipContent>
                )}
              </Tooltip>
            </li>
          </ul>
        </TooltipProvider>
      </nav>

      {/* User Profile */}
      <div
        className={`border-t border-stone-200 p-4 ${isCollapsed ? "flex flex-col items-center" : ""}`}
      >
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <div
                className={`flex items-center ${isCollapsed ? "justify-center mb-2" : "space-x-3"}`}
              >
                <Avatar className="ring-2 ring-stone-300 ring-offset-2 ring-offset-stone-50">
                  <AvatarImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=alex123" />
                  <AvatarFallback className="bg-stone-300 text-stone-700">
                    AL
                  </AvatarFallback>
                </Avatar>
                {!isCollapsed && (
                  <div className="flex-1">
                    <p className="text-sm font-medium text-stone-800">
                      Alex Johnson
                    </p>
                    <p className="text-xs text-stone-600">alex@example.com</p>
                  </div>
                )}
              </div>
            </TooltipTrigger>
            {isCollapsed && (
              <TooltipContent side="right">Alex Johnson</TooltipContent>
            )}
          </Tooltip>
        </TooltipProvider>

        {/* Warm Message */}
        {!isCollapsed && (
          <div className="mt-3 mb-2">
            <p className="text-sm text-center text-stone-700 font-medium bg-stone-100 px-3 py-2 rounded-lg shadow-sm">
              {warmMessage}
            </p>
          </div>
        )}

        {!isCollapsed && (
          <Button
            variant="ghost"
            size="sm"
            className="w-full mt-2 justify-start hover:bg-stone-200 text-stone-700"
          >
            <LogOut size={16} className="mr-2" />
            Sign Out
          </Button>
        )}
      </div>
    </div>
  );
};

export default Sidebar;
