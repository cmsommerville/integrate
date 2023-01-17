import AppButton from "@/components/AppButton";

const AuthUser = () => {
  const onClick = () => {
    fetch(`/api/auth/login`, {
      method: "POST",
      body: JSON.stringify({
        user_name: "superuser",
        password: "hello_world",
      }),
      headers: {
        "Content-Type": "application/json",
      },
    });
  };
  return <AppButton onClick={onClick}>Login</AppButton>;
};

export default AuthUser;
