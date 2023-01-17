import { Outlet } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import AuthRefresh from "./services/AuthRefresh";

const App = () => {
  return (
    <AuthRefresh>
      <MainLayout>
        <Outlet />
      </MainLayout>
    </AuthRefresh>
  );
};

export default App;
