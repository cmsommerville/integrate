import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useMutation } from "@tanstack/react-query";
import { FaCircleExclamation } from "react-icons/fa6";
import { UserType } from "../../types/auth";
import { useAuthContext } from "@/providers/AuthContext";

import { Button } from "@/components/ui/button";
import { LoadingSpinner } from "@/components/ui/spinner";

interface ILoginRequiredInput {
  user_name: string;
  password: string;
}

interface ILoginResponseSuccess {
  status: "success";
  msg: string;
  data: UserType;
}
interface ILoginResponseError {
  status: "error";
  msg: string;
}

type ILoginResponse = ILoginResponseSuccess | ILoginResponseError;

const postLogin = async ({
  user_name,
  password,
}: ILoginRequiredInput): Promise<ILoginResponse> => {
  const res = await fetch("/api/auth/user/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_name, password }),
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.msg);
  }
  return res.json();
};

function LoginPage() {
  const { setUser } = useAuthContext();
  const navigate = useNavigate({ from: "/auth/login" });

  // Mutations
  const login_mutation = useMutation<
    ILoginResponse,
    Error,
    ILoginRequiredInput
  >({
    mutationFn: async (input: ILoginRequiredInput) => postLogin(input),
    onSuccess: (data) => {
      if (data.status === "success") {
        setUser(data.data);
        navigate({ to: "/" });
      }
    },
  });

  const handleLogin = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    const formElements = form.elements as typeof form.elements & {
      user_name: { value: string };
      password: { value: string };
    };
    const user_name = formElements.user_name.value;
    const password = formElements.password.value;
    login_mutation.mutate({ user_name, password });
  };
  return (
    <>
      <div className="flex min-h-full flex-1 flex-col py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <h2 className="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Sign in to your account
          </h2>
        </div>

        <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-[480px]">
          <div className="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
            <form className="space-y-6" onSubmit={(e) => handleLogin(e)}>
              <div>
                <label
                  htmlFor="user_name"
                  className="block text-sm font-medium leading-6 text-gray-900"
                >
                  User name
                </label>
                <div className="mt-2">
                  <input
                    id="user_name"
                    name="user_name"
                    type="text"
                    autoComplete="user_name"
                    required
                    className="block w-full rounded-md border-0 py-1.5 pl-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="block text-sm font-medium leading-6 text-gray-900"
                >
                  Password
                </label>
                <div className="mt-2">
                  <input
                    id="password"
                    name="password"
                    type="password"
                    autoComplete="current-password"
                    required
                    className="block w-full rounded-md border-0 py-1.5 pl-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <input
                    id="remember-me"
                    name="remember-me"
                    type="checkbox"
                    className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                  />
                  <label
                    htmlFor="remember-me"
                    className="ml-3 block text-sm leading-6 text-gray-900"
                  >
                    Remember me
                  </label>
                </div>

                <div className="text-sm leading-6">
                  <a
                    href="#"
                    className="font-semibold text-indigo-600 hover:text-indigo-500"
                  >
                    Forgot password?
                  </a>
                </div>
              </div>

              <div>
                <Button
                  type="submit"
                  variant="default"
                  className="flex w-full justify-center bg-indigo-600 hover:bg-indigo-700 text-white focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Sign in
                  {login_mutation.isPending ? (
                    <LoadingSpinner size={20} className="ml-2" />
                  ) : null}
                </Button>
                {login_mutation.isError ? (
                  <p
                    className="mt-2 text-sm text-red-600 flex items-center"
                    id="login-error"
                  >
                    <FaCircleExclamation className="inline-block mr-1" />{" "}
                    {login_mutation.error?.message || "An error occurred"}
                  </p>
                ) : undefined}
              </div>
            </form>
          </div>
        </div>
      </div>
    </>
  );
}

export const Route = createFileRoute("/auth/login")({
  component: () => <LoginPage />,
});
