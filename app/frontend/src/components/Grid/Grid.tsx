import { AgGridReact } from "ag-grid-react";
import { GridOptions } from "ag-grid-community";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const Grid = ({ defaultColDef, ...props }: GridOptions) => {
  return (
    <div className="ag-theme-alpine h-full w-full">
      <AgGridReact
        defaultColDef={{
          filter: true,
          sortable: true,
          flex: 1,
          ...defaultColDef,
        }}
        {...props}
      ></AgGridReact>
    </div>
  );
};

export default Grid;
