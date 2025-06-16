import { useState } from "react";
import { useUser, useSupabaseClient } from "@supabase/auth-helpers-react";
import { useRouter } from "next/router";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import ResumeUpload from "@/components/ResumeUpload";
import ProfileForm from "@/components/ProfileForm";

export default function SetupPage() {
  const supabase = useSupabaseClient();
  const user = useUser();
  const router = useRouter();
  
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState<any>(null);
  const [parsedResume, setParsedResume] = useState<any>(null);

  async function handleFinishSetup() {
    if (!user || !profileData) {
      toast.error("Profile data is missing. Please save it first.");
      return;
    }

    setLoading(true);
    toast.loading("Finalizing your account...");

    const { error } = await supabase
      .from('profiles')
      .update({
        full_name: profileData.full_name,
        job_title: profileData.job_title,
        skills: profileData.skills,
        experience: profileData.experience,
        setup_complete: true,
      })
      .eq('id', user.id);

    toast.dismiss();

    if (error) {
      setLoading(false);
      console.error("Error updating profile:", error);
      toast.error("Failed to save profile.", {
        description: error.message || "An unknown database error occurred.",
      });
    } else {
      toast.success("Setup complete! Redirecting...");
      router.push('/dashboard');
    }
  }

  return (
    <div className="container mx-auto max-w-3xl p-4 sm:p-8">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Welcome to Joblight!</h1>
        <p className="text-muted-foreground mt-2">Let's set up your profile. Start by uploading your resume.</p>
      </div>

      <div className="space-y-8">
        <ResumeUpload onParsed={setParsedResume} />
        <ProfileForm onSave={setProfileData} profile={parsedResume} />
        
        {profileData && (
          <Button
            onClick={handleFinishSetup}
            disabled={loading}
            size="lg"
            className="w-full"
          >
            {loading ? "Please wait..." : "Finish Setup & Go to Dashboard"}
          </Button>
        )}
      </div>
    </div>
  );
}