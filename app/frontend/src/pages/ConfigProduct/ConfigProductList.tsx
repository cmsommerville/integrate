import { useState, useEffect, useMemo, useCallback, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { Link } from "react-router-dom";
import moment from "moment";
import { PlusIcon } from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppSnackbar from "@/components/AppSnackbar";
import AppButton from "@/components/AppButton";
import { ConfigProduct } from "./types";
import { PageTitle } from "./Components";
import Grid from "@/components/Grid";
import {
  GridApi,
  ColumnApi,
  GridReadyEvent,
  ColDef,
  RowDoubleClickedEvent,
} from "ag-grid-community";

const EditLinkComponent = (props: any) => {
  const url = useMemo(() => {
    return `/app/config/product/${props.data.config_product_id}`;
  }, [props]);

  return (
    <Link to={url}>
      <span
        className={classNames(
          "text-primary-600 font-semibold cursor-pointer",
          "hover:underline hover:text-primary-400"
        )}
      >
        Edit
      </span>
    </Link>
  );
};

const ConfigProductList = () => {
  const navigate = useNavigate();

  const [gridApi, setGridApi] = useState<GridApi>();
  const [columnApi, setColumnApi] = useState<ColumnApi>();

  const [products, setProducts] = useState<ConfigProduct[]>([]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/config/products`, { signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get product data");
        }
        return res.json();
      })
      .then((res) => {
        setProducts(res);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, []);

  useEffect(() => {
    if (!gridApi) return;
    if (!columnApi) return;
    if (!products) return;
    if (products.length === 0) return;

    gridApi.setRowData(products);
  }, [gridApi, columnApi, products]);

  const components = useMemo(() => {
    return {
      editLinkComponent: EditLinkComponent,
    };
  }, []);

  const onNewProductHandler = () => {
    navigate(`/app/config/product`);
  };

  const toProduct = (params: RowDoubleClickedEvent<any>) => {
    return navigate(`/app/config/product/${params.data.config_product_id}`);
  };

  return (
    <>
      <PageTitle title="Products" subtitle="Select a product">
        <div className="flex items-end">
          <AppButton onClick={onNewProductHandler}>
            <span className="space-x-1 flex items-center">
              <PlusIcon className="w-5 h-5 inline-block" />
              <span>New</span>
            </span>
          </AppButton>
        </div>
      </PageTitle>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-5 flex flex-col space-y-4">
          <AppPanel className="px-0 py-0">
            <div className="h-72">
              <Grid
                components={components}
                onGridReady={(params: GridReadyEvent) => {
                  setGridApi(params.api);
                  setColumnApi(params.columnApi);
                }}
                defaultColDef={DEFAULT_COLUMN_DEFS}
                columnDefs={COLUMN_DEFS}
                onFirstDataRendered={(params) => {
                  params.columnApi.autoSizeAllColumns();
                }}
                onRowDoubleClicked={toProduct}
              />
            </div>
          </AppPanel>
        </div>
      </div>
    </>
  );
};

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const DEFAULT_COLUMN_DEFS = {
  resizable: true,
  filter: true,
} as ColDef;

const COLUMN_DEFS = [
  {
    field: "config_product_label",
    headerName: "Product",
    cellClass: "font-semibold text-gray-900",
  },
  {
    field: "config_product_effective_date",
    headerName: "Effective Date",
    valueFormatter: (params) => moment(params.value).format("M/D/YYYY"),
  },
  {
    field: "config_product_expiration_date",
    headerName: "Expiration Date",
    valueFormatter: (params) => moment(params.value).format("M/D/YYYY"),
  },
  {
    cellRenderer: "editLinkComponent",
    cellRendererParams: {
      url: (params: any) =>
        `/app/config/product/${params.data.config_product_id}`,
    },
  },
] as ColDef[];

export default ConfigProductList;
