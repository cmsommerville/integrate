import { useState, useEffect, useMemo, useCallback } from "react";
import { useNavigate, useParams } from "react-router";
import { FolderPlusIcon } from "@heroicons/react/20/solid";
import { ConfigBenefit, RefBenefit } from "./types";
import axios from "@/services/axios";
import AppRadioSelect from "@/components/AppRadioSelect";
import AppButton from "@/components/AppButton";
import { PageTitle } from "../ConfigProduct/Components";
import { AppPanel } from "@/components/AppPanel";
import { Tabs, TabCode } from "./Components";

const ConfigBenefitDetailBasicInfo = () => {
  const { product_id, benefit_id } = useParams();
  const navigate = useNavigate();
  const [benefit, setBenefit] = useState<Partial<ConfigBenefit>>({});
  const [refBenefits, setRefBenefits] = useState<Partial<RefBenefit>[]>([]);

  const [isSaving, setIsSaving] = useState(false);
  const [isDirty, setIsDirty] = useState(false);

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

  const onTabClick = (selected: TabCode) => {
    navigate(
      `/app/config/product/${product_id}/benefit/${benefit_id}/${selected}`
    );
  };

  const onSave = () => {
    axios
      .patch(`/api/config/product/${product_id}/benefit/${benefit_id}`, {})
      .then((res) => {
        console.log(res);
      });
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
        setBenefit(res);
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
    <>
      <PageTitle
        title="Benefit Setup"
        subtitle="Give this benefit a name and tell us when it's effective..."
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
              <Tabs selected="basic" onClick={onTabClick} />
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
                        benefitSetter(
                          "config_benefit_version_code",
                          e.target.value
                        )
                      }
                      value={benefit.config_benefit_version_code ?? ""}
                    />
                    <p className="text-sm text-gray-400">
                      Enter a unique code to represent this version of this
                      benefit.
                    </p>
                  </div>
                  <div className="space-y-1">
                    <div className="flex items-end space-x-3">
                      <AppRadioSelect
                        as="select"
                        items={refBenefits}
                        defaultValue={benefit.ref_benefit?.ref_id}
                        label="Benefit"
                        itemId="ref_id"
                        itemLabel="ref_attr_label"
                        onClick={(item) => {
                          benefitSetter("ref_benefit", item);
                          benefitSetter("ref_benefit_id", item.ref_id);
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
                        className="block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm placeholder:text-gray-400"
                        defaultValue={benefit.config_benefit_description}
                        onChange={(e) => {
                          benefitSetter(
                            "config_benefit_description",
                            e.target.value
                          );
                        }}
                        placeholder="Enter a user-friendly description of this benefit..."
                      />
                    </div>
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

export default ConfigBenefitDetailBasicInfo;
