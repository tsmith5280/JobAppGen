import { useState, ReactElement } from "react";
import { NextPageWithLayout } from "./_app";
import DashboardLayout from "@/components/layout/DashboardLayout";
import ApplicationForm from "@/components/features/ApplicationForm";
import ApplicationList from "@/components/features/ApplicationList";

const ApplicationsPage: NextPageWithLayout = () => {
  const [refresh, setRefresh] = useState(false);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Applications</h1>
      </div>
      <ApplicationForm onSubmitSuccess={() => setRefresh(prev => !prev)} />

      <div className="mt-8">
        <ApplicationList refresh={refresh} />
      </div>
    </div>
  );
};

ApplicationsPage.getLayout = function getLayout(page: ReactElement) {
  const dummyProfile = { full_name: "User", avatar_url: "" };
  return (
    <DashboardLayout profile={dummyProfile}>
      {page}
    </DashboardLayout>
  );
};

export default ApplicationsPage;