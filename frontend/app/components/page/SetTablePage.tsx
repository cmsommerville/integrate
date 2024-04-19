"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { PiPlus, PiPencilSimple, PiWarningCircle } from "react-icons/pi";
import AppCard from "../ui/AppCard";
import AppGrid from "../grid/AppGrid";
import AppButton from "../ui/AppButton";
import { ColDef, GridOptions } from "ag-grid-community";
import { classNames } from "@/utils";

interface Routes<T> {
  new: () => Promise<string>;
  edit: (row: T) => Promise<string>;
}

export interface SetTablePageProps<T> {
  title: string;
  rowData: T[];
  columnDefs: ColDef[];
  routes: Routes<T>;
  className?: string;
  children?: React.ReactNode;
  gridOptions?: GridOptions;
}

interface SetTablePageSubtitleProps {
  children: React.ReactNode;
}

export const SetTablePageSubtitle = ({
  children,
}: SetTablePageSubtitleProps) => {
  return <p className="text-gray-400 text-xs">{children}</p>;
};

export default function SetTablePage<T>(props: SetTablePageProps<T>) {
  const router = useRouter();
  const [selectedRow, setSelectedRow] = useState<T>();
  const [editButtonStatus, setEditButtonStatus] = useState<"VALID" | "INVALID">(
    "VALID"
  );
  const [errorMessage, setErrorMessage] = useState("");

  const { onRowClicked, onRowDoubleClicked, ...gridOptions } =
    props.gridOptions ?? {};

  const newHandler = async () => {
    const to_route = await props.routes.new();
    router.push(to_route);
  };

  const onEditRow = async () => {
    if (!selectedRow) {
      setEditButtonStatus("INVALID");
      setErrorMessage("Select a row to edit!");
      return;
    }
    const to_route = await props.routes.edit(selectedRow);
    router.push(to_route);
  };

  useEffect(() => {
    if (editButtonStatus === "VALID") return;
    const timer = setTimeout(() => {
      setEditButtonStatus("VALID");
    }, 500);

    return () => {
      clearTimeout(timer);
    };
  }, [editButtonStatus]);

  return (
    <AppCard className={classNames("space-y-4", props.className ?? "")}>
      <div>
        <h2 className="text-gray-600 text-lg">{props.title}</h2>
        {props.children}
      </div>
      <div className="space-y-8">
        <AppGrid
          height={"90%"}
          columnDefs={props.columnDefs}
          rowData={props.rowData}
          onFirstDataRendered={(params) => params.api.sizeColumnsToFit()}
          rowSelection="single"
          onRowClicked={(params) => {
            if (onRowClicked) {
              onRowClicked(params);
            }
            setSelectedRow(params.data);
            setErrorMessage("");
          }}
          onRowDoubleClicked={(params) => {
            if (onRowDoubleClicked) {
              onRowDoubleClicked(params);
            }
            onEditRow();
          }}
          {...gridOptions}
        />
        <div className="space-y-4">
          <div className="w-full flex justify-end space-x-4">
            <AppButton
              variant="primary"
              onClick={newHandler}
              className="flex items-center space-x-1"
            >
              <PiPlus /> <span>New</span>
            </AppButton>
            <AppButton
              variant="dark-transparent"
              onClick={onEditRow}
              invalid={editButtonStatus === "INVALID"}
              className="flex items-center space-x-1"
            >
              <PiPencilSimple /> <span>Edit</span>
            </AppButton>
          </div>

          <div className="w-full flex justify-end items-center text-sm text-red-500 font-semibold min-h-full space-x-1">
            {errorMessage ? (
              <>
                <PiWarningCircle className="h-4 w-4" />
                <span>{errorMessage}</span>
              </>
            ) : (
              ""
            )}
          </div>
        </div>
      </div>
    </AppCard>
  );
}
