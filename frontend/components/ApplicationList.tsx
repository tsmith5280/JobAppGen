import { useEffect, useState } from "react";

type Application = {
  job_title: string;
  company: string;
  status: string;
  date: string;
  notes: string;
};

export default function ApplicationList({ refresh }: { refresh: boolean }) {
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const res = await fetch("http://localhost:8000/applications/");
        const data = await res.json();
        setApplications(data);
      } catch (error) {
        console.error("Failed to load applications:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, [refresh]);

  if (loading) return <p className="mt-6">Loading applications...</p>;
  if (!applications.length) return <p className="mt-6">No applications found.</p>;

  return (
    <div className="mt-8 space-y-4">
      {applications.map((app, index) => (
        <div
          key={index}
          className="border p-4 rounded shadow-sm bg-white dark:bg-zinc-800"
        >
          <h3 className="text-lg font-semibold">{app.job_title} @ {app.company}</h3>
          <p className="text-sm text-zinc-500">Status: {app.status}</p>
          <p className="text-sm">Applied on: {app.date}</p>
          <p className="mt-2 text-sm italic">{app.notes}</p>
        </div>
      ))}
    </div>
  );
}
