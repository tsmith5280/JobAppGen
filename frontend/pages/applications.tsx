import { useState } from "react";
import Layout from "@/components/Layout";
import ApplicationForm from "@/components/ApplicationForm";
import ApplicationList from "@/components/ApplicationList";

export default function ApplicationsPage() {
  const [refresh, setRefresh] = useState(false);

  return (
    <Layout>
      <h2 className="text-2xl font-bold mb-4 text-amber-600">Job Applications</h2>
      <ApplicationForm onSubmitSuccess={() => setRefresh(prev => !prev)} />
      <ApplicationList refresh={refresh} />
    </Layout>
  );
}
