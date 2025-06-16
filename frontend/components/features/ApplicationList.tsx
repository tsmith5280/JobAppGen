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

interface ApplicationListProps {
  refresh: boolean;
}

const getBadgeVariant = (status: string): "default" | "secondary" | "destructive" | "outline" => {
  switch (status.toLowerCase()) {
    case "interview": return "default";
    case "offer": return "secondary";
    case "rejected": return "destructive";
    case "applied": default: return "outline";
  }
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString("en-US", { month: "short", day: "numeric" });
};

const ApplicationList = ({ refresh }: ApplicationListProps) => {
  const supabase = useSupabaseClient();
  const [applications, setApplications] = useState<Application[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApplications = async () => {
      setLoading(true);
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
  }, [supabase, refresh]);

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="animate-pulse">
            <div className="h-48 bg-muted rounded-lg"></div>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {applications.length > 0 ? (
        applications.map((app) => (
          <Card key={app.id} className="hover:shadow-md transition-shadow">
            <CardContent className="p-4 flex flex-col justify-between h-full">
              <div>
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-semibold text-foreground pr-2">{app.job_title}</h3>
                  <Badge variant={getBadgeVariant(app.status)}>{app.status}</Badge>
                </div>
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div className="flex items-center">
                    <Building size={14} className="mr-2" />
                    <span>{app.company_name}</span>
                  </div>
                  <div className="flex items-center">
                    <Calendar size={14} className="mr-2" />
                    <span>{formatDate(app.application_date)}</span>
                  </div>
                </div>
              </div>
              <Button variant="secondary" size="sm" className="w-full mt-4">
                View Details
              </Button>
            </CardContent>
          </Card>
        ))
      ) : (
        <p className="text-muted-foreground col-span-full text-center py-8">
          You haven't added any applications yet.
        </p>
      )}
    </div>
  );
};

export default ApplicationList;