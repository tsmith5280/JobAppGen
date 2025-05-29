import { useState } from "react";

export default function ProfileForm({ onSave }: { onSave: (data: any) => void }) {
  const [profile, setProfile] = useState({
    full_name: "",
    job_title: "",
    skills: "",
    experience: ""
  });

  const handleChange = (key: string, value: string) =>
    setProfile((prev) => ({ ...prev, [key]: value }));

  return (
    <div className="space-y-3 p-4 border rounded bg-zinc-900">
      <h2 className="text-xl font-bold">Your Profile</h2>
      <input
        className="bg-zinc-800 text-white border p-2 rounded w-full"
        placeholder="Full Name"
        value={profile.full_name}
        onChange={(e) => handleChange("full_name", e.target.value)}
      />
      <input
        className="bg-zinc-800 text-white border p-2 rounded w-full"
        placeholder="Job Title"
        value={profile.job_title}
        onChange={(e) => handleChange("job_title", e.target.value)}
      />
      <input
        className="bg-zinc-800 text-white border p-2 rounded w-full"
        placeholder="Skills (comma-separated)"
        value={profile.skills}
        onChange={(e) => handleChange("skills", e.target.value)}
      />
      <textarea
        className="bg-zinc-800 text-white border p-2 rounded w-full"
        placeholder="Experience"
        value={profile.experience}
        onChange={(e) => handleChange("experience", e.target.value)}
      />
      <button
        onClick={() =>
          onSave({
            ...profile,
            skills: profile.skills.split(",").map((s) => s.trim())
          })
        }
        className="bg-amber-500 px-4 py-2 rounded text-white"
      >
        Save Profile
      </button>
    </div>
  );
}
