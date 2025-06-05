import React, { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { BriefcaseIcon, CalendarIcon, CheckCircleIcon } from "lucide-react";

interface StatsCardProps {
  title: string;
  count: number;
  icon: React.ReactNode;
  bgColor: string;
  microcopy: string[];
}

const StatsCard = ({
  title,
  count,
  icon,
  bgColor = "bg-teal-50",
  microcopy = ["Keep going!"],
}: StatsCardProps) => {
  const [currentMicrocopy, setCurrentMicrocopy] = useState(microcopy[0]);
  const [animate, setAnimate] = useState(false);

  useEffect(() => {
    if (microcopy.length > 1) {
      const interval = setInterval(() => {
        setAnimate(true);
        setTimeout(() => {
          setCurrentMicrocopy(
            microcopy[Math.floor(Math.random() * microcopy.length)],
          );
          setAnimate(false);
        }, 200);
      }, 5000);

      return () => clearInterval(interval);
    }
  }, [microcopy]);

  return (
    <Card className="rounded-2xl shadow-sm hover:shadow-lg transition-all duration-300 hover:scale-105 border-0">
      <CardContent className={`${bgColor} p-6 rounded-2xl`}>
        <div className="flex items-center space-x-4">
          <div className="bg-white/70 p-3 rounded-full shadow-sm">{icon}</div>
          <div className="flex-1">
            <p className="text-sm font-medium text-gray-600 mb-1">{title}</p>
            <h3 className="text-3xl font-light text-gray-800 mb-2">{count}</h3>
            <p
              className={`text-xs font-medium text-gray-500 transition-all duration-200 ${animate ? "opacity-0 transform translate-y-1" : "opacity-100 transform translate-y-0"}`}
            >
              {currentMicrocopy}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

interface StatsOverviewProps {
  applicationsSent?: number;
  interviewsScheduled?: number;
  offersReceived?: number;
}

const StatsOverview = ({
  applicationsSent = 24,
  interviewsScheduled = 8,
  offersReceived = 2,
}: StatsOverviewProps) => {
  const applicationsMicrocopy = [
    "Keep going!",
    "You're on fire!",
    "Great momentum!",
    "Stay consistent!",
  ];

  const interviewsMicrocopy = [
    "You're crushing it!",
    "Impressive progress!",
    "Keep it up!",
    "You've got this!",
  ];

  const offersMicrocopy = [
    "Amazing progress!",
    "Outstanding work!",
    "Success is yours!",
    "Incredible achievement!",
  ];

  return (
    <div className="bg-white w-full">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <StatsCard
          title="Applications Sent"
          count={applicationsSent}
          icon={<BriefcaseIcon className="h-6 w-6 text-teal-500" />}
          bgColor="bg-gradient-to-br from-teal-50 to-teal-100"
          microcopy={applicationsMicrocopy}
        />
        <StatsCard
          title="Interviews Scheduled"
          count={interviewsScheduled}
          icon={<CalendarIcon className="h-6 w-6 text-purple-500" />}
          bgColor="bg-gradient-to-br from-purple-50 to-lavender-100"
          microcopy={interviewsMicrocopy}
        />
        <StatsCard
          title="Offers Received"
          count={offersReceived}
          icon={<CheckCircleIcon className="h-6 w-6 text-emerald-500" />}
          bgColor="bg-gradient-to-br from-emerald-50 to-mint-100"
          microcopy={offersMicrocopy}
        />
      </div>
    </div>
  );
};

export default StatsOverview;
