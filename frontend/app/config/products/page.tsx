import ProductsLandingClientGrid from "./client";
import { getProducts } from "./data";
import { ProductType } from "../types";

export default async function ProductsLandingPage() {
  const row_data = await getProducts();

  const onEditHandler = async (row: ProductType) => {
    "use server";
    return `/config/product/${row.config_product_id}/`;
  };

  const newProductHandler = async () => {
    "use server";
    return `/config/product`;
  };

  return (
    <ProductsLandingClientGrid
      className="max-w-4xl"
      title="Products"
      rowData={row_data}
      routes={{
        edit: onEditHandler,
        new: newProductHandler,
      }}
    />
  );
}
