import { useState, useEffect } from "react";
import {
  ConfigBenefit,
  ConfigBenefitAuth,
  ConfigBenefitAuthACL,
  ConfigBenefitDetail,
} from "./types";
import { AuthRole } from "@/types/auth";
import axios, { authServerAxiosInstance } from "@/services/axios";
import { GridApi, ColumnApi, ColDef } from "ag-grid-community";
import Grid from "@/components/Grid";
import AppButton from "@/components/AppButton";

import ConfigBenefitDetailValues from "./ConfigBenefitDetailValues";

type Props = {
  product_id: number | string;
  benefit: ConfigBenefit;
  onChange(key: string, val: any): void;
};

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const ConfigBenefitDetailValuesList = ({
  product_id,
  benefit,
  onChange,
  ...props
}: Props) => {
  const [showBenefitPanel, toggleOpenBenefitPanel] = useState(false);
  const [benefitDetail, setBenefitDetail] = useState<ConfigBenefitDetail>();
  const [authRoles, setAuthRoles] = useState<AuthRole[]>([]);
  const [gridApi, setGridApi] = useState<GridApi>();
  const [columnApi, setColumnApi] = useState<ColumnApi>();

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    if (!benefit) return;

    axios
      .get(
        `/api/config/product/${product_id}/benefit/${benefit.config_benefit_id}`,
        { signal }
      )
      .then((res) => {
        setBenefitDetail(res.data);
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
    if (!benefitDetail) return;
    if (!authRoles.length) return;
    if (!benefitDetail.benefit_auth) return;

    gridApi.setRowData(benefitDetail.benefit_auth);
  }, [gridApi, columnApi, benefitDetail, authRoles]);

  const onFirstDataRendered = () => {
    if (!columnApi) return;
    columnApi.autoSizeAllColumns();
  };

  const onDataEdit = (bnft: ConfigBenefitAuth) => {
    setBenefitDetail((prev) => {
      if (!prev) return prev;
      if (!prev.benefit_auth) {
        prev.benefit_auth = [bnft];
        console.log("here");
      } else {
        prev.benefit_auth = [...prev.benefit_auth, bnft];
        console.log("Herreeee");
      }
      return { ...prev };
    });
  };

  return (
    <div className="space-y-4">
      <ConfigBenefitDetailValues
        open={showBenefitPanel}
        onSave={onDataEdit}
        onClose={() => toggleOpenBenefitPanel(false)}
      />
      <div className="h-72">
        <Grid
          onGridReady={(params) => {
            setGridApi(params.api);
            setColumnApi(params.columnApi);
          }}
          defaultColDef={{
            filter: true,
            resizable: true,
            sortable: true,
          }}
          rowDragManaged={true}
          rowDragEntireRow={true}
          animateRows={true}
          onRowDragEnd={(params) => params.api.refreshCells()}
          context={{
            authRoles: authRoles,
          }}
          columnDefs={GRID_COLUMNS}
          onFirstDataRendered={onFirstDataRendered}
        />
      </div>

      <div className="flex justify-end">
        <AppButton
          transparent={true}
          onClick={() => toggleOpenBenefitPanel(true)}
        >
          New
        </AppButton>
      </div>
    </div>
  );
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
    valueGetter: (params) => {
      return `${params.data.default_value}%`;
    },
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
