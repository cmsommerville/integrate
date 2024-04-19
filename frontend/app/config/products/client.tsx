"use client";
import SetTablePage, {
  SetTablePageSubtitle,
  SetTablePageProps,
} from "@/components/page/SetTablePage";
import { format, parseISO } from "date-fns";
import { ColDef, ValueFormatterParams } from "ag-grid-community";

export const COL_DEFS: ColDef[] = [
  {
    field: "config_product_label",
    headerName: "Product",
  },
  {
    field: "config_product_effective_date",
    headerName: "Effective",
    cellRenderer: "StoplightComponent",
    cellRendererParams: {
      colorFormatter: (params: any) => {
        return parseISO(params.data.config_product_expiration_date) <
          parseISO("9999-12-31")
          ? "red"
          : parseISO(params.data.config_product_effective_date) <
            parseISO("2015-01-01")
          ? "yellow"
          : "green";
      },
    },
    valueFormatter: (params: ValueFormatterParams) => {
      console.log(params.data.config_product_effective_date);
      return `${format(
        parseISO(params.data.config_product_effective_date),
        "M/d/yyyy"
      )} - ${format(
        parseISO(params.data.config_product_expiration_date),
        "M/d/yyyy"
      )}`;
    },
  },
];

export default function ProductsLandingClientGrid<T>(
  props: Omit<SetTablePageProps<T>, "columnDefs">
) {
  return (
    <SetTablePage
      className="max-w-4xl"
      title="Products"
      rowData={props.rowData}
      columnDefs={COL_DEFS}
      routes={props.routes}
    >
      <SetTablePageSubtitle>
        Select a product to edit or create a new product from scratch!
      </SetTablePageSubtitle>
    </SetTablePage>
  );
}
