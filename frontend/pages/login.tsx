import { useEffect } from "react";
import { useUser } from "@supabase/auth-helpers-react";
import { useRouter } from "next/router";
import { createClientComponentClient } from "@supabase/auth-helpers-nextjs";

export default function LoginPage() {
  const supabase = createClientComponentClient();
  const user = useUser();
  const router = useRouter();

  useEffect(() => {
    if (user) router.push("/dashboard");
  }, [user]);

  const handleLogin = async () => {
    await supabase.auth.signInWithOAuth({
      provider: "github", 
    });
  };

  return (
    <div className="p-8 text-center">
      <h1 className="text-2xl font-bold mb-4">Log in to Joblight</h1>
      <button
        onClick={handleLogin}
        className="bg-amber-500 text-white px-4 py-2 rounded hover:bg-amber-600 transition"
      >
        Sign in with GitHub
      </button>
    </div>
  );
}
