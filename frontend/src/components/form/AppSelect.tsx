import { Field, ErrorMessage, useField } from "formik";
import { cn } from "@/lib/utils";
import { IoMdClose } from "react-icons/io";
import { ILabelValue } from "@/types";
import { useEffect } from "react";

interface AppSelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  name: string;
  label: string;
  placeholder?: string;
  options: ILabelValue[];
  showClearSelection?: boolean;
}

export function AppSelect({
  label,
  options,
  placeholder,
  className,
  name,
  onChange,
  disabled,
  showClearSelection,
  ...props
}: AppSelectProps) {
  const [field, meta, helpers] = useField(name);

  useEffect(() => {
    if (options.length === 1 && !field.value) {
      helpers.setValue(options[0].value);
    }
  }, [options, field.value, helpers]);

  // user must want to show the button
  // there must also be more than one option
  const showClearButton = showClearSelection && options.length > 1;

  return (
    <div className="text-sm py-2">
      <label
        htmlFor={name}
        className="relative block text-sm font-medium leading-6 text-gray-900"
      >
        {label}
      </label>
      <div className={cn("relative", className)}>
        <Field
          component="select"
          name={name}
          value={field.value || ""}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) => {
            helpers.setValue(e.target.value);
            onChange ? onChange(e) : null;
          }}
          onBlur={() => helpers.setTouched(true)}
          disabled={disabled}
          className={cn(
            "block w-full rounded-md border-0 px-3 py-1.5 h-10 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
            meta.error && meta.touched
              ? "text-red-900 ring-1 ring-inset ring-red-300 placeholder:text-red-300"
              : ""
          )}
          {...props}
        >
          <option hidden key={""} value="">
            {placeholder ?? "Select an option"}
          </option>
          {options.map((opt) => {
            return (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            );
          })}
        </Field>

        {showClearButton ? (
          <button
            type="button"
            className={cn(
              "absolute top-1/2 -translate-y-1/2 right-5 h-4 w-4 text-[#d1d5db]",
              disabled ? "cursor-default" : "cursor-pointer"
            )}
            onClick={() => {
              if (disabled) return;
              helpers.setValue(undefined);
              helpers.setTouched(false);
            }}
          >
            <IoMdClose />
          </button>
        ) : null}
      </div>
      <p
        className={cn(
          "text-xs",
          meta.error && meta.touched ? "text-red-500" : ""
        )}
      >
        <ErrorMessage name={name} />
      </p>
    </div>
  );
}
