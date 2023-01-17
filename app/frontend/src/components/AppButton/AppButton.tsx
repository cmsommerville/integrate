import React, { useMemo } from "react";
import AppSpinner from "@/components/AppSpinner";

interface ButtonProps extends React.ComponentPropsWithoutRef<"button"> {
  children: string | JSX.Element;
  isLoading?: boolean;
  transparent?: boolean;
  flat?: boolean;
}

const default_props = {
  isLoading: false,
  transparent: false,
  flat: false,
};

function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const AppButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (props, ref) => {
    const { children, isLoading, transparent, flat, className, ...rest } =
      props;
    const bgClasses = useMemo(() => {
      if (transparent) {
        return classNames(
          "px-8 py-2 flex items-center",
          "bg-transparent text-primary-600 border-2 border-primary-600",
          "hover:ring-primary-500",
          "disabled:text-gray-400 disabled:border-gray-400 disabled:ring-0"
        );
      }
      if (flat) {
        return classNames(
          "bg-transparent text-inherit border-0",
          "hover:ring-0 hover:bg-transparent",
          "disabled:text-gray-400 disabled:ring-0"
        );
      }
      return classNames(
        "px-8 py-2 flex items-center",
        "bg-primary-600 text-white border-2 border-primary-600",
        "hover:ring-primary-600 hover:bg-primary-600",
        "disabled:bg-gray-400 disabled:border-gray-400 disabled:ring-0"
      );
    }, [transparent, flat]);

    return (
      <button
        ref={ref}
        disabled={isLoading ?? false}
        {...rest}
        className={classNames(
          "rounded-lg transition duration-300 ease",
          "hover:ring-2 hover:ring-offset-2",
          bgClasses,
          className
        )}
      >
        {isLoading ? <AppSpinner /> : children}
      </button>
    );
  }
);

AppButton.defaultProps = default_props;

export default AppButton;
