import SetTablePage from "./components/page/SetTablePage";
import { ColDef } from "ag-grid-community";

const COL_DEFS: ColDef[] = [
  {
    field: "id",
    headerName: "Id",
    type: "number0",
  },
  {
    field: "name",
    headerName: "Name",
  },
];

const ROW_DATA = [
  { id: 1000.12, name: "Chandler" },
  { id: 2111, name: "Sally" },
  { id: 3000, name: "Collins" },
  { id: 4000, name: "Ellison" },
  { id: 4000, name: "Ellison" },
  { id: 4000, name: "Ellison" },
  { id: 4000, name: "Ellison" },
  { id: 4000, name: "Ellison" },
];

const getData = async () => {
  const data = await ROW_DATA;
  return data;
};

export default async function Home() {
  const row_data = await getData();

  async function route_edit(row: { id: number; name: string }) {
    "use server";
    return `/config?q=${row.name}`;
  }
  async function route_new() {
    "use server";
    return `/config`;
  }
  return (
    <SetTablePage
      title="Users"
      className="w-1/2"
      rowData={row_data}
      columnDefs={COL_DEFS}
      routes={{ edit: route_edit, new: route_new }}
    >
      <p className="text-gray-400 text-xs">Please select a user to edit!</p>
    </SetTablePage>
  );
}
