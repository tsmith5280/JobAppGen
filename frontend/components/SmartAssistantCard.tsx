import React, { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { X, MessageCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

interface SmartAssistantCardProps {
  messages?: string[];
  onDismiss?: () => void;
}

const SmartAssistantCard = ({
  messages = [
    "Follow up with TechCorp?",
    "Need to update your resume?",
    "You've applied to 4 jobs this week—amazing!",
    "Time to check your LinkedIn messages?",
    "Consider applying to similar roles at StartupXYZ?",
    "Your interview with DataCorp is tomorrow!",
  ],
  onDismiss = () => {},
}: SmartAssistantCardProps) => {
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);
  const [isVisible, setIsVisible] = useState(true);
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimate(true);
      setTimeout(() => {
        setCurrentMessageIndex((prev) => (prev + 1) % messages.length);
        setAnimate(false);
      }, 300);
    }, 4000);

    return () => clearInterval(interval);
  }, [messages.length]);

  const handleDismiss = () => {
    setIsVisible(false);
    setTimeout(() => {
      onDismiss();
    }, 300);
  };

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 animate-in slide-in-from-bottom-4 duration-500">
      <Card className="w-80 bg-gradient-to-br from-teal-50 to-amber-50 border-teal-200 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
        <CardContent className="p-4">
          <div className="flex items-start space-x-3">
            {/* Avatar */}
            <div className="relative">
              <Avatar className="h-10 w-10 ring-2 ring-teal-200 ring-offset-2">
                <AvatarImage src="https://api.dicebear.com/7.x/avataaars/svg?seed=assistant&backgroundColor=teal" />
                <AvatarFallback className="bg-teal-100 text-teal-700">
                  <MessageCircle className="h-5 w-5" />
                </AvatarFallback>
              </Avatar>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-teal-400 rounded-full animate-pulse"></div>
            </div>

            {/* Message Content */}
            <div className="flex-1 min-w-0">
              <div className="flex items-center justify-between mb-1">
                <h4 className="text-sm font-semibold text-teal-800">
                  Smart Assistant
                </h4>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleDismiss}
                  className="h-6 w-6 p-0 text-teal-600 hover:text-teal-800 hover:bg-teal-100"
                >
                  <X className="h-3 w-3" />
                </Button>
              </div>

              <div className="relative overflow-hidden">
                <p
                  className={`text-sm text-teal-700 transition-all duration-300 ${animate ? "opacity-0 transform translate-y-2" : "opacity-100 transform translate-y-0"}`}
                >
                  {messages[currentMessageIndex]}
                </p>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex justify-end space-x-2 mt-3 pt-3 border-t border-teal-100">
            <Button
              variant="outline"
              size="sm"
              className="text-xs border-teal-200 text-teal-700 hover:bg-teal-50 hover:border-teal-300"
            >
              Remind Later
            </Button>
            <Button
              size="sm"
              className="text-xs bg-teal-600 hover:bg-teal-700 text-white"
            >
              Take Action
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default SmartAssistantCard;
