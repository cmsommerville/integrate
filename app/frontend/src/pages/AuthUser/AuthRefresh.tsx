import { refreshAccessToken } from "@/services/axios";

const AuthRefresh = () => {
  const refreshHandler = async () => {
    const data = await refreshAccessToken();
  };

  return <button onClick={refreshHandler}>Refresh</button>;
};

export default AuthRefresh;
