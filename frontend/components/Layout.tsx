import { ReactNode } from "react";

type LayoutProps = {
  children: ReactNode;
};

export default function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-white dark:bg-zinc-900 text-zinc-900 dark:text-white p-6">
      <header className="mb-6 border-b pb-4">
        <h1 className="text-2xl font-bold text-teal-600 dark:text-amber-400">Joblight</h1>
      </header>
      <main>{children}</main>
    </div>
  );
}
