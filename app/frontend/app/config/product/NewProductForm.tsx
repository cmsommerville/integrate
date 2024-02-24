"use client";
import { useState } from "react";
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { format, parseISO } from "date-fns";
import { cn } from "@/lib/utils";
import { ProductFormSchema } from "./schemas";
import { createNewProduct, updateExistingProduct } from "./data";

import { Calendar } from "@/components/ui/calendar";
import { Button } from "@/components/ui/button";
import AppButton from "@/components/ui/AppButton";
import { Input } from "@/components/ui/input";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

import { PiPencilSimple, PiCalendarBlank } from "react-icons/pi";
import { ProductType } from "../types";

type NewProductFormProps = {
  product: z.infer<typeof ProductFormSchema>;
  editability?: "RESTRICTED" | "TOGGLEABLE" | "EDITABLE";
  disabled?: { [k in keyof z.infer<typeof ProductFormSchema>]?: boolean };
};

export default function NewProductForm({
  product,
  editability = "RESTRICTED",
  disabled = { config_product_expiration_date: true },
}: NewProductFormProps) {
  const [isFormDisabled, setIsFormDisabled] = useState(
    editability === "EDITABLE" ? false : true
  );

  const form = useForm<z.infer<typeof ProductFormSchema>>({
    resolver: zodResolver(ProductFormSchema),
    defaultValues: {
      ...product,
    },
  });

  function isFieldDisabled(field: keyof z.infer<typeof ProductFormSchema>) {
    if (isFormDisabled) return true;
    return disabled[field] ?? false;
  }

  function onToggleEditable() {
    setIsFormDisabled((prev) => !prev);
  }

  function onSubmit(values: z.infer<typeof ProductFormSchema>) {
    if (product.config_product_id != null) {
      updateExistingProduct(values, product as ProductType);
    } else {
      createNewProduct(values);
    }
  }
  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-8 relative"
      >
        {editability === "TOGGLEABLE" ? (
          <TooltipProvider>
            <Tooltip defaultOpen={true} delayDuration={300}>
              <TooltipTrigger asChild>
                <button
                  className={cn(
                    "absolute -top-4 right-0 shadow-md rounded-full w-6 h-6 flex justify-center items-center transition duration-100 ease",
                    "active:scale-95 shadow-sm",
                    isFormDisabled
                      ? "ring-1 ring-gray-400 text-gray-400 hover:bg-gray-50"
                      : "ring-1 ring-primary-600 bg-primary-600 text-white"
                  )}
                  onClick={(e) => {
                    e.preventDefault();
                    onToggleEditable();
                  }}
                >
                  <PiPencilSimple />
                </button>
              </TooltipTrigger>
              <TooltipContent side="top" sideOffset={35} align="end">
                {isFormDisabled
                  ? "Click here to edit!"
                  : "Click to disable editing!"}
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        ) : null}
        <div className="grid grid-cols-2 gap-8">
          <FormField
            control={form.control}
            disabled={isFieldDisabled("config_product_code")}
            name="config_product_code"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Product Code</FormLabel>
                <FormControl>
                  <Input placeholder="AC" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            disabled={isFieldDisabled("form_code")}
            name="form_code"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Form Code</FormLabel>
                <FormControl>
                  <Input placeholder="C70000" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <FormField
          control={form.control}
          disabled={isFieldDisabled("config_product_label")}
          name="config_product_label"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Input placeholder="i.e. Accident Series 70000" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <div className="grid grid-cols-2 gap-8">
          <FormField
            control={form.control}
            name="config_product_effective_date"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Effective Date</FormLabel>
                <Popover>
                  <PopoverTrigger
                    asChild
                    disabled={isFieldDisabled("config_product_effective_date")}
                  >
                    <FormControl>
                      <Button
                        variant={"outline"}
                        className={cn(
                          "w-full pl-3 text-left font-normal",
                          !field.value && "text-muted-foreground"
                        )}
                      >
                        {field.value ? (
                          format(parseISO(field.value), "P")
                        ) : (
                          <span>Pick a date</span>
                        )}
                        <PiCalendarBlank className="ml-auto h-4 w-4 opacity-50" />
                      </Button>
                    </FormControl>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="start">
                    <Calendar
                      numberOfMonths={1}
                      fixedWeeks
                      mode="single"
                      selected={parseISO(field.value)}
                      onSelect={field.onChange}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="config_product_expiration_date"
            render={({ field }) => (
              <FormItem className="flex flex-col">
                <FormLabel>Termination Date</FormLabel>
                <Popover>
                  <PopoverTrigger
                    asChild
                    disabled={isFieldDisabled("config_product_expiration_date")}
                  >
                    <FormControl>
                      <Button
                        variant={"outline"}
                        className={cn(
                          "w-full pl-3 text-left font-normal",
                          !field.value && "text-muted-foreground"
                        )}
                      >
                        {field.value ? (
                          format(parseISO(field.value), "P")
                        ) : (
                          <span>Pick a date</span>
                        )}
                        <PiCalendarBlank className="ml-auto h-4 w-4 opacity-50" />
                      </Button>
                    </FormControl>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0" align="end">
                    <Calendar
                      numberOfMonths={1}
                      fixedWeeks
                      mode="single"
                      selected={parseISO(field.value)}
                      onSelect={field.onChange}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <div className="flex justify-end">
          <AppButton type="submit">Save</AppButton>
        </div>
      </form>
    </Form>
  );
}
