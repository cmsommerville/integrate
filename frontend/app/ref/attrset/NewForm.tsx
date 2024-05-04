"use client";
import * as z from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { AttrSetFormSchema } from "@/ref/schemas";
import { createNewAttributeSet } from "./data";
import { ConfigAttributeSet } from "@/ref/types";

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
import { useRouter } from "next/navigation";

type ValidationSchema = z.infer<typeof AttrSetFormSchema>;

type NewProductFormProps = {
  data: ValidationSchema;
};

export default function NewForm({ data }: NewProductFormProps) {
  const router = useRouter();
  const form = useForm<ValidationSchema>({
    resolver: zodResolver(AttrSetFormSchema),
    defaultValues: {
      ...data,
    },
  });

  const success_route = (data: ConfigAttributeSet) => {
    return `/ref/attrset/${data.config_attr_set_id}`;
  };

  async function onSubmit(values: ValidationSchema) {
    const data = await createNewAttributeSet(values);
    if (data) {
      router.push(success_route(data));
      router.refresh();
    }
  }
  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(onSubmit)}
        className="space-y-8 relative"
      >
        <FormField
          control={form.control}
          name="config_attr_set_code"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Code</FormLabel>
              <FormControl>
                <Input
                  placeholder="Unique code for this set of attributes"
                  {...field}
                />
              </FormControl>
              <FormDescription></FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="config_attr_set_label"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Input
                  placeholder="A description, such as Gender Attributes"
                  {...field}
                />
              </FormControl>
              <FormDescription></FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <div className="flex justify-end">
          <AppButton type="submit">Save</AppButton>
        </div>
      </form>
    </Form>
  );
}
