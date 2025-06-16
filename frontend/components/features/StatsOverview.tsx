import { useEffect, useState } from "react";
import { useSupabaseClient } from "@supabase/auth-helpers-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Briefcase, Calendar, CheckCircle } from "lucide-react";

interface StatData {
  applications_sent: number;
  interviews: number;
  offers: number;
}

const StatsOverview = () => {
  const supabase = useSupabaseClient();
  const [stats, setStats] = useState<StatData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const { data, error } = await supabase.functions.invoke("api/applications/stats");

        if (error) throw error;
        setStats(data);
      } catch (error) {
        console.error("Error fetching application stats:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [supabase]);

  const statItems = [
    { title: "Applications Sent", value: stats?.applications_sent, icon: Briefcase, iconClass: "text-blue-500" },
    { title: "Interviews", value: stats?.interviews, icon: Calendar, iconClass: "text-purple-500" },
    { title: "Offers Received", value: stats?.offers, icon: CheckCircle, iconClass: "text-green-500" },
  ];

  if (loading) {
    return <div className="grid gap-4 md:grid-cols-3">
        {/* Skeleton loaders for a better UX */}
        {[...Array(3)].map((_, i) => (
            <Card key={i} className="animate-pulse">
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <div className="h-4 bg-muted rounded w-2/3"></div>
                    <div className="h-4 w-4 bg-muted rounded-full"></div>
                </CardHeader>
                <CardContent><div className="h-8 bg-muted rounded w-1/3"></div></CardContent>
            </Card>
        ))}
    </div>;
  }

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {statItems.map((item) => (
        <Card key={item.title} className="hover:shadow-md transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              {item.title}
            </CardTitle>
            <item.icon className={`h-4 w-4 ${item.iconClass}`} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{item.value ?? 0}</div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default StatsOverview;