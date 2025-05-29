import { useState } from "react";
import ProfileForm from "@/components/ProfileForm";
import JobTargetForm from "@/components/JobTargetForm";

export default function ResumeGenerator() {
  const [profile, setProfile] = useState<any>(null);
  const [resume, setResume] = useState("");
  const [score, setScore] = useState<number | null>(null);
  const [warning, setWarning] = useState("");

  async function generateResume(target: any) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/generate_resume/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile, target })
    });
    const data = await res.json();
    setResume(data.resume);
    setScore(data.score);
    setWarning(data.recommendation);
  }

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">AI Resume Generator</h1>
      <ProfileForm onSave={setProfile} />
      {profile && <JobTargetForm onGenerate={generateResume} />}
      {resume && (
        <div className="mt-6 p-4 border rounded bg-zinc-800 text-white">
          <h2 className="text-xl font-bold mb-2">Generated Resume</h2>
          <pre>{resume}</pre>
          {score !== null && <p className="mt-2">Match Score: <strong>{score}%</strong></p>}
          {warning && <p className="mt-1 text-red-400 italic">{warning}</p>}
        </div>
      )}
    </div>
  );
}
