import { useState } from "react";
import Layout from "@/components/Layout";
import ResumeUpload from "@/components/ResumeUpload";
import ProfileForm from "@/components/ProfileForm";
import JobTargetForm from "@/components/JobTargetForm";

const DashboardContent = () => (
  <>
    <h2 className="text-3xl font-bold text-amber-600 mb-4">Dashboard</h2>
    <p>Welcome to your job search dashboard.</p>
  </>
);

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [resume, setResume] = useState("");
  const [score, setScore] = useState(null);
  const [recommendation, setRecommendation] = useState("");

  async function generateResume(target: any) {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/generate_resume/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ profile, target }),
    });
    const data = await res.json();
    setResume(data.resume);
    setScore(data.score);
    setRecommendation(data.recommendation);
  }

  return (
    <Layout>
      <div className="p-8 space-y-4">
        <DashboardContent />
        <ResumeUpload />
        <ProfileForm onSave={setProfile} />
        {profile && <JobTargetForm onGenerate={generateResume} />}

        {resume && (
          <div className="bg-zinc-800 text-white p-4 rounded">
            <h2 className="text-lg font-semibold">Generated Resume</h2>
            <pre>{resume}</pre>
            {score !== null && <p>Match Score: <strong>{score}%</strong></p>}
            {recommendation && <p className="text-red-400 italic">{recommendation}</p>}
          </div>
        )}
      </div>
    </Layout>
  );
}
