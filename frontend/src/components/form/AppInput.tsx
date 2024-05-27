import { useState } from "react";
import { Field, ErrorMessage, useField } from "formik";
import { cn } from "@/lib/utils";
import { IoEyeOutline, IoEyeOffOutline } from "react-icons/io5";

interface AppInputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  name: string;
  children: React.ReactNode;
}

interface PasswordEyeProps extends React.HTMLAttributes<HTMLButtonElement> {
  hidePasswordText: boolean;
  onClick: () => void;
}

const PasswordEye = ({ hidePasswordText, onClick }: PasswordEyeProps) => {
  if (hidePasswordText) {
    return (
      <button
        type="button"
        className="absolute inset-y-0 right-0 flex items-center pr-3"
        onClick={onClick}
        tabIndex={-1}
      >
        <IoEyeOffOutline className="h-5 w-5 text-gray-400" aria-hidden="true" />
      </button>
    );
  }
  return (
    <button
      type="button"
      className="absolute inset-y-0 right-0 flex items-center pr-3"
      onClick={onClick}
      tabIndex={-1}
    >
      <IoEyeOutline className="h-5 w-5 text-gray-400" aria-hidden="true" />
    </button>
  );
};

export function AppInput({
  children,
  className,
  onChange,
  ...props
}: AppInputProps) {
  const [hidePasswordText, togglePasswordText] = useState(false);
  const [internalType, setInternalType] = useState(props.type);
  const [field, meta, helpers] = useField(props.name);

  const onTogglePasswordText = () => {
    setInternalType((prev) => (prev === "password" ? "text" : "password"));
    togglePasswordText((prev) => !prev);
  };

  if (props.type === "password") {
    const { type, ...rest } = props;
    return (
      <div className="text-sm py-2">
        <label
          htmlFor={props.name}
          className="block text-sm font-medium leading-6 text-gray-900"
        >
          {children}
        </label>
        <div className="relative">
          <Field
            className={cn(
              "block w-full rounded-md border-0 px-3 py-2 h-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
              meta.error && meta.touched
                ? "text-red-900 ring-1 ring-inset ring-red-300 placeholder:text-red-300"
                : "",
              className
            )}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
              helpers.setValue(e.target.value);
              onChange ? onChange(e) : null;
            }}
            onBlur={() => helpers.setTouched(true)}
            type={internalType}
            {...rest}
          />

          <PasswordEye
            hidePasswordText={hidePasswordText}
            onClick={onTogglePasswordText}
          />
        </div>
        <p
          className={cn(
            "text-xs",
            meta.error && meta.touched ? "text-red-500" : ""
          )}
        >
          <ErrorMessage name={props.name} />
        </p>
      </div>
    );
  }

  return (
    <div className="text-sm py-2">
      <label
        htmlFor={props.name}
        className="block text-sm font-medium leading-6 text-gray-900"
      >
        {children}
      </label>
      <div className="relative">
        <Field
          className={cn(
            "block w-full rounded-md border-0 px-3 py-2 h-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
            meta.error && meta.touched
              ? "text-red-900 ring-1 ring-inset ring-red-300 placeholder:text-red-300"
              : "",
            className
          )}
          onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
            helpers.setValue(e.target.value);
            onChange ? onChange(e) : null;
          }}
          onBlur={() => helpers.setTouched(true)}
          {...props}
        />
      </div>
      <p
        className={cn(
          "text-xs",
          meta.error && meta.touched ? "text-red-500" : ""
        )}
      >
        <ErrorMessage name={props.name} />
      </p>
    </div>
  );
}
