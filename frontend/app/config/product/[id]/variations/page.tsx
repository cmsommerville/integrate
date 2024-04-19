import ProductVariationsLandingClientGrid from "./client";
import { getVariations } from "./data";
import { ProductVariationType } from "../../../types";

export default async function VariationsLandingPage({
  params,
}: {
  params: { id: string };
}) {
  const row_data = await getVariations(parseInt(params.id));

  const onEditHandler = async (row: ProductVariationType) => {
    "use server";
    return `variation/${row.config_product_variation_id}`;
  };

  const newProductHandler = async () => {
    "use server";
    return `variation`;
  };

  return (
    <ProductVariationsLandingClientGrid
      className="max-w-4xl"
      title="Product Variations"
      rowData={row_data}
      routes={{
        edit: onEditHandler,
        new: newProductHandler,
      }}
    />
  );
}
