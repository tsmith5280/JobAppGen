import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { CalendarIcon, BriefcaseIcon, BuildingIcon } from "lucide-react";

interface Application {
  id: string;
  jobTitle: string;
  companyName: string;
  applicationDate: string;
  status: "Applied" | "Interview" | "Rejected" | "Offer";
}

interface ApplicationListProps {
  applications?: Application[];
}

const ApplicationList = ({ applications = [] }: ApplicationListProps) => {
  // Default applications if none are provided
  const defaultApplications: Application[] = [
    {
      id: "1",
      jobTitle: "Frontend Developer",
      companyName: "Tech Solutions Inc.",
      applicationDate: "2023-06-15",
      status: "Applied",
    },
    {
      id: "2",
      jobTitle: "UX Designer",
      companyName: "Creative Designs Co.",
      applicationDate: "2023-06-10",
      status: "Interview",
    },
    {
      id: "3",
      jobTitle: "Full Stack Engineer",
      companyName: "Web Innovations",
      applicationDate: "2023-06-05",
      status: "Rejected",
    },
    {
      id: "4",
      jobTitle: "Product Manager",
      companyName: "Software Giants",
      applicationDate: "2023-06-01",
      status: "Applied",
    },
    {
      id: "5",
      jobTitle: "DevOps Engineer",
      companyName: "Cloud Systems",
      applicationDate: "2023-05-28",
      status: "Interview",
    },
    {
      id: "6",
      jobTitle: "Data Scientist",
      companyName: "Analytics Pro",
      applicationDate: "2023-05-20",
      status: "Offer",
    },
  ];

  const displayApplications =
    applications.length > 0 ? applications : defaultApplications;

  // Function to determine badge color based on status
  const getBadgeVariant = (status: string) => {
    switch (status) {
      case "Applied":
        return "default"; // Green
      case "Interview":
        return "secondary"; // Blue
      case "Rejected":
        return "destructive"; // Red
      case "Offer":
        return "outline"; // Outline style
      default:
        return "default";
    }
  };

  // Function to format date
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const handleFollowUp = (id: string) => {
    console.log(`Follow up for application ${id}`);
    // Implement follow-up action here
  };

  return (
    <div className="bg-background w-full">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Recent Applications</h2>
        <Button variant="outline">View All</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {displayApplications.map((application) => (
          <Card
            key={application.id}
            className="overflow-hidden hover:shadow-md transition-shadow duration-300"
          >
            <CardContent className="p-6">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-lg truncate">
                  {application.jobTitle}
                </h3>
                <Badge variant={getBadgeVariant(application.status)}>
                  {application.status}
                </Badge>
              </div>

              <div className="space-y-3 mt-4">
                <div className="flex items-center text-muted-foreground">
                  <BuildingIcon className="h-4 w-4 mr-2" />
                  <span>{application.companyName}</span>
                </div>

                <div className="flex items-center text-muted-foreground">
                  <CalendarIcon className="h-4 w-4 mr-2" />
                  <span>Applied {formatDate(application.applicationDate)}</span>
                </div>
              </div>

              <div className="mt-6">
                <Button
                  onClick={() => handleFollowUp(application.id)}
                  variant="outline"
                  size="sm"
                  className="w-full"
                >
                  Follow Up
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default ApplicationList;
