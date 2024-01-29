import AppCard from "@/components/ui/AppCard";
import NewProductForm from "../NewProductForm";
import { getSingleProduct } from "@/config/product/data";
import ProcessSteps from "@/components/page/ProcessSteps";
import { ProcessStep } from "@/components/page/types";

export default async function ProductPage({
  params,
}: {
  params: { id: string };
}) {
  const data = await getSingleProduct(parseInt(params.id));

  const STEPS: ProcessStep[] = [
    {
      name: "Product",
      href: "#",
      status: "CURRENT",
    },
    {
      name: "Product Variations",
      href: `/config/product/${params.id}/variations`,
      status:
        data && data.config_product_variations ? "COMPLETE" : "INCOMPLETE",
    },
  ];

  if (!data)
    return (
      <AppCard>
        <h2>Oh no! We cannot find that record!</h2>
      </AppCard>
    );

  return (
    <div className="flex items-start space-x-8">
      <AppCard className="w-2/3">
        <div className="space-y-4">
          <div className="">
            <h2 className="text-lg">{data.config_product_label}</h2>
            <p className="text-xs text-gray-400">
              Click the edit button to the right to edit.
            </p>
          </div>
          <hr />
          <NewProductForm
            editability="TOGGLEABLE"
            disabled={{}}
            product={data}
          />
        </div>
      </AppCard>
      <AppCard className="w-60 h-auto">
        <ProcessSteps steps={STEPS} />
      </AppCard>
    </div>
  );
}
