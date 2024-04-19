"use client";
import { classNames } from "@/utils";

interface Props extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  invalid?: boolean;
  variant?: "primary" | "primary-transparent" | "dark-transparent";
}

export default function AppButton({
  children,
  className,
  invalid,
  variant,
  ...props
}: Props) {
  let classes = "";
  switch (variant) {
    case "primary-transparent": {
      classes =
        "bg-transparent text-primary-500 ring-2 ring-primary-500 hover:bg-primary-50 hover:text-primary-600 hover:ring-primary-600";
      break;
    }
    case "dark-transparent": {
      classes =
        "bg-transparent text-gray-700 ring-2 ring-inset ring-gray-700 hover:bg-gray-700 hover:text-white hover:ring-gray-700";
      break;
    }
    default: {
      classes =
        "bg-primary-600 text-white ring-2 ring-inset ring-primary-600 hover:bg-primary-500 hover:ring-primary-500";
      break;
    }
  }
  return (
    <button
      className={classNames(
        "h-10 text-[0.9rem] font-medium scale-100 shadow shadow-gray-400 rounded-md py-[0.4rem] px-4 transition duration-100 ease",
        "active:scale-[97%] active:shadow-sm",
        invalid ? "animate-wiggle" : "",
        classes,
        className ?? ""
      )}
      {...props}
    >
      {children}
    </button>
  );
}
