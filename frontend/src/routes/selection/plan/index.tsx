import { useEffect, useState } from "react";
import {
  createFileRoute,
  useLoaderData,
  useNavigate,
} from "@tanstack/react-router";
import { useMutation } from "@tanstack/react-query";
import { Formik, Form, useFormikContext } from "formik";
import { addDays, lastDayOfMonth } from "date-fns";
import AppPanel from "@/components/layout/AppPanel";
import { ErrorText } from "@/components/ui/error";
import {
  ConfigProductVariationStateDetail,
  getProducts,
  getProductVariationStates,
  createDefaultPlan,
} from "./queries";
import {
  SelectionPlanCreateNewFormSchema,
  SelectionPlanCreateNewForm_PayloadSchema,
} from "./schemas";
import { AppDatePicker } from "@/components/form/AppDatePicker";
import { AppSelect } from "@/components/form/AppSelect";
import { z, ZodError } from "zod";
import { unique_dropdown } from "@/lib/utils";
import { LoadingSpinner } from "@/components/ui/spinner";

export const Route = createFileRoute("/selection/plan/")({
  component: () => <SelectionPlanCreateNew />,
  loader: () => getProducts(),
});

function SelectionPlanCreateNew() {
  const navigate = useNavigate({ from: "/selection/plan/" });
  const products = useLoaderData({ from: "/selection/plan/" });
  const qryCreateDefaultPlan = useMutation({
    mutationFn: createDefaultPlan,
  });

  const onSubmitHandler = async (
    values: z.infer<typeof SelectionPlanCreateNewFormSchema>,
    setSubmitting: (isSubmitting: boolean) => void
  ) => {
    const validated_data =
      SelectionPlanCreateNewForm_PayloadSchema.safeParse(values);
    if (validated_data.success) {
      qryCreateDefaultPlan.mutate(validated_data.data, {
        onSuccess: (data) => {
          navigate({ to: `/selection/plan/${data.selection_plan_id}` });
        },
        onSettled: () => {
          setSubmitting(false);
        },
      });
      return;
    } else {
      alert("There was an error with the form data");
    }
  };
  return (
    <div className="grid grid-cols-1 xl:grid-cols-2">
      <AppPanel>
        <h2 className="text-md text-gray-900 mb-1">Create a new plan</h2>
        <p className="text-xs text-gray-400 mb-4">
          Lorem ipsum, dolor sit amet consectetur adipisicing elit. Libero vitae
          explicabo aliquid pariatur, quas consequuntur at reiciendis ullam
          ratione ducimus quos dolor ut magnam maxime dolore cumque minima
          nostrum. Assumenda.
        </p>
        <Formik
          enableReinitialize
          initialValues={{
            config_product_id: undefined,
            selection_plan_effective_date: addDays(
              lastDayOfMonth(new Date()),
              1
            ),
            situs_state_id: undefined,
            config_product_variation_id: undefined,
          }}
          validate={(values) => {
            try {
              SelectionPlanCreateNewFormSchema.parse(values);
            } catch (error) {
              if (error instanceof ZodError) {
                return error.formErrors.fieldErrors;
              }
            }
          }}
          onSubmit={(values, { setSubmitting }) => {
            onSubmitHandler(values, setSubmitting);
          }}
        >
          <Form className="">
            <div className="mb-6">
              <div className="space-y-2">
                <AppSelect
                  className=""
                  name="config_product_id"
                  label="Product"
                  placeholder="Select a product"
                  options={products.data.map((prod) => ({
                    label: prod.config_product_label,
                    value: prod.config_product_id,
                  }))}
                />
              </div>
              <div className="py-2">
                <AppDatePicker
                  className=""
                  name="selection_plan_effective_date"
                  label="Effective Date"
                  placeholder="Choose an effective date"
                />
              </div>
            </div>

            <ConditionalVariationStateForm />

            <div className="mt-6 flex justify-end">
              <button
                type="submit"
                className="flex items-center space-x-1 rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                <span>Submit</span>
                {qryCreateDefaultPlan.isPending && (
                  <LoadingSpinner className="h-5 w-5" />
                )}
              </button>
            </div>
            {qryCreateDefaultPlan.isError ? (
              <ErrorText className="flex justify-end py-2">
                {qryCreateDefaultPlan.error.message}
              </ErrorText>
            ) : null}
          </Form>
        </Formik>
      </AppPanel>
    </div>
  );
}

function ConditionalVariationStateForm() {
  const [dropdowns, setDropdowns] = useState<
    ConfigProductVariationStateDetail[]
  >([]);
  // Grab values and submitForm from context
  const { values, setFieldValue } =
    useFormikContext<z.infer<typeof SelectionPlanCreateNewFormSchema>>();
  const { data: formattedValues } =
    SelectionPlanCreateNewFormSchema.partial().safeParse(values);

  useEffect(() => {
    // fetch the dropdown data when the product and effective date change
    if (!values?.config_product_id || !values?.selection_plan_effective_date)
      return;
    getProductVariationStates(
      values?.config_product_id,
      values?.selection_plan_effective_date
    )
      .then((d) => {
        setFieldValue("config_product_variation_id", undefined);
        setFieldValue("situs_state_id", undefined);
        const { data } = d;
        setDropdowns(data);
      })
      .catch(() => {
        setDropdowns([]);
      });
  }, [
    setFieldValue,
    values?.config_product_id,
    values?.selection_plan_effective_date,
  ]);

  useEffect(() => {
    // when the product variation and situs state change, then set the config_product_variation_state_id
    if (!values?.config_product_variation_id) return;
    if (!values?.situs_state_id) return;
    const { data: formattedValues } =
      SelectionPlanCreateNewFormSchema.partial().safeParse(values);
    if (!formattedValues) return;

    // the row should always exist, but if it doesn't, clear the variation and situs state
    const row = dropdowns.find((dd) => {
      return (
        dd.config_product_variation_id ===
          formattedValues.config_product_variation_id &&
        dd.situs_state_id === formattedValues.situs_state_id
      );
    });
    if (!row) {
      setFieldValue("config_product_variation_id", undefined);
      setFieldValue("situs_state_id", undefined);
      return;
    }
    setFieldValue(
      "config_product_variation_state_id",
      row.config_product_variation_state_id
    );
  }, [dropdowns, setFieldValue, values]);

  if (!formattedValues) return null;

  return (
    <div className="grid grid-cols-2 gap-8">
      <AppSelect
        name="situs_state_id"
        label="Situs State"
        placeholder="Select a situs"
        disabled={!dropdowns || !dropdowns.length}
        options={unique_dropdown(
          dropdowns,
          "situs_state_id",
          formattedValues
        ).map((pv) => ({
          label: pv.state_name as string,
          value: pv.situs_state_id as number,
        }))}
        showClearSelection={true}
      />
      <AppSelect
        name="config_product_variation_id"
        label="Product Variation"
        placeholder="Select a product variation"
        disabled={!dropdowns || !dropdowns.length}
        options={unique_dropdown(
          dropdowns,
          "config_product_variation_id",
          formattedValues
        ).map((pv) => ({
          label: pv.config_product_variation_label as string,
          value: pv.config_product_variation_id as number,
        }))}
        showClearSelection={true}
      />
    </div>
  );
}
