import { createFileRoute } from "@tanstack/react-router";
import { useMutation } from "@tanstack/react-query";
import { z, ZodError } from "zod";
import { Formik, Form } from "formik";
import { ErrorText } from "@/components/ui/error";

import {
  AuthResetPasswordInputForm,
  AuthResetPasswordResponse,
} from "./schemas";
import { AppInput } from "@/components/form/AppInput";

export const Route = createFileRoute("/auth/password")({
  component: () => <ResetPasswordPage />,
});

interface IResetPasswordInput {
  user_name: string;
  old_password: string;
  new_password: string;
  confirm_password: string;
}

const postResetPassword = async (input: IResetPasswordInput) => {
  const res = await fetch("/api/auth/user:password", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(input),
  });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.msg);
  }
  const data = await res.json();
  return AuthResetPasswordResponse.parseAsync(data);
};

function ResetPasswordPage() {
  // Mutations
  const login_mutation = useMutation<
    z.infer<typeof AuthResetPasswordResponse>,
    Error,
    IResetPasswordInput
  >({
    mutationFn: async (input: IResetPasswordInput) => postResetPassword(input),
  });

  const handleResetPassword = (
    input_data: z.infer<typeof AuthResetPasswordInputForm>
  ) => {
    login_mutation.mutate(input_data);
  };
  return (
    <>
      <div className="flex min-h-full flex-1 flex-col py-12 sm:px-6 lg:px-8">
        <div className="sm:mx-auto sm:w-full sm:max-w-md">
          <h2 className="mt-6 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">
            Reset your password
          </h2>
        </div>

        <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-[480px]">
          <div className="bg-white px-6 py-12 shadow sm:rounded-lg sm:px-12">
            <Formik
              enableReinitialize
              initialValues={{
                user_name: undefined,
                old_password: undefined,
                new_password: undefined,
                confirm_password: undefined,
              }}
              validate={(values) => {
                try {
                  AuthResetPasswordInputForm.parse(values);
                } catch (error) {
                  if (error instanceof ZodError) {
                    return error.formErrors.fieldErrors;
                  }
                }
              }}
              onSubmit={(values) => {
                handleResetPassword(values);
              }}
            >
              <Form className="space-y-1">
                <AppInput
                  className=""
                  name="user_name"
                  placeholder="jdoe@company.com"
                >
                  User name
                </AppInput>
                <AppInput
                  className=""
                  name="old_password"
                  type="password"
                  placeholder="SuperStr0ngP@ssword"
                >
                  Current password
                </AppInput>

                <AppInput
                  className=""
                  name="new_password"
                  type="password"
                  placeholder="SuperStr0ngP@ssword2"
                >
                  New password
                </AppInput>
                <AppInput
                  className=""
                  name="confirm_password"
                  type="password"
                  placeholder="SuperStr0ngP@ssword2"
                >
                  Confirm password
                </AppInput>

                <div className="mt-6 flex justify-end">
                  <button
                    type="submit"
                    className="flex items-center space-x-1 rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                  >
                    <span>Submit</span>
                  </button>
                </div>
                {login_mutation.isError ? (
                  <ErrorText className="flex justify-end py-2">
                    {login_mutation.error.message}
                  </ErrorText>
                ) : null}
              </Form>
            </Formik>
          </div>
        </div>
      </div>
    </>
  );
}
