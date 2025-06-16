[{
	"resource": "/C:/...Projects/GitHub/JobAppGen/frontend/pages/api/auth/callback.ts",
	"owner": "typescript",
	"code": "2724",
	"severity": 8,
	"message": "'\"@supabase/auth-helpers-nextjs\"' has no exported member named 'supabaseServerClient'. Did you mean 'SupabaseClient'?",
	"source": "ts",
	"startLineNumber": 2,
	"startColumn": 10,
	"endLineNumber": 2,
	"endColumn": 30
}]
import { createPagesServerClient } from "@supabase/auth-helpers-nextjs";
import type { NextApiRequest, NextApiResponse } from "next";

export default async function callback(req: NextApiRequest, res: NextApiResponse) {
  const supabase = createPagesServerClient({ req, res });
  await supabase.auth.exchangeCodeForSession(req.url!);
  res.redirect("/dashboard");
}
