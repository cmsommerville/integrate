"use client";
import { AgGridReact, AgGridReactProps, AgReactUiProps } from "ag-grid-react"; // React Grid Logic
import { columnTypes } from "./columnTypes";

import "ag-grid-community/styles/ag-grid.css"; // Core CSS
import "ag-grid-community/styles/ag-theme-alpine.css"; // Theme
import "./AppGrid.css";
import StoplightComponent from "./StoplightComponent";

type Unit = "%" | "px" | "em" | "vh" | "vh";
type HeightProp = `${number}${Unit}`;

interface AppGridProps extends AgGridReactProps, AgReactUiProps {
  height?: HeightProp;
}

const COMPONENTS = {
  StoplightComponent,
};

export default function AppGrid({ height, ...props }: AppGridProps) {
  return (
    <div className="ag-theme-alpine" style={height ? { height } : {}}>
      <AgGridReact
        domLayout="autoHeight"
        columnTypes={columnTypes}
        components={COMPONENTS}
        {...props}
      />
    </div>
  );
}
