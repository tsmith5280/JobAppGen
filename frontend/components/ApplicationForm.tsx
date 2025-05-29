import { useState } from "react";

export default function ApplicationForm({ onSubmitSuccess }: { onSubmitSuccess: () => void }) {
  const [form, setForm] = useState({
    job_title: "",
    company: "",
    status: "Saved",
    date: new Date().toISOString().split("T")[0],
    notes: "",
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const res = await fetch("http://localhost:8000/applications/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    console.log(data);
    onSubmitSuccess(); // Trigger list refresh
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input name="job_title" placeholder="Job Title" className="w-full p-2 border rounded" onChange={handleChange} />
      <input name="company" placeholder="Company" className="w-full p-2 border rounded" onChange={handleChange} />
      <select name="status" className="w-full p-2 border rounded" onChange={handleChange}>
        {["Saved", "Applied", "Interviewing", "Rejected", "Offer"].map(status => (
          <option key={status}>{status}</option>
        ))}
      </select>
      <input type="date" name="date" className="w-full p-2 border rounded" onChange={handleChange} />
      <textarea name="notes" placeholder="Notes" className="w-full p-2 border rounded" onChange={handleChange} />
      <button type="submit" className="bg-teal-600 text-white px-4 py-2 rounded">Submit</button>
    </form>
  );
}
