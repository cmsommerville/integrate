import { DateTime } from "luxon";
import { ColDef } from "ag-grid-community";

export const columnTypes: { [k: string]: ColDef } = {
  dollars: {
    cellClass: "tabular-nums",
    valueFormatter: (params) => {
      try {
        return params.value.toLocaleString("en-US", {
          style: "currency",
          currency: "USD",
          maximumFractionDigits: 0,
        });
      } catch (err) {
        return params.value;
      }
    },
  },
  dollars_and_cents: {
    cellClass: "tabular-nums",
    valueFormatter: (params) => {
      try {
        return params.value.toLocaleString("en-US", {
          style: "currency",
          currency: "USD",
          minimumFractionDigits: 2,
          maximumFractionDigits: 2,
        });
      } catch (err) {
        return params.value;
      }
    },
  },
  number0: {
    valueFormatter: (params) => {
      try {
        return params.value.toLocaleString("en-US", {
          maximumFractionDigits: 0,
        });
      } catch (err) {
        return params.value;
      }
    },
  },
  date: {
    valueFormatter: (params) => {
      try {
        return DateTime.fromISO(params.value).toLocaleString();
      } catch (err) {
        return params.value;
      }
    },
  },
};
