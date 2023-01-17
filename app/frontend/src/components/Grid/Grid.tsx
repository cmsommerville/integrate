import { AgGridReact } from "ag-grid-react";
import { GridOptions } from "ag-grid-community";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";
import "./Grid.scss";

const Grid = ({ defaultColDef, ...props }: GridOptions) => {
  return (
    <div className="ag-theme-alpine ag-theme-integrate h-full w-full">
      <AgGridReact
        defaultColDef={{
          filter: true,
          sortable: true,
          flex: 1,
          ...defaultColDef,
        }}
        {...props}
        className="h-full w-full"
      ></AgGridReact>
    </div>
  );
};

export default Grid;
