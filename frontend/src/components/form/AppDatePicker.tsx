import { useField, useFormikContext } from "formik";
import { format } from "date-fns";
import { Calendar as CalendarIcon } from "lucide-react";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { InputHTMLAttributes } from "react";

interface DatePickerFieldProps extends InputHTMLAttributes<HTMLInputElement> {
  name: string;
  label: string;
  placeholder?: string;
  onDayClick?: (val: Date) => void;
}

export const AppDatePicker = ({
  name,
  label,
  placeholder,
  className,
  onDayClick,
}: DatePickerFieldProps) => {
  const { setFieldValue } = useFormikContext();
  const [field] = useField(name);
  return (
    <Popover>
      <PopoverTrigger asChild>
        <div className={cn("w-full", className)}>
          <p className="blo}ck text-sm font-medium leading-6 text-gray-900">
            {label}
          </p>
          <Button
            type="button"
            variant={"outline"}
            className={cn(
              "w-full justify-start px-3 py-1.5 h-10 rounded-md text-left font-normal border-0 ring-1 ring-inset ring-gray-300",
              !field.value && "text-muted-foreground"
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4 text-gray-400" />
            {field.value ? (
              format(field.value, "M/d/yyyy")
            ) : (
              <span className="text-gray-400">
                {placeholder ?? "Pick a date"}
              </span>
            )}
          </Button>
        </div>
      </PopoverTrigger>
      <PopoverContent className="w-auto p-0">
        <Calendar
          mode="single"
          className="w-[280px] flex justify-center"
          selected={field.value}
          onSelect={(val) => {
            setFieldValue(field.name, val);
          }}
          initialFocus
          defaultMonth={field.value ?? new Date()}
          onDayClick={(val) => {
            onDayClick ? onDayClick(val) : null;
          }}
          {...field}
        />
      </PopoverContent>
    </Popover>
  );
};
