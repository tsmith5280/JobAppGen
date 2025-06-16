import { useState } from "react";

export default function JobTargetForm({
  onGenerate
}: {
  onGenerate: (target: any) => void;
}) {
  const [target, setTarget] = useState({
    job_title: "",
    company: "",
    description: ""
  });

  return (
    <div className="space-y-3 p-4 border rounded bg-zinc-900 mt-6">
      <h2 className="text-xl font-bold">Target Job</h2>
      <input
        className="bg-zinc-800 text-white border p-2 rounded w-full"
        placeholder="Target Job Title"
        value={target.job_title}
        onChange={(e) => setTarget({ ...target, job_title: e.target.value })}
      />
      <input
        className="bg-zinc-800 text-white border p-2 rounded w-full"
        placeholder="Company Name"
        value={target.company}
        onChange={(e) => setTarget({ ...target, company: e.target.value })}
      />
      <textarea
        className="bg-zinc-800 text-white border p-2 rounded w-full"
        placeholder="Job Description"
        value={target.description}
        onChange={(e) => setTarget({ ...target, description: e.target.value })}
      />
      <button
        onClick={() => onGenerate(target)}
        className="bg-teal-600 px-4 py-2 rounded text-white"
      >
        Generate Resume
      </button>
    </div>
  );
}
