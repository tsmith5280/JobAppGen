const DashboardContent = () => (
  <>
    <h2 className="text-3xl font-bold text-amber-600 mb-4">Dashboard</h2>
    <p>Welcome to your job search dashboard.</p>
  </>
);

export default function Dashboard() {
  return (
    <Layout>
      <DashboardContent />
    </Layout>
  );
}
