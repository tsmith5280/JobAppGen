import { useUser, useSupabaseClient, User } from "@supabase/auth-helpers-react";
import { useRouter } from "next/router";
import { useEffect, useState, ReactElement } from "react";
import DashboardLayout from "@/components/layout/DashboardLayout";
import StatsOverview from "@/components/features/StatsOverview";
import ApplicationList from "@/components/features/ApplicationList";
import { NextPageWithLayout } from "./_app";

interface Profile {
  full_name?: string;
  avatar_url?: string;
  // Add any other profile properties here in the future
}

interface DashboardContentProps {
  profile: Profile;
  user: User | null;
}

const DashboardContent = ({ profile, user }: DashboardContentProps) => {
  return (
    <>
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <p className="text-muted-foreground">Welcome back, {profile.full_name || user?.email || 'User'}</p>
      
      <div className="mt-8 space-y-8">
        <StatsOverview />
        <ApplicationList />
      </div>
    </>
  );
};

const DashboardPage: NextPageWithLayout = () => {
  const supabase = useSupabaseClient();
  const user = useUser();
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState<Profile | null>(null);

  useEffect(() => {
    if (user) {
      const checkProfile = async () => {
        const { data } = await supabase.from('profiles').select('*').eq('id', user.id).single();
        if (data && data.setup_complete) {
          setProfile(data);
        } else {
          router.push('/setup');
        }
        setLoading(false);
      };
      checkProfile();
    } else if (!loading) {
      const timer = setTimeout(() => {
        if(!user) router.push('/login');
      }, 100);
      return () => clearTimeout(timer);
    }
  }, [user, router, supabase, loading]);

  if (loading || !profile) {
    return <div className="flex h-screen items-center justify-center bg-background"><p>Loading...</p></div>;
  }
  
  return <DashboardContent profile={profile} user={user} />;
};

DashboardPage.getLayout = function getLayout(page: ReactElement) {
  return (
    <DashboardLayout profile={(page.props as DashboardContentProps).profile}>
      {page}
    </DashboardLayout>
  );
};

export default DashboardPage;