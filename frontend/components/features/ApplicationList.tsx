import { useEffect, useState } from "react";
import { useSupabaseClient } from "@supabase/auth-helpers-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Building, Calendar } from "lucide-react";

interface Application {
  id: string;
  job_title: string;
  company_name: string;
  status: string;
  application_date: string;
}

const getBadgeVariant = (status: string): "default" | "secondary" | "destructive" | "outline" => {
  switch (status.toLowerCase()) {
    case "interview":
      return "default";
    case "offer":
      return "secondary";
    case "rejected":
      return "destructive";
    case "applied":
      return "outline";
    default:
      return "outline"; // Add a default return value
  }
};

const formatDate = (dateString: string) => {
    // ... (formatDate function remains the same)
};

const ApplicationList = () => {
  const supabase = useSupabaseClient();
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApplications = async () => {
      try {
        const { data, error } = await supabase.functions.invoke("api/applications/");

        if (error) throw error;
        setApplications(data || []);
      } catch (error) {
        console.error("Error fetching applications:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchApplications();
  }, [supabase]);

  if (loading) {
    return <div className="mt-8">
        <h2 className="text-2xl font-bold mb-4">Recent Applications</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Skeleton loaders */}
            {[...Array(4)].map((_, i) => (
                <Card key={i} className="animate-pulse"><div className="h-48 bg-muted rounded-lg"></div></Card>
            ))}
        </div>
    </div>;
  }

  return (
    <div className="mt-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Recent Applications</h2>
        <Button variant="ghost">View all</Button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {applications.length > 0 ? applications.map((app) => (
          <Card key={app.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-4 flex flex-col justify-between h-full">
              {/* ... Card content JSX remains the same, but now uses live data ... */}
              {/* Example: <h3 ...>{app.job_title}</h3> */}
            </CardContent>
          </Card>
        )) : (
          <p className="text-muted-foreground col-span-full">You haven't added any applications yet. Get started!</p>
        )}
      </div>
    </div>
  );
};

export default ApplicationList;