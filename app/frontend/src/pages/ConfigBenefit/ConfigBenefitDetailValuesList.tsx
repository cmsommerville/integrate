import { useState, useEffect, useMemo } from "react";
import { useParams, useNavigate } from "react-router";
import {
  ConfigBenefitAuth,
  ConfigBenefitAuthACL,
  ConfigBenefitDetail,
} from "./types";
import { AuthRole } from "@/types/auth";
import axios, { authServerAxiosInstance } from "@/services/axios";
import {
  GridApi,
  ColumnApi,
  ColDef,
  ICellRendererParams,
  RowClickedEvent,
  RowDragEndEvent,
  RowDoubleClickedEvent,
} from "ag-grid-community";
import Grid from "@/components/Grid";
import AppButton from "@/components/AppButton";
import { PageTitle } from "../ConfigProduct/Components";
import { AppPanel } from "@/components/AppPanel";
import { Tabs, TabCode } from "./Components";
import { PlusIcon } from "@heroicons/react/20/solid";

import ConfigBenefitDetailValues from "./ConfigBenefitDetailValues";

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const ConfigBenefitDetailValuesList = () => {
  const { product_id, benefit_id } = useParams();

  const [isSaving, setIsSaving] = useState(false);
  const [isDirty, setIsDirty] = useState(false);

  const [showBenefitPanel, toggleOpenBenefitPanel] = useState(false);
  const [benefitAuths, setBenefitAuths] = useState<
    Partial<ConfigBenefitAuth>[]
  >([]);
  const [benefit, setBenefit] = useState<Partial<ConfigBenefitDetail>>({});
  const [selected, setSelected] = useState<Partial<ConfigBenefitAuth>>({});
  const [authRoles, setAuthRoles] = useState<AuthRole[]>([]);
  const [gridApi, setGridApi] = useState<GridApi>();
  const [columnApi, setColumnApi] = useState<ColumnApi>();

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    axios
      .get(`/api/config/product/${product_id}/benefit/${benefit_id}`, {
        signal,
      })
      .then((res) => {
        const { benefit_auth, ...benefit } = res.data;
        const b = [...benefit_auth] as ConfigBenefitAuth[];
        b.sort((x, y) => {
          if (x.priority == null) return 1;
          if (y.priority == null) return -1;
          return x.priority < y.priority ? -1 : 1;
        });
        setBenefitAuths(b);
        setBenefit(benefit);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, [product_id, benefit_id]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    authServerAxiosInstance
      .get(`/roles`, { signal })
      .then((res) => {
        setAuthRoles(res.data);
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
    if (!benefitAuths) return;
    if (!authRoles.length) return;

    gridApi.setRowData(benefitAuths);
  }, [gridApi, columnApi, benefitAuths, authRoles]);

  const onFirstDataRendered = () => {
    if (!columnApi) return;
    columnApi.autoSizeAllColumns();
  };

  const isValid = useMemo(() => {
    // return Object.entries(benefit).reduce((isValid, [k, v]) => {
    //   return isValid && validator(k as keyof ConfigBenefit, v);
    // }, true);
    return true;
  }, []);

  const onTabClick = (selected: TabCode) => {
    console.log(selected);
  };

  const onDataEdit = (bnft: Partial<ConfigBenefitAuth>) => {
    if (!benefitAuths) return;
    const bnfts = [
      ...benefitAuths.filter((b) => {
        return b.config_benefit_auth_id !== bnft.config_benefit_auth_id;
      }),
      { priority: 999, ...bnft },
    ];
    bnfts.sort((a, b) => {
      if (!a.priority) return 1;
      if (!b.priority) return -1;
      return a.priority < b.priority ? -1 : 1;
    });

    setBenefitAuths((prev) => {
      return { ...prev, benefit_auth: bnfts };
    });
    setIsDirty(true);
  };

  const reprioritizeRows = (api: GridApi) => {
    // loop through all the rows in the grid and set the priority based on display order
    let data = [] as any[];
    api.forEachNode((row, i) => {
      const r = row.data;
      r.priority = (i + 1) * 10;
      data.push(r);
    });
    api.applyTransaction({
      update: data,
    })!;
    setIsDirty(true);
  };

  const onRowClick = (event: RowClickedEvent) => {
    setSelected(event.data);
  };

  const onRowDragEnd = (event: RowDragEndEvent) => {
    // reset the priority as a data element whenever drag event ends
    reprioritizeRows(event.api);
    event.api.refreshCells();
  };

  const openBenefitAuthEditHandler = () => {
    // make sure to set the priority before a new benefit auth is added
    // also opens on double click
    if (!gridApi) return;
    reprioritizeRows(gridApi);
    toggleOpenBenefitPanel(true);
  };

  const onCloseBenefitSidePanel = () => {
    setSelected({});
    toggleOpenBenefitPanel(false);
  };

  const onSave = () => {
    axios
      .patch(`/api/config/product/${product_id}/benefit/${benefit_id}`, {
        benefit_auth: benefitAuths,
      })
      .then((res) => {
        console.log(res);
      });
  };

  return (
    <>
      <PageTitle
        title="Benefit Values"
        subtitle="Set defaults, mins, and maxes, and which roles are authorized to use them..."
      >
        <div className="flex items-end">
          <AppButton
            disabled={!isValid || !isDirty}
            isLoading={isSaving}
            onClick={onSave}
          >
            Save
          </AppButton>
        </div>
      </PageTitle>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-4 flex flex-col space-y-4">
          <AppPanel className="pb-16 pt-2 h-fit">
            <>
              <Tabs selected="values" onClick={onTabClick} />
              <div className="space-y-4">
                <ConfigBenefitDetailValues
                  open={showBenefitPanel}
                  benefit_auth={selected}
                  benefit={benefit}
                  onSave={onDataEdit}
                  onClose={onCloseBenefitSidePanel}
                />
                <div className="h-72 relative">
                  <Grid
                    onGridReady={(params) => {
                      setGridApi(params.api);
                      setColumnApi(params.columnApi);
                    }}
                    defaultColDef={{
                      filter: true,
                      resizable: true,
                      sortable: false,
                    }}
                    rowDragManaged={true}
                    rowDragEntireRow={true}
                    animateRows={true}
                    onRowDragEnd={onRowDragEnd}
                    onRowClicked={onRowClick}
                    onRowDoubleClicked={openBenefitAuthEditHandler}
                    context={{
                      authRoles: authRoles,
                      benefit: benefit,
                    }}
                    columnDefs={GRID_COLUMNS}
                    onFirstDataRendered={onFirstDataRendered}
                  />

                  <button
                    className="absolute -bottom-6 right-0 rounded-full p-4 bg-primary-600 text-white ring-offset-2 transition-all ease duration-300 hover:bg-primary-700 hover:ring-2 hover:ring-primary-700"
                    onClick={openBenefitAuthEditHandler}
                  >
                    <PlusIcon className="w-5 h-5" />
                  </button>
                </div>

                <div className="flex justify-end"></div>
              </div>
            </>
          </AppPanel>
        </div>
      </div>
    </>
  );
};

const BenefitAmountRenderer = (params: ICellRendererParams) => {
  const unit_type = params.context.benefit.unit_type.ref_attr_symbol;
  const val = params.value;
  let symbol;
  if (unit_type === "%") {
    return (
      <div className="w-full flex justify-space-between items-center space-x-1">
        <div className="w-full">{val}</div>
        <div className="text-gray-400 text-xs">%</div>
      </div>
    );
  }
  if (["$"].includes(unit_type)) {
    return (
      <div className="w-full flex justify-space-between items-center space-x-1">
        <div className="text-gray-400 text-xs w-full flex">{unit_type}</div>
        <div className="">{val}</div>
      </div>
    );
  }
  return;
};

const RangeRenderer = (params: ICellRendererParams) => {
  const unit_type = params.context.benefit.unit_type.ref_attr_symbol;
  let symbol;
  if (unit_type === "%") {
    return (
      <div className="w-full flex justify-space-between items-center space-x-1">
        <div className="w-full">
          [{params.data.min_value} - {params.data.max_value}]
        </div>
        <div className="text-gray-400 text-xs">%</div>
      </div>
    );
  }
  return;
};
const GRID_COLUMNS = [
  {
    headerName: "Priority",
    valueGetter: (params) => {
      if (!params.node) return;
      if (params.node.rowIndex == null) return;
      return params.node.rowIndex + 1;
    },
    rowDrag: true,
  },
  {
    field: "default_value",
    headerName: "Default",
    cellClass: "text-right",
    cellRenderer: BenefitAmountRenderer,
  },
  {
    field: "min_value",
    headerName: "Range",
    cellClass: "text-right",
    cellRenderer: RangeRenderer,
  },
  {
    headerName: "Roles",
    valueGetter: (params) => {
      return params.data.acl
        .map((item: ConfigBenefitAuthACL) => {
          const role = params.context.authRoles.find(
            (r: AuthRole) => r.auth_role_code === item.auth_role_code
          );
          return role.auth_role_label;
        })
        .join(", ");
    },
  },
] as ColDef[];

export default ConfigBenefitDetailValuesList;
