import PublicDashboard from '../components/PublicDashboard';
import PersonalDashboard from '../components/PersonalDashboard';

const Dashboard = () => {
  const isLoggedIn = !!localStorage.getItem('token');
  
  return isLoggedIn ? <PersonalDashboard /> : <PublicDashboard />;
};

export default Dashboard;
