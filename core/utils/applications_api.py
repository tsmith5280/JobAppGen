from .supabase_client import supabase

def insert_application(user_id, job_title, company, status, date, notes):
    response = supabase.table("applications").insert({
        "user_id": user_id,
        "job_title": job_title,
        "company": company,
        "status": status,
        "date": date,
        "notes": notes
    }).execute()
    return response

def get_user_applications(user_id):
    response = supabase.table("applications") \
        .select("*") \
        .eq("user_id", user_id) \
        .order("date", desc=True) \
        .execute()

    return response.data or []