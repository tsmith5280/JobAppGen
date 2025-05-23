from .supabase_client import supabase

def get_user_profile(user_id):
    response = supabase.table("user_profile") \
        .select("*") \
        .eq("user_id", user_id) \
        .single() \
        .execute()
    return response.data if response.data else None

def upsert_user_profile(user_id, profile):
    response = supabase.table("user_profile").upsert({
        "user_id": user_id,
        "full_name": profile.get("full_name", ""),
        "job_title": profile.get("job_title", ""),
        "skills": profile.get("skills", []),
        "experience": profile.get("experience", "")
    }).execute()
    return response
