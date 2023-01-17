import { useState, useEffect, useMemo, useCallback, useRef } from "react";
import { useNavigate, useParams } from "react-router-dom";
import axios from "@/services/axios";
import { PlusIcon } from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";
import { ConfigBenefit, RefBenefit } from "./types";
import Grid, { EditLinkComponent } from "@/components/Grid";
import {
  GridApi,
  ColumnApi,
  GridReadyEvent,
  ColDef,
  RowDoubleClickedEvent,
} from "ag-grid-community";

const ConfigBenefitList = () => {
  const { product_id } = useParams();
  const navigate = useNavigate();

  const [gridApi, setGridApi] = useState<GridApi>();
  const [columnApi, setColumnApi] = useState<ColumnApi>();

  const [benefits, setBenefits] = useState<ConfigBenefit[]>([]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    // fetch(`/api/data/config/product/${product_id}/benefits`, { signal });
    // .then((res) => {
    //     if (!res.ok) {
    //       throw new Error("Cannot get product data");
    //     }
    //     return res.json();
    //   })
    axios
      .get(`/api/data/config/product/${product_id}/benefits`, { signal })
      .then((res) => {
        setBenefits(res.data);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, [product_id]);

  useEffect(() => {
    if (!gridApi) return;
    if (!columnApi) return;
    if (!benefits) return;
    if (benefits.length === 0) return;

    gridApi.setRowData(benefits);
  }, [gridApi, columnApi, benefits]);

  const components = useMemo(() => {
    return {
      editLinkComponent: EditLinkComponent,
    };
  }, []);

  const onNewHandler = () => {
    navigate(`/app/config/product/${product_id}/benefit`);
  };

  const toProduct = (params: RowDoubleClickedEvent<any>) => {
    return navigate(
      `/app/config/product/${product_id}/benefit/${params.data.config_benefit_id}`
    );
  };

  return (
    <>
      <div className="flex justify-between pb-6">
        <div className="">
          <h2 className="text-2xl font-light tracking-wide text-gray-700">
            Benefits
          </h2>
          <p className="text-sm text-gray-400">
            Create a new benefit or edit an existing one!
          </p>
        </div>
        <div className="flex justify-end items-end">
          <div className="flex items-end">
            <AppButton onClick={onNewHandler}>
              <span className="space-x-1 flex items-center">
                <PlusIcon className="w-5 h-5 inline-block" />
                <span>New</span>
              </span>
            </AppButton>
          </div>
        </div>
      </div>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-3 flex flex-col space-y-4">
          <AppPanel className="px-0 py-0">
            <div className="h-70vh">
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
    field: "ref_benefit.ref_attr_label",
    headerName: "Benefit",
    cellClass: "font-semibold text-gray-900",
  },
  {
    field: "default_value",
    headerName: "Default Value",
    valueFormatter: (params) => {
      const symbol = params.data.unit_type.ref_attr_symbol;

      return symbol === "$"
        ? `${symbol} ${params.value}`
        : symbol === "%"
        ? `${params.value} ${symbol}`
        : params.value;
    },
  },
  {
    cellRenderer: "editLinkComponent",
    cellRendererParams: {
      url: (params: any) =>
        `/app/config/product/${params.data.config_product_id}/benefit/${params.data.config_benefit_id}`,
    },
  },
] as ColDef[];

export default ConfigBenefitList;
