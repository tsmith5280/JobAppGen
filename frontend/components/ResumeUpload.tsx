import { useState } from "react";

type ParsedProfile = {
  full_name: string;
  job_title: string;
  skills: string[];
  experience: string;
};

export default function ResumeUpload({ onParsed }: { onParsed: (parsed: ParsedProfile) => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [parsed, setParsed] = useState<ParsedProfile | null>(null);
  const [status, setStatus] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    setStatus("Uploading...");

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/resume/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setParsed(data);
    onParsed(data);
    setStatus("Parsed!");
  };

  const handleSave = async () => {
    if (!parsed) return;

    const res = await fetch("http://localhost:8000/profile/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(parsed),
    });

    const data = await res.json();
    setStatus("✅ Profile saved!");
    console.log(data);
  };

  return (
    <div className="space-y-4">
      <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
      <button onClick={handleUpload} className="bg-teal-600 text-white px-4 py-2 rounded">Upload & Parse</button>

      {parsed && (
        <div className="border p-4 rounded bg-zinc-100 dark:bg-zinc-800 text-sm">
          <h3 className="text-lg font-semibold mb-2">Parsed Resume</h3>
          <p><strong>Name:</strong> {parsed.full_name}</p>
          <p><strong>Job Title:</strong> {parsed.job_title}</p>
          <p><strong>Skills:</strong> {Array.isArray(parsed.skills) ? parsed.skills.join(", ") : "N/A"}</p>
          <p><strong>Experience:</strong> {parsed.experience}</p>
          <button onClick={handleSave} className="mt-4 bg-amber-500 text-white px-4 py-2 rounded">Save Profile</button>
        </div>
      )}

      {status && <p className="text-sm italic text-zinc-500">{status}</p>}
    </div>
  );
}
