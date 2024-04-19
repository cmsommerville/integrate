"use client";
import * as z from "zod";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { AttrDetailFormSchema } from "@/ref/schemas";
import { createNewAttributeDetail } from "./data";

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

type ValidationSchema = z.infer<typeof AttrDetailFormSchema>;

type NewProductFormProps = {
  data: ValidationSchema;
  success_route: string;
};

export default function NewForm({ data, success_route }: NewProductFormProps) {
  const router = useRouter();
  const form = useForm<ValidationSchema>({
    resolver: zodResolver(AttrDetailFormSchema),
    defaultValues: {
      ...data,
    },
  });

  function onSubmit(values: ValidationSchema) {
    try {
      createNewAttributeDetail(values);
      router.push(success_route);
      router.refresh();
    } catch (err) {
      console.log("Uh oh!");
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
          name="config_attr_detail_code"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Code</FormLabel>
              <FormControl>
                <Input placeholder="M / F for Male or Female" {...field} />
              </FormControl>
              <FormDescription></FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="config_attr_detail_label"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Input placeholder="Male or Female" {...field} />
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
