import React from "react";

export interface ParsedResumeProps {
  name: string;
  jobTitle: string;
  skills: string[];
  experience: string[];
}


export default function ParsedResume({
  name,
  jobTitle,
  skills,
  experience,
}: ParsedResumeProps) {
  return (
    <div className="bg-zinc-900 p-4 rounded-lg border border-zinc-700">
      <p><strong>Name:</strong> {name}</p>
      <p><strong>Job Title:</strong> {jobTitle}</p>

      <p><strong>Skills:</strong></p>
      <ul className="list-disc list-inside text-sm ml-4">
        {skills.map(skill => (
          <li key={skill}>{skill}</li>
        ))}
      </ul>

      <p><strong>Experience:</strong></p>
      <ul className="list-disc list-inside text-sm ml-4">
        {experience.map((exp, i) => (
          <li key={i}>{exp}</li>
        ))}
      </ul>
    </div>
  );
}