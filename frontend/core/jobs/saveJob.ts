import { toast } from "sonner";

interface SaveJobProps {
  title: string;
  company: string;
  sourceURL: string;
  resumeVersion: string;
}

export interface JobEntry {
  title: string;
  company: string;
  sourceURL: string;
  resumeUsed: string;
  appliedDate: string;
  followUpSent: boolean;
}

export function saveJob({ title, company, sourceURL, resumeVersion }: SaveJobProps) {
  const newJob: JobEntry = {
    title,
    company,
    sourceURL,
    resumeUsed: resumeVersion,
    appliedDate: new Date().toISOString(),
    followUpSent: false,
  };

  console.log("Saving job:", newJob);
  toast.success("📌 Job saved! We’ll remind you to follow up.");
}
