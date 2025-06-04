import { useState, useEffect } from "react";
import Layout from "@/components/Layout";
import ResumeUpload from "@/components/ResumeUpload";
import ProfileForm from "@/components/ProfileForm";
import JobTargetForm from "@/components/JobTargetForm";
import ParsedResume from "@/components/ParsedResume";
import type { ParsedProfile } from "@/components/ResumeUpload";
import type { ParsedResumeProps } from "@/components/ParsedResume";
import type { JobEntry } from "@/core/jobs/saveJob";
import { saveJob } from "@/core/jobs/saveJob";

export default function Dashboard() {
  const [profile, setProfile] = useState<ParsedProfile | null>(null);
  const [parsedResume, setParsedResume] = useState<ParsedProfile | null>(null);
  const [generatedResume, setGeneratedResume] = useState<string>("");
  const [score, setScore] = useState<number | null>(null);
  const [recommendation, setRecommendation] = useState("");

  const [savedJobs, setSavedJobs] = useState<JobEntry[]>(() => {
  if (typeof window !== "undefined") {
    const saved = localStorage.getItem("jobTracker");
    return saved ? JSON.parse(saved) : [];
  }
  return [];
});


  useEffect(() => {
    localStorage.setItem("jobTracker", JSON.stringify(savedJobs));
  }, [savedJobs]);

  function handleSaveJob() {
    const mockJob = {
      title: profile?.job_title ?? "Unknown Role",
      company: "Unknown Company",
      sourceURL: "https://example.com/job-posting",
      resumeUsed: parsedResume?.full_name ?? "Unknown",
    };

    saveJob({
      ...mockJob,
      resumeVersion: mockJob.resumeUsed,
    });

    const newEntry: JobEntry = {
      ...mockJob,
      appliedDate: new Date().toISOString(),
      followUpSent: false,
    };

    setSavedJobs(prev => [...prev, newEntry]);
  }

  async function generateResume(target: any) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/generate_resume/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile, target }),
    });

    const data = await res.json();
    setGeneratedResume(data.resume);
    setScore(data.score);
    setRecommendation(data.recommendation);
  }

  return (
    <div className="p-8 space-y-4">
      <h2 className="text-3xl font-bold text-amber-600 mb-4">Dashboard</h2>
      <p>Welcome to your job search dashboard.</p>

      <ResumeUpload onParsed={setParsedResume} />
      <ProfileForm onSave={setProfile} profile={profile} />
      {profile && <JobTargetForm onGenerate={generateResume} />}

      {parsedResume && (
        <ParsedResume
          name={parsedResume.full_name}
          jobTitle={parsedResume.job_title}
          skills={parsedResume.skills}
          experience={[parsedResume.experience]}
        />
      )}

      {generatedResume && (
        <div className="bg-zinc-800 text-white p-4 rounded">
          <h2 className="text-lg font-semibold">Generated Resume</h2>
          <pre>{generatedResume}</pre>
          <p className="mt-2 text-sm">📩 Save this job for reminders later?</p>
          <button
            onClick={handleSaveJob}
            className="mt-1 bg-amber-500 text-white px-4 py-2 rounded hover:bg-amber-600 transition"
          >
            Save Job
          </button>

          {savedJobs.length > 0 && (
            <div className="mt-6 bg-zinc-900 p-4 rounded border border-zinc-700">
              <h3 className="text-lg font-semibold mb-2 text-teal-400">Saved Jobs</h3>
              <ul className="list-disc list-inside space-y-1 text-sm">
                {savedJobs.map((job, i) => (
                  <li key={i}>
                    <strong>{job.title}</strong> at {job.company} —{" "}
                    <span className="text-zinc-400">
                      {new Date(job.appliedDate).toLocaleDateString()}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {score !== null && <p>Match Score: <strong>{score}%</strong></p>}
          {recommendation && <p className="text-red-400 italic">{recommendation}</p>}
        </div>
      )}
    </div>
  );
}
