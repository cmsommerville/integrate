import { useEffect } from "react";
import { refreshAxiosInstance } from "@/services/axios";

// User has switched back to the tab
const onVisibilityChange = async () => {
  if (document.visibilityState === "visible") {
    const data = await refreshAxiosInstance.post("/api/auth/refresh");
    console.log(data.data);
  }
};

interface Props {
  children: JSX.Element;
}

const AuthRefresh = (props: Props) => {
  useEffect(() => {
    window.addEventListener("visibilitychange", onVisibilityChange);
    return () => {
      window.removeEventListener("visibilitychange", onVisibilityChange);
    };
  }, []);

  return <>{props.children}</>;
};

export default AuthRefresh;
