"use client";
import * as z from "zod";
import { useState, useMemo } from "react";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { EditAttrDetailFormSchema } from "@/ref/schemas";
import { editConfigAttributeDetail } from "./data";

import AppButton from "@/components/ui/AppButton";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { PiPencilSimple, PiPencilSimpleSlash } from "react-icons/pi";

type ValidationSchema = z.infer<typeof EditAttrDetailFormSchema>;

type EditFormProps = {
  data: ValidationSchema;
};

const DEFAULT_EDITABLE_STATE = {
  config_attr_detail_code: false,
  config_attr_detail_label: false,
};

export default function NewForm({ data }: EditFormProps) {
  const [isEditable, setIsEditable] = useState(DEFAULT_EDITABLE_STATE);

  const router = useRouter();
  const form = useForm<ValidationSchema>({
    resolver: zodResolver(EditAttrDetailFormSchema),
    defaultValues: {
      ...data,
    },
  });

  function onSubmit(values: ValidationSchema) {
    try {
      console.log(values);
      editConfigAttributeDetail(values);
      router.push(`/ref/attrset/${values.config_attr_set_id}`);
      router.refresh();
    } catch (err) {
      console.log("Uh oh!");
    }
  }

  function toggleEditable(key: keyof typeof DEFAULT_EDITABLE_STATE) {
    setIsEditable((prev) => {
      return { ...prev, [key]: !prev[key] };
    });
  }

  const displaySave = useMemo(() => {
    return Object.values(isEditable).some((val) => !!val);
  }, [isEditable]);

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-8 relative"
      >
        <FormField
          control={form.control}
          name="config_attr_detail_code"
          render={({ field }) => (
            <FormItem className="grid grid-cols-4 gap-x-8 items-center space-y-0">
              <FormLabel className="col-span-1">Code</FormLabel>
              <div className="col-span-3 flex items-center ">
                <FormControl>
                  <div className="flex w-full max-w-sm items-center space-x-4">
                    <Input
                      placeholder="i.e. M / F"
                      disabled={!isEditable.config_attr_detail_code}
                      {...field}
                    />
                    <button
                      type="button"
                      className="size-6 text-slate-500 hover:text-primary-300 transition duration-100"
                      onClick={() => toggleEditable("config_attr_detail_code")}
                    >
                      {isEditable.config_attr_detail_code ? (
                        <PiPencilSimpleSlash />
                      ) : (
                        <PiPencilSimple />
                      )}
                    </button>
                  </div>
                </FormControl>
                <FormDescription></FormDescription>
                <FormMessage />
              </div>
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="config_attr_detail_label"
          render={({ field }) => (
            <FormItem className="grid grid-cols-4 gap-x-8 items-center space-y-0">
              <FormLabel className="col-span-1">Description</FormLabel>
              <div className="col-span-3 flex items-center ">
                <FormControl>
                  <div className="flex w-full max-w-sm items-center space-x-4">
                    <Input
                      placeholder="i.e. Male or Female"
                      disabled={!isEditable.config_attr_detail_label}
                      {...field}
                    />
                    <button
                      type="button"
                      className="size-6 text-slate-500 hover:text-primary-300 transition duration-100"
                      onClick={() => toggleEditable("config_attr_detail_label")}
                    >
                      {isEditable.config_attr_detail_label ? (
                        <PiPencilSimpleSlash />
                      ) : (
                        <PiPencilSimple />
                      )}
                    </button>
                  </div>
                </FormControl>
                <FormDescription></FormDescription>
                <FormMessage />
              </div>
            </FormItem>
          )}
        />
        <div className="flex justify-end">
          {displaySave ? <AppButton type="submit">Save</AppButton> : null}
        </div>
      </form>
    </Form>
  );
}
