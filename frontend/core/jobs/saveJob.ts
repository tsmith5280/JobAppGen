import { toast } from "sonner";

interface SaveJobProps {
  title: string;
  company: string;
  url: string;
  resumeVersion: string;
}
export type JobEntry = {
  title: string;
  company: string;
  sourceURL: string;
  resumeUsed: string;
  appliedDate: string;
  followUpSent: boolean;
};

export function saveJob({ title, company, url, resumeVersion }: SaveJobProps) {
  const newJob = {
    title,
    company,
    sourceURL: url,
    resumeUsed: resumeVersion,
    appliedDate: new Date().toISOString(),
    followUpSent: false,
  };

  // 👇 Replace this with your actual store or Supabase logic
  console.log("Saving job:", newJob);

  // 👇 Temporary placeholder toast (replace later with real one)
  alert("📌 Job saved! We’ll remind you to follow up in a few days.");
  toast.success("📌 Job saved! We’ll remind you to follow up.");
}