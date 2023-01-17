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

const ConfigBenefitDetailAddlInfo = ({
  product_id,
  benefit,
  onChange,
  ...props
}: Props) => {
  const [refUnitTypes, setRefUnitTypes] = useState<RefUnitType[]>([]);
  const [coverages, setCoverages] = useState<ConfigCoverage[]>([]);
  const [rateGroups, setRateGroups] = useState<ConfigRateGroup[]>([]);

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
  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/config/product/${product_id}/coverages`, {
      signal,
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get coverages");
        }
        return res.json();
      })
      .then((res) => {
        setCoverages(res);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, [product_id]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/config/product/${product_id}/rate-groups`, {
      signal,
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get rate groups");
        }
        return res.json();
      })
      .then((res) => {
        setRateGroups(res);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, [product_id]);
  return (
    <div className="flex justify-start">
      <form className="space-y-6 w-full">
        <div className="grid grid-cols-5 gap-x-3 gap-y-1">
          <div className="col-span-4">
            <AppRadioSelect
              as="select"
              items={coverages}
              label="Coverage"
              itemId="config_coverage_id"
              itemLabel="config_coverage_label"
              onClick={(item) => {
                onChange("config_coverage_id", item.config_coverage_id);
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
          <p className="col-span-4 text-sm text-gray-400">
            A coverage is a grouping of benefits.
          </p>
        </div>

        <div className="grid grid-cols-5 gap-x-3 gap-y-1">
          <div className="col-span-4">
            <AppRadioSelect
              as="select"
              items={rateGroups}
              label="Rate Group"
              itemId="config_rate_group_id"
              itemLabel="config_rate_group_label"
              onClick={(item) => {
                onChange("config_rate_group_id", item.config_rate_group_id);
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
          <p className="col-span-4 text-sm text-gray-400">
            The rates for benefits in the same rate group will be combined for
            the final rate.
          </p>
        </div>
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

export default ConfigBenefitDetailAddlInfo;
