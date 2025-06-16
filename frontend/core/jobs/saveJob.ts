import { SupabaseClient } from "@supabase/supabase-js";
import { toast } from "sonner";

interface SaveJobProps {
  job_title: string;
  company_name: string;
  status?: string;
}

export async function saveJobToDatabase(
  supabase: SupabaseClient,
  jobData: SaveJobProps
) {
  try {
    const { error } = await supabase.from("applications").insert([
      {
        job_title: jobData.job_title,
        company_name: jobData.company_name,
        status: jobData.status || "Applied",
      },
    ]);

    if (error) {
      // Let the calling function know something went wrong.
      throw error;
    }

    toast.success("📌 Job saved to your dashboard!");

  } catch (error: any) {
    console.error("Error saving job:", error);
    toast.error("Failed to save job", {
      description: error.message,
    });
  }
}