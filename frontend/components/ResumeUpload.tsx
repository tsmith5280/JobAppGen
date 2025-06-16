import { useState } from "react";

export type ParsedProfile = {
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
  const selected = e.target.files?.[0];
  if (!selected) return;

  const allowedTypes = ["application/pdf", 
                        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"];

  if (!allowedTypes.includes(selected.type)) {
    setStatus("❌ Only PDF or DOCX files are allowed.");
    return;
  }

  setFile(selected);
  setStatus(""); // clear status
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

if (!res.ok) {
  setStatus("❌ Upload failed.");
  return;
}

const data = await res.json();

// 🔍 Validate parsed structure
if (
  !data.full_name ||
  !data.job_title ||
  !Array.isArray(data.skills) ||
  typeof data.experience !== "string"
) {
  setStatus("❗️Parsing incomplete — resume may be unsupported or missing info.");
  return;
}

setParsed(data);
onParsed(data);
setStatus("✅ Parsed!");

  };
  const handleSave = async () => {
    if (!parsed) return;
    if (
  !parsed.full_name ||
  !parsed.job_title ||
  !Array.isArray(parsed.skills) ||
  typeof parsed.experience !== "string"
) {
  setStatus("⚠️ Profile data is incomplete or malformed.");
  return;
}
    const res = await fetch("http://localhost:8000/profile/", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(parsed),
});

if (!res.ok) {
  setStatus("❌ Save failed.");
  return;
}

const data = await res.json();
setStatus("✅ Profile saved!");

    console.log(data);
  };

  return (
    <div className="space-y-4">
      <input type="file" accept=".pdf,.docx" onChange={handleFileChange} />
      <button
  onClick={handleUpload}
  className="bg-teal-600 text-white px-4 py-2 rounded"
  disabled={status === "Uploading..."}
>
  Upload & Parse
</button>


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
