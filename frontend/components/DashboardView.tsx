import React, { useState } from "react";
import { Card } from "@/components/ui/card";
import Sidebar from "./Sidebar";
import StatsOverview from "./StatsOverview";
import ApplicationList from "./ApplicationList";
import SmartAssistantCard from "./SmartAssistantCard";
import type { ParsedProfile } from "@/components/ResumeUpload";

type Props = {
  profile: ParsedProfile | null;
};

export default function DashboardView({ profile }: Props) {
  const [showAssistant, setShowAssistant] = useState(true);
  const userName = profile?.full_name || "Guest";

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <header className="bg-background border-b p-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold">Dashboard</h1>
            <p className="text-muted-foreground">Welcome back, {userName}!</p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="text-sm bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 transition-colors">
              + New Application
            </button>
          </div>
        </header>

        {/* Main Content Area */}
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto space-y-6">
            {/* Stats Overview */}
            <section>
              <h2 className="text-xl font-semibold mb-4">Overview</h2>
              <StatsOverview />
            </section>

            {/* Applications List */}
            <section>
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-xl font-semibold">Recent Applications</h2>
                <select
                  className="bg-background border rounded-md px-3 py-1 text-sm"
                  defaultValue="all"
                >
                  <option value="all">All Applications</option>
                  <option value="applied">Applied</option>
                  <option value="interview">Interview</option>
                  <option value="rejected">Rejected</option>
                </select>
              </div>
              <Card className="p-6">
                <ApplicationList />
              </Card>
            </section>
          </div>
        </main>
      </div>

      {/* Smart Assistant Card */}
      {showAssistant && (
        <SmartAssistantCard onDismiss={() => setShowAssistant(false)} />
      )}
    </div>
  );
}
