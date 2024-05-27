import { createContext, useContext, useState } from "react";
import { UserType } from "@/types/auth";

interface IProps {
  children: React.ReactNode;
}

export const AuthContext = createContext<{
  user: UserType | undefined;
  setUser: React.Dispatch<React.SetStateAction<UserType | undefined>>;
}>({
  user: undefined,
  setUser: (user) => {
    return user;
  },
});

export const AuthProvider = ({ children }: IProps) => {
  const [user, setUser] = useState<UserType | undefined>();

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuthContext = () => {
  return useContext(AuthContext);
};
