import React from "react";
import Sidebar from "./Sidebar";

type DashboardLayoutProps = {
  children: React.ReactNode;
  profile: any; // Or a more specific profile type
};

const DashboardLayout: React.FC<DashboardLayoutProps> = ({
  children,
  profile,
}) => {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="grid grid-cols-[280px_1fr]">
        <Sidebar profile={profile} />
        <main className="p-8">{children}</main>
      </div>
    </div>
  );
};

export default DashboardLayout;