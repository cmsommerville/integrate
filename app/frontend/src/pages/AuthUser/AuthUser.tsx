import AppButton from "@/components/AppButton";
import { authServerAxiosInstance } from "@/services/axios";

const AuthUser = () => {
  const onClick = async () => {
    try {
      await authServerAxiosInstance.post("/login", {
        body: JSON.stringify({
          user_name: "superuser",
          password: "hello_world",
        }),
      });
    } catch (err) {
      console.log(err);
    }
  };
  return <AppButton onClick={onClick}>Login</AppButton>;
};

export default AuthUser;
