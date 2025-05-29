import Head from "next/head";

export default function Home() {
  return (
    <>
      <Head>
        <title>Joblight</title>
        <meta name="description" content="Your AI job assistant" />
      </Head>
      <main className="min-h-screen bg-white text-black dark:bg-zinc-900 dark:text-white flex flex-col items-center justify-center p-8">
        <h1 className="text-4xl font-bold mb-4">Welcome to Joblight 💼</h1>
        <p className="text-center max-w-lg">
          Your AI assistant for finding jobs, building resumes, and tracking applications.
        </p>
        <a
          href="/dashboard"
          className="bg-amber-500 hover:bg-amber-600 text-white px-6 py-3 rounded-full shadow transition mt-8"
        >
          Go to Dashboard
        </a>
      </main>
    </>
  );
}
