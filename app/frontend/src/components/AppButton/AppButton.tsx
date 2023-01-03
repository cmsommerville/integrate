import React from "react";
import AppSpinner from "@/components/AppSpinner";

interface ButtonProps extends React.ComponentPropsWithoutRef<"button"> {
  children: string;
  isLoading?: boolean;
}

function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const AppButton = ({ children, isLoading, ...props }: ButtonProps) => {
  return (
    <button
      disabled={isLoading ?? false}
      {...props}
      className={classNames(
        "bg-primary-600 px-8 py-2 rounded-lg text-white transition duration-300 ease",
        "hover:ring-2 hover:ring-offset-2 hover:ring-primary-600",
        "disabled:bg-gray-600 disabled:ring-0",
        props.className
      )}
    >
      {isLoading ? <AppSpinner /> : children}
    </button>
  );
};

export default AppButton;
