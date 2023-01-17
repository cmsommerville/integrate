import { useState, useEffect } from "react";
import { FolderPlusIcon } from "@heroicons/react/20/solid";
import {
  ConfigBenefit,
  RefBenefit,
  RefUnitType,
  ConfigCoverage,
  ConfigRateGroup,
} from "./types";
import AppRadioSelect from "@/components/AppRadioSelect";
import AppButton from "@/components/AppButton";

type Props = {
  product_id: number | string;
  benefit: ConfigBenefit;
  onChange(key: string, val: any): void;
};

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const ConfigBenefitDetailValues = ({
  product_id,
  benefit,
  onChange,
  ...props
}: Props) => {
  const [refUnitTypes, setRefUnitTypes] = useState<RefUnitType[]>([]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/ref/unit-types`, { signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get unit types");
        }
        return res.json();
      })
      .then((res) => {
        setRefUnitTypes(res);
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
  return (
    <div className="flex justify-start">
      <form className="space-y-6 w-full">
        <div className="grid grid-cols-5 gap-x-3">
          <div className="col-span-4">
            <AppRadioSelect
              as="select"
              items={refUnitTypes}
              label="Unit Type"
              itemId="ref_id"
              itemLabel={(item) => {
                return (
                  item.ref_attr_label +
                  (item.ref_attr_symbol ? ` (${item.ref_attr_symbol})` : "")
                );
              }}
              onClick={(item) => {
                onChange("unit_type", item);
                onChange("unit_type_id", item.ref_id);
              }}
            />
          </div>
          <button
            type="button"
            className="relative -ml-px inline-flex items-center space-x-2 rounded-md border border-gray-300 bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 justify-self-start self-end"
            onClick={(e) => e.preventDefault()}
          >
            <FolderPlusIcon
              className="h-5 w-5 text-gray-400"
              aria-hidden="true"
            />
            <span>Add</span>
          </button>
        </div>
      </form>
    </div>
  );
};

export default ConfigBenefitDetailValues;
