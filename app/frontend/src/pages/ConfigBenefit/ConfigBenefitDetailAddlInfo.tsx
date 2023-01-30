import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams, useNavigate } from "react-router";
import { FolderPlusIcon } from "@heroicons/react/20/solid";
import {
  ConfigBenefit,
  RefUnitType,
  ConfigCoverage,
  ConfigRateGroup,
} from "./types";
import axios from "@/services/axios";
import AppRadioSelect from "@/components/AppRadioSelect";
import AppButton from "@/components/AppButton";
import { PageTitle } from "../ConfigProduct/Components";
import { AppPanel } from "@/components/AppPanel";
import { Tabs, TabCode } from "./Components";

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const ConfigBenefitDetailAddlInfo = () => {
  const { product_id, benefit_id } = useParams();
  const navigate = useNavigate();

  const [isSaving, setIsSaving] = useState(false);
  const [isDirty, setIsDirty] = useState(false);

  const [benefit, setBenefit] = useState<Partial<ConfigBenefit>>({});
  const [refUnitTypes, setRefUnitTypes] = useState<Partial<RefUnitType>[]>([]);
  const [coverages, setCoverages] = useState<Partial<ConfigCoverage>[]>([]);
  const [rateGroups, setRateGroups] = useState<Partial<ConfigRateGroup>[]>([]);

  const isValid = useMemo(() => {
    // return Object.entries(benefit).reduce((isValid, [k, v]) => {
    //   return isValid && validator(k as keyof ConfigBenefit, v);
    // }, true);
    return true;
  }, []);

  const benefitSetter = useCallback(
    (key: keyof ConfigBenefit, val: any) => {
      setBenefit((old) => ({ ...old, [key]: val }));
      setIsDirty(true);
    },
    [setBenefit]
  );

  const onSave = () => {
    axios
      .patch(`/api/config/product/${product_id}/benefit/${benefit_id}`, {})
      .then((res) => {
        console.log(res);
      });
  };

  const onTabClick = (selected: TabCode) => {
    navigate(
      `/app/config/product/${product_id}/benefit/${benefit_id}/${selected}`
    );
  };

  useEffect(() => {
    if (!benefit_id) return;
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/config/product/${product_id}/benefit/${benefit_id}`, { signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get benefit");
        }
        return res.json();
      })
      .then((res) => {
        const { config_coverage_id, config_rate_group_id, unit_type_id } = res;
        setBenefit({ config_coverage_id, config_rate_group_id, unit_type_id });
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, [product_id, benefit_id]);

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
    <>
      <PageTitle
        title="Benefit Additional Info"
        subtitle="Assign a coverage, rate group, and unit type..."
      >
        <div className="flex items-end">
          <AppButton
            disabled={!isValid || !isDirty}
            isLoading={isSaving}
            onClick={onSave}
          >
            Save
          </AppButton>
        </div>
      </PageTitle>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-4 flex flex-col space-y-4">
          <AppPanel className="pb-16 pt-2 h-fit">
            <>
              <Tabs selected="addl" onClick={onTabClick} />
              <div className="flex justify-start">
                <form className="space-y-6 w-full">
                  <div className="grid grid-cols-5 gap-x-3 gap-y-1">
                    <div className="col-span-4">
                      <AppRadioSelect
                        as="select"
                        items={coverages}
                        defaultValue={benefit.config_coverage_id}
                        label="Coverage"
                        itemId="config_coverage_id"
                        itemLabel="config_coverage_label"
                        onClick={(item) => {
                          benefitSetter(
                            "config_coverage_id",
                            item.config_coverage_id
                          );
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
                        defaultValue={benefit.config_rate_group_id}
                        itemId="config_rate_group_id"
                        itemLabel="config_rate_group_label"
                        onClick={(item) => {
                          benefitSetter(
                            "config_rate_group_id",
                            item.config_rate_group_id
                          );
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
                      The rates for benefits in the same rate group will be
                      combined for the final rate.
                    </p>
                  </div>
                  <div className="grid grid-cols-5 gap-x-3">
                    <div className="col-span-4">
                      <AppRadioSelect
                        as="select"
                        items={refUnitTypes}
                        defaultValue={benefit.unit_type_id}
                        label="Unit Type"
                        itemId="ref_id"
                        itemLabel={(item) => {
                          return (
                            item.ref_attr_label +
                            (item.ref_attr_symbol
                              ? ` (${item.ref_attr_symbol})`
                              : "")
                          );
                        }}
                        onClick={(item) => {
                          benefitSetter("unit_type", item);
                          benefitSetter("unit_type_id", item.ref_id);
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
            </>
          </AppPanel>
        </div>
      </div>
    </>
  );
};

export default ConfigBenefitDetailAddlInfo;
