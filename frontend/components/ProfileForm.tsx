import { useState, useEffect } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";

interface ProfileData {
  full_name: string;
  job_title: string;
  skills: string[];
  experience: string;
}

interface ProfileFormProps {
  onSave: (data: ProfileData) => void;
  profile?: ProfileData | null;
}

export default function ProfileForm({ onSave, profile: initialProfile }: ProfileFormProps) {
  const [profile, setProfile] = useState({
    full_name: "",
    job_title: "",
    skills: "",
    experience: "",
  });

  useEffect(() => {
    if (initialProfile) {
      setProfile({
        full_name: initialProfile.full_name || "",
        job_title: initialProfile.job_title || "",
        skills: (initialProfile.skills || []).join(", "),
        experience: initialProfile.experience || "",
      });
    }
  }, [initialProfile]);

  const handleChange = (key: keyof typeof profile, value: string) => {
    setProfile((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = () => {
    const trimmed: ProfileData = {
      full_name: profile.full_name.trim(),
      job_title: profile.job_title.trim(),
      skills: profile.skills.split(",").map((s) => s.trim()).filter(Boolean),
      experience: profile.experience.trim(),
    };

    if (!trimmed.full_name || !trimmed.job_title) {
      toast.error("Full name and job title are required.");
      return;
    }

    onSave(trimmed);
    toast.success("Profile data updated.", {
      description: "You can now proceed to the dashboard."
    });
  };

  const isValid = profile.full_name.trim() && profile.job_title.trim();

  return (
    <Card>
      <CardHeader>
        <CardTitle>Your Profile</CardTitle>
        <CardDescription>Verify and edit the information parsed from your resume.</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="full_name">Full Name</Label>
          <Input id="full_name" placeholder="e.g. Jane Doe" value={profile.full_name} onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("full_name", e.target.value)} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="job_title">Target Job Title</Label>
          <Input id="job_title" placeholder="e.g. Senior Software Engineer" value={profile.job_title} onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("job_title", e.target.value)} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="skills">Skills</Label>
          <Input id="skills" placeholder="e.g. React, Python, SQL" value={profile.skills} onChange={(e: React.ChangeEvent<HTMLInputElement>) => handleChange("skills", e.target.value)} />
        </div>
        <div className="space-y-2">
          <Label htmlFor="experience">Experience Summary</Label>
          <Textarea id="experience" placeholder="Summarize your key experience..." value={profile.experience} onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => handleChange("experience", e.target.value)} />
        </div>
      </CardContent>
      <CardFooter>
        <Button onClick={handleSave} disabled={!isValid} className="w-full">Save Profile</Button>
      </CardFooter>
    </Card>
  );
}