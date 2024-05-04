"use client";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { RatingMapperCollectionFormSchema } from "../../schemas";
import { createNewRatingMapperCollection } from "./data";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";

import AppButton from "@/components/ui/AppButton";
import { NewRatingMapperCollectionType } from "@/config/types";
import { ConfigAttributeSet } from "@/ref/types";

type NewCollectionFormProps = {
  collection: NewRatingMapperCollectionType;
  dropdowns: ConfigAttributeSet[];
};

type ValidationSchemaType = NewRatingMapperCollectionType;

export default function NewForm({
  collection,
  dropdowns,
}: NewCollectionFormProps) {
  const router = useRouter();
  const form = useForm<ValidationSchemaType>({
    resolver: zodResolver(RatingMapperCollectionFormSchema),
    defaultValues: {
      ...collection,
    },
  });

  function onSubmit(values: ValidationSchemaType) {
    try {
      createNewRatingMapperCollection(values);
      router.push(`/config/mappers/collections`);
      router.refresh();
    } catch (err) {
      console.log("Uh oh...");
    }
  }
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="config_attribute_set_id"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Attributes</FormLabel>
              <Select
                onValueChange={field.onChange}
                defaultValue={String(field.value)}
              >
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select a verified email to display" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  {dropdowns.map((dd) => {
                    return (
                      <SelectItem
                        key={dd.config_attr_set_id}
                        value={String(dd.config_attr_set_id)}
                      >
                        {dd.config_attr_set_label}
                      </SelectItem>
                    );
                  })}
                </SelectContent>
              </Select>
              <FormDescription>
                You can manage email addresses in your{" "}
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="config_rating_mapper_collection_label"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Collection Name</FormLabel>
              <FormControl>
                <Input
                  placeholder="Enter a description for this collection"
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
          name="is_selectable"
          render={({ field }) => (
            <FormItem className="flex flex-row items-start space-x-3 space-y-0">
              <FormControl>
                <Checkbox
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
              <div className="space-y-1 leading-none">
                <FormLabel>Will users select these from a dropdown?</FormLabel>
                <FormDescription>
                  Common examples are selecting composite vs. tobacco-distinct
                  rates.
                </FormDescription>
              </div>
            </FormItem>
          )}
        />
        <AppButton type="submit">Submit</AppButton>
      </form>
    </Form>
  );
}
