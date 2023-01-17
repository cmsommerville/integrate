import { useState, useEffect } from "react";
import { FolderPlusIcon } from "@heroicons/react/20/solid";
import { ConfigBenefit, RefBenefit } from "./types";
import AppRadioSelect from "@/components/AppRadioSelect";

type Props = {
  product_id: number | string;
  benefit: ConfigBenefit;
  onChange(key: string, val: any): void;
};

const ConfigBenefitDetailBasicInfo = ({
  product_id,
  benefit,
  onChange,
  ...props
}: Props) => {
  const [refBenefits, setRefBenefits] = useState<RefBenefit[]>([]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/ref/benefits`, { signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get benefits");
        }
        return res.json();
      })
      .then((res) => {
        setRefBenefits(res);
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
        <div className="space-y-1">
          <label
            htmlFor="config_benefit_version_code"
            className="block text-sm font-medium text-gray-700"
          >
            Version Code
          </label>

          <input
            type="text"
            name="config_benefit_version_code"
            id="config_benefit_version_code"
            className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
            onChange={(e) =>
              onChange("config_benefit_version_code", e.target.value)
            }
            value={benefit.config_benefit_version_code ?? ""}
          />
          <p className="text-sm text-gray-400">
            Enter a unique code to represent this version of this benefit.
          </p>
        </div>
        <div className="space-y-1">
          <div className="flex items-end space-x-3">
            <AppRadioSelect
              as="select"
              items={refBenefits}
              label="Benefit"
              itemId="ref_id"
              itemLabel="ref_attr_label"
              onClick={(item) => {
                onChange("ref_benefit", item);
                onChange("ref_benefit_id", item.ref_id);
              }}
            />
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
          <p className="text-sm text-gray-400">
            Select the benefit code or add a new one.
          </p>
        </div>
        <div>
          <label
            htmlFor="config_benefit_description"
            className="block text-sm font-medium text-gray-700"
          >
            Benefit Description
          </label>
          <div className="mt-1">
            <textarea
              rows={4}
              name="config_benefit_description"
              id="config_benefit_description"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              defaultValue={benefit.config_benefit_description}
              onChange={(e) => {
                onChange("config_benefit_description", e.target.value);
              }}
            />
          </div>
        </div>
      </form>
    </div>
  );
};

export default ConfigBenefitDetailBasicInfo;
