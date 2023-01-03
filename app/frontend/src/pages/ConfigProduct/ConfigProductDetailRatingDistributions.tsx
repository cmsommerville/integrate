import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import {
  ConfigProduct_Basic,
  ConfigAttributeDistributionSet_Gender,
  ConfigAttributeDistributionSet_SmokerStatus,
  ConfigAgeDistributionSet,
  ConfigProduct_DistributionSets,
} from "@/types/config";
import { CalendarIcon, HeartIcon, MoonIcon } from "@heroicons/react/24/outline";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";
import { Breadcrumb, PageTitle } from "./Components";

const PAGE_DETAILS = {
  id: "distributions",
  title: "Distributions",
  subtitle:
    "Specify the distributions used for smoker disposition, gender, and age...",
};

const ConfigProductDetailRatingDistributions = () => {
  const { product_id } = useParams();

  const [isDirty, setIsDirty] = useState(false);
  const [isValid, setIsValid] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  const [product, setProduct] = useState<
    ConfigProduct_Basic & ConfigProduct_DistributionSets
  >();
  const [genderDists, setGenderDists] = useState<
    ConfigAttributeDistributionSet_Gender[]
  >([]);
  const [smokerDists, setSmokerDists] = useState<
    ConfigAttributeDistributionSet_SmokerStatus[]
  >([]);
  const [ageDists, setAgeDists] = useState<ConfigAgeDistributionSet[]>([]);

  const [selection, setSelection] = useState<ConfigProduct_DistributionSets>(
    DEFAULT_PRODUCT_DISTS
  );

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/config/product/${product_id}`, { signal })
      .then((res) => res.json())
      .then((res) => {
        setProduct(res);
        if (res.gender_distribution_set_id) {
          setSelection({
            gender_distribution_set_id: res.gender_distribution_set_id,
            smoker_status_distribution_set_id:
              res.smoker_status_distribution_set_id,
            age_distribution_set_id: res.age_distribution_set_id,
          });
        }
      });
    return () => {
      controller.abort();
    };
  }, [product_id]);

  useEffect(() => {
    const controller1 = new AbortController();
    const signal1 = controller1.signal;
    const controller2 = new AbortController();
    const signal2 = controller2.signal;
    const controller3 = new AbortController();
    const signal3 = controller3.signal;

    fetch("/api/config/attribute-distribution/sets/smoker_status", {
      signal: signal1,
    })
      .then((res) => res.json())
      .then((res) => {
        setSmokerDists(res);
      });

    fetch("/api/config/attribute-distribution/sets/gender", {
      signal: signal2,
    })
      .then((res) => res.json())
      .then((res) => {
        setGenderDists(res);
      });

    fetch("/api/config/age-distribution/sets", { signal: signal3 })
      .then((res) => res.json())
      .then((res) => {
        setAgeDists(res);
      });
    return () => {
      controller1.abort();
      controller2.abort();
      controller3.abort();
    };
  }, []);

  const setter = (key: keyof ConfigProduct_DistributionSets, val: number) => {
    setSelection((prev) => ({ ...prev, [key]: val }));
    setIsDirty(true);
  };

  const clickHandler = () => {
    if (!isDirty) return;
    setIsSaving(true);
    fetch(`/api/config/product/${product_id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(selection),
    })
      .then((res) => {})
      .finally(() => {
        setIsSaving(false);
      });
  };

  return (
    <>
      <PageTitle title={PAGE_DETAILS.title} subtitle={PAGE_DETAILS.subtitle}>
        <AppButton disabled={!isValid} onClick={clickHandler}>
          Next
        </AppButton>
      </PageTitle>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-2 flex flex-col space-y-6">
          <AppPanel className="pt-0 pl-0 pr-0 h-fit space-y-6">
            <>
              <h3 className="font-normal text-white py-4 px-4 bg-primary-700 rounded-t-lg flex space-x-2">
                <HeartIcon className="h-6 w-6" aria-hidden="true" />
                <span>Genders</span>
              </h3>
              <fieldset className="px-4 pb-4" name="attr_set">
                <legend className="sr-only">Gender</legend>
                <div className="space-y-5">
                  {genderDists.map((dist) => (
                    <div
                      key={dist.config_attr_distribution_set_id}
                      className="relative flex items-start"
                    >
                      <div className="flex h-5 items-center">
                        <input
                          id={`${dist.config_attr_type_code}-${dist.config_attr_distribution_set_id}`}
                          aria-describedby={`${dist.config_attr_distribution_set_id}-description`}
                          name="gender_attr_set"
                          type="radio"
                          checked={
                            dist.config_attr_distribution_set_id ===
                            selection.gender_distribution_set_id
                          }
                          onChange={() =>
                            setter(
                              "gender_distribution_set_id",
                              dist.config_attr_distribution_set_id
                            )
                          }
                          className="h-4 w-4 border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label
                          htmlFor={`${dist.config_attr_type_code}-${dist.config_attr_distribution_set_id}`}
                          className="font-medium cursor-pointer"
                        >
                          {dist.config_attr_distribution_set_label}
                        </label>
                      </div>
                    </div>
                  ))}
                </div>
              </fieldset>
            </>
          </AppPanel>

          <AppPanel className="pt-0 pl-0 pr-0 h-fit space-y-6">
            <>
              <h3 className="font-normal text-white py-4 px-4 bg-primary-700 rounded-t-lg flex space-x-2">
                <MoonIcon className="h-6 w-6" aria-hidden="true" />
                <span>Smoker Dispositions</span>
              </h3>
              <fieldset className="px-4 pb-4" name="attr_set">
                <legend className="sr-only">Smoker Dispositions</legend>
                <div className="space-y-5">
                  {smokerDists.map((dist) => (
                    <div
                      key={dist.config_attr_distribution_set_id}
                      className="relative flex items-start"
                    >
                      <div className="flex h-5 items-center">
                        <input
                          id={`${dist.config_attr_type_code}-${dist.config_attr_distribution_set_id}`}
                          aria-describedby={`${dist.config_attr_distribution_set_id}-description`}
                          name="smoker_status_attr_set"
                          type="radio"
                          checked={
                            dist.config_attr_distribution_set_id ===
                            selection.smoker_status_distribution_set_id
                          }
                          onChange={() =>
                            setter(
                              "gender_distribution_set_id",
                              dist.config_attr_distribution_set_id
                            )
                          }
                          className="h-4 w-4 border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label
                          htmlFor={`${dist.config_attr_type_code}-${dist.config_attr_distribution_set_id}`}
                          className="font-medium cursor-pointer"
                        >
                          {dist.config_attr_distribution_set_label}
                        </label>
                      </div>
                    </div>
                  ))}
                </div>
              </fieldset>
            </>
          </AppPanel>
        </div>
        <div className="col-span-2 flex flex-col space-y-4">
          <AppPanel className="pt-0 pl-0 pr-0 h-fit space-y-6">
            <>
              <h3 className="font-normal text-white py-4 px-4 bg-primary-700 rounded-t-lg flex space-x-2">
                <CalendarIcon className="h-6 w-6" aria-hidden="true" />
                <span>Age</span>
              </h3>
              <fieldset className="px-4 pb-4" name="attr_set">
                <legend className="sr-only">Age</legend>
                <div className="space-y-5">
                  {ageDists.map((dist) => (
                    <div
                      key={dist.config_age_distribution_set_id}
                      className="relative flex items-start"
                    >
                      <div className="flex h-5 items-center">
                        <input
                          id={`$age-${dist.config_age_distribution_set_id}`}
                          aria-describedby={`${dist.config_age_distribution_set_id}-description`}
                          name="age_set"
                          type="radio"
                          checked={
                            dist.config_age_distribution_set_id ===
                            selection.age_distribution_set_id
                          }
                          onChange={() =>
                            setter(
                              "age_distribution_set_id",
                              dist.config_age_distribution_set_id
                            )
                          }
                          className="h-4 w-4 border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label
                          htmlFor={`age-${dist.config_age_distribution_set_id}`}
                          className="font-medium cursor-pointer"
                        >
                          {dist.config_age_distribution_set_label}
                        </label>
                      </div>
                    </div>
                  ))}
                </div>
              </fieldset>
            </>
          </AppPanel>
        </div>
        <div className="col-span-2 flex flex-col items-end">
          <Breadcrumb step="distributions" />
        </div>
      </div>
    </>
  );
};

const DEFAULT_PRODUCT_DISTS = {
  gender_distribution_set_id: undefined,
  smoker_status_distribution_set_id: undefined,
  age_distribution_set_id: undefined,
} as ConfigProduct_DistributionSets;

export default ConfigProductDetailRatingDistributions;
