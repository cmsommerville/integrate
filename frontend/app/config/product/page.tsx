import AppCard from "@/components/ui/AppCard";
import NewProductForm from "./NewProductForm";
import { ProductType } from "../types";
import ProcessSteps from "@/components/page/ProcessSteps";
import { ProcessStep } from "@/components/page/types";

const INITIAL_DATA: Omit<ProductType, "config_product_id"> = {
  config_product_code: "",
  config_product_label: "",
  form_code: "",
  config_product_effective_date: "2023-12-01",
  config_product_expiration_date: "9999-12-31",
};

const STEPS: ProcessStep[] = [
  {
    name: "Product",
    href: "#",
    status: "CURRENT",
  },
  {
    name: "Product Variations",
    href: "#",
    status: "INCOMPLETE",
  },
];

export default function NewProductPage() {
  return (
    <div className="flex items-start space-x-8">
      <AppCard className="w-2/3">
        <div className="space-y-4">
          <h2 className="text-lg">Create a new product</h2>
          <hr />
          <NewProductForm editability="EDITABLE" product={INITIAL_DATA} />
        </div>
      </AppCard>
      <AppCard className="w-60 h-auto">
        <ProcessSteps steps={STEPS} />
      </AppCard>
    </div>
  );
}
