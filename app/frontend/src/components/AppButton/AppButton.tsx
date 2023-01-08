import React, { useMemo } from "react";
import AppSpinner from "@/components/AppSpinner";

interface ButtonProps extends React.ComponentPropsWithoutRef<"button"> {
  children: string | JSX.Element;
  isLoading?: boolean;
  transparent?: boolean;
}

const default_props = {
  isLoading: false,
  transparent: false,
};

function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const AppButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (props, ref) => {
    const { children, isLoading, transparent, className, ...rest } = props;
    const bgClasses = useMemo(() => {
      return transparent
        ? "bg-transparent text-primary-600 border-2 border-primary-600 hover:ring-primary-600 disabled:text-gray-600 disabled:border-gray-600 disabled:ring-0"
        : "bg-primary-600 text-white border-2 border-primary-600 hover:ring-primary-600 disabled:bg-gray-600 disabled:border-gray-600 disabled:ring-0";
    }, [transparent]);

    return (
      <button
        ref={ref}
        disabled={isLoading ?? false}
        {...rest}
        className={classNames(
          "px-8 py-2 rounded-lg transition duration-300 ease",
          "hover:ring-2 hover:ring-offset-2 flex items-center",
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
