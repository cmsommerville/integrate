import axios from "@/services/axios";

const AuthRefresh = () => {
  const refreshHandler = async () => {
    const data = await axios.post("/api/auth/refresh");
    console.log("Complete");
  };

  return <button onClick={refreshHandler}>Refresh</button>;
};

export default AuthRefresh;
