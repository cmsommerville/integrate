import { AgGridReact } from "ag-grid-react";
import { GridOptions } from "ag-grid-community";

import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css";

const Grid = (props: GridOptions) => {
  return (
    <div className="ag-theme-alpine h-full w-full">
      <AgGridReact {...props}></AgGridReact>
    </div>
  );
};

export default Grid;
