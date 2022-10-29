import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import { RadioGroup } from "@headlessui/react";
import _ from "lodash";
import {
  Accordion,
  SelectCensusSet,
  SelectSmokerStatus,
  SelectGender,
} from "@/pages/RatingWorkbench";
import { pivot } from "@/methods/data_munging";

function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const rateGrouper = (rate: any) => {
  return [
    rate.gender.config_attr_detail_label,
    rate.smoker_status.config_attr_detail_label,
    rate.relationship.config_attr_detail_label,
  ].join(":");
};

type RefMaster = {
  ref_id: number | string;
  ref_entity_code: string;
  ref_attr_code: string;
  ref_attr_label: string;
};

type ConfigProduct = {
  config_product_id: number | string;
  gender_rating_strategy: RefMaster;
  smoker_status_rating_strategy: RefMaster;
};

type SelectionAgeBand = {
  selection_age_band_id: number | string;
  selection_plan_id: number | string;
  lower_age_value: number;
  upper_age_value: number;
};

type ConfigRateGroup = {
  config_rate_group_id: number | string;
  config_product_id: number | string;
  config_rate_group_code: string;
  config_rate_group_label: string;
  unit_value: number;
  apply_discretionary_factor?: boolean | undefined | null;
};

type ConfigAttributeDetail = {
  config_attr_detail_id: number | string;
  config_attr_detail_code: string;
  config_attr_detail_label: string;
  is_composite_id?: boolean;
};

type SelectionRateTable = {
  selection_rate_table_id: number | string;
  selection_plan_id: number | string;
  selection_age_band_id: number | string;
  config_rate_group_id: number | string;
  config_gender_detail_id: number | string;
  config_smoker_status_detail_id: number | string;
  config_relationship_detail_id: number | string;
  age_band: SelectionAgeBand;
  smoker_status: ConfigAttributeDetail;
  gender: ConfigAttributeDetail;
  relationship: ConfigAttributeDetail;
  config_rate_group: ConfigRateGroup;
  annual_rate: number;
  discretionary_factor?: number | null | undefined;
};

interface IProps {
  product: ConfigProduct;
  rates: SelectionRateTable[];
}

const showRatingStrategies = ["rating"];

/**
 * Shows rates by age band as rows and each rate group as columns
 * @product a product object containing the gender and smoker status rating strategies
 * @rates the SelectionRateTable object
 * @returns a React component displaying the rates by age band and rate group
 */
export const RateDisplayTemplateAgeBand = ({ product, rates }: IProps) => {
  const [rateFilter, setRateFilter] = useState({
    rate_group: "",
    gender: "",
    smoker_status: "",
    relationship: "",
  });

  useEffect(() => {
    if (rates.length === 0) return;
    const initRateFilter = Object.keys(_.groupBy(rates, rateGrouper))[0].split(
      ":"
    );
    setRateFilter({
      gender: initRateFilter[0],
      smoker_status: initRateFilter[1],
      relationship: initRateFilter[2],
      rate_group: initRateFilter[3],
    });
  }, [rates]);

  const isLoaded = useMemo(() => {
    return product && product.config_product_id && rates && rates.length > 0;
  }, [product, rates]);

  const pivotedRates = useMemo(() => {
    if (rates.length === 0) return {};
    const pivoted = pivot(
      rates,
      [
        "selection_plan_id",
        "selection_age_band_id",
        "config_gender_detail_id",
        "config_smoker_status_detail_id",
        "config_relationship_detail_id",
        "gender",
        "smoker_status",
        "relationship",
        "age_band",
      ],
      "config_rate_group.config_rate_group_label",
      "annual_rate"
    );

    return _.groupBy(pivoted, rateGrouper);
  }, [rates]);

  const distinctGenders = useMemo(() => {
    return _.uniq(
      rates.map((rate: any) => rate.gender.config_attr_detail_label)
    );
  }, [rates]);

  const distinctSmokerStatuses = useMemo(() => {
    return _.uniq(
      rates.map((rate: any) => rate.smoker_status.config_attr_detail_label)
    );
  }, [rates]);

  const distinctRelationships = useMemo(() => {
    return _.uniq(
      rates.map((rate: any) => rate.relationship.config_attr_detail_label)
    );
  }, [rates]);

  const distinctRateGroups = useMemo(() => {
    return _.uniq(
      rates.map((rate: any) => rate.config_rate_group.config_rate_group_label)
    ) as string[];
  }, [rates]);

  const displayRates = useMemo(() => {
    const key = [
      rateFilter.gender,
      rateFilter.smoker_status,
      rateFilter.relationship,
    ].join(":");
    let display_rates = pivotedRates[key];
    if (!display_rates) return [];
    return display_rates.sort((a: any, b: any) => {
      return a.age_band.lower_age_value < b.age_band.lower_age_value ? -1 : 1;
    });
  }, [pivotedRates, rateFilter]);

  return (
    <>
      {isLoaded ? (
        <div className="my-8 grid grid-cols-2 p-4 ">
          <div className="col-span-1 -my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div className="inline-block py-2 align-middle md:px-6 lg:px-8 min-w-full">
              <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-l-lg md:rounded-br-lg">
                <table className="min-w-full divide-y divide-gray-300">
                  {/* <caption className="text-lg font-semibold bg-primary-700 text-gray-50 py-2">
                    Annual Rates
                  </caption> */}
                  <thead className="bg-gray-50">
                    <tr>
                      <th
                        scope="col"
                        className="px-6 py-3 text-left text-sm font-semibold text-gray-900"
                      >
                        Age Band
                      </th>

                      {distinctRateGroups.map((rate_group) => {
                        return (
                          <th
                            key={rate_group}
                            scope="col"
                            className="px-6 py-3 text-sm font-semibold text-gray-900 text-right"
                          >
                            {rate_group}
                          </th>
                        );
                      })}
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200 bg-white">
                    {displayRates && displayRates.length > 0
                      ? displayRates.map((rate: any) => (
                          <tr key={rate.selection_age_band_id}>
                            <td className="whitespace-nowrap px-3 py-3 text-sm text-gray-500">
                              {rate.age_band.lower_age_value} -{" "}
                              {rate.age_band.upper_age_value}
                            </td>
                            {distinctRateGroups.map((rate_group) => {
                              return (
                                <td
                                  key={rate_group}
                                  className="whitespace-nowrap px-3 py-3 text-sm text-gray-500 text-right"
                                >
                                  {rate[rate_group].toFixed(5)}
                                </td>
                              );
                            })}
                          </tr>
                        ))
                      : null}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          <div className="col-span-1 flex flex-col">
            <Accordion />
            {/* <div className="rounded-r-lg shadow-lg px-4 py-8 space-y-8">
              {showRatingStrategies.includes(
                product.gender_rating_strategy.ref_attr_code
              ) ? (
                <div>
                  <div className="flex items-center justify-between">
                    <h2 className="text-sm font-medium text-gray-900">
                      Gender
                    </h2>
                  </div>

                  <RadioGroup
                    value={rateFilter.gender}
                    onChange={(val: string) =>
                      setRateFilter((prev) => ({ ...prev, gender: val }))
                    }
                    className="mt-2"
                  >
                    <RadioGroup.Label className="sr-only">
                      {" "}
                      Choose a gender{" "}
                    </RadioGroup.Label>
                    <div className="grid grid-cols-2 gap-3">
                      {distinctGenders.map((option: any) => (
                        <RadioGroup.Option
                          key={option}
                          value={option}
                          className={({ active, checked }) =>
                            classNames(
                              active
                                ? "ring-2 ring-offset-2 ring-primary-500"
                                : "",
                              checked
                                ? "bg-primary-600 border-transparent text-white hover:bg-primary-700"
                                : "bg-white border-gray-200 text-gray-900 hover:bg-gray-50",
                              "cursor-pointer border rounded-md py-1 px-1 flex items-center justify-center text-sm font-medium sm:flex-1"
                            )
                          }
                        >
                          <RadioGroup.Label as="span">
                            {option}
                          </RadioGroup.Label>
                        </RadioGroup.Option>
                      ))}
                    </div>
                  </RadioGroup>
                </div>
              ) : null}
              {showRatingStrategies.includes(
                product.smoker_status_rating_strategy.ref_attr_code
              ) ? (
                <div>
                  <div className="flex items-center justify-between">
                    <h2 className="text-sm font-medium text-gray-900">
                      Smoker Status
                    </h2>
                  </div>

                  <RadioGroup
                    value={rateFilter.smoker_status}
                    onChange={(val: string) =>
                      setRateFilter((prev) => ({ ...prev, smoker_status: val }))
                    }
                    className="mt-2"
                  >
                    <RadioGroup.Label className="sr-only">
                      {" "}
                      Choose a smoker status{" "}
                    </RadioGroup.Label>
                    <div className="grid grid-cols-2 gap-3">
                      {distinctSmokerStatuses.map((option: any) => (
                        <RadioGroup.Option
                          key={option}
                          value={option}
                          className={({ active, checked }) =>
                            classNames(
                              active
                                ? "ring-2 ring-offset-2 ring-primary-500"
                                : "",
                              checked
                                ? "bg-primary-600 border-transparent text-white hover:bg-primary-700"
                                : "bg-white border-gray-200 text-gray-900 hover:bg-gray-50",
                              "cursor-pointer border rounded-md py-1 px-1 flex items-center justify-center text-sm font-medium sm:flex-1"
                            )
                          }
                        >
                          <RadioGroup.Label as="span">
                            {option}
                          </RadioGroup.Label>
                        </RadioGroup.Option>
                      ))}
                    </div>
                  </RadioGroup>
                </div>
              ) : null}
              <div>
                <div className="flex items-center justify-between">
                  <h2 className="text-sm font-medium text-gray-900">
                    Relationship
                  </h2>
                </div>

                <RadioGroup
                  value={rateFilter.relationship}
                  onChange={(val: string) =>
                    setRateFilter((prev) => ({ ...prev, relationship: val }))
                  }
                  className="mt-2"
                >
                  <RadioGroup.Label className="sr-only">
                    {" "}
                    Choose a relationship{" "}
                  </RadioGroup.Label>
                  <div className="grid grid-cols-3 gap-3">
                    {distinctRelationships.map((option: any) => (
                      <RadioGroup.Option
                        key={option}
                        value={option}
                        className={({ active, checked }) =>
                          classNames(
                            active
                              ? "ring-2 ring-offset-2 ring-primary-500"
                              : "",
                            checked
                              ? "bg-primary-600 border-transparent text-white hover:bg-primary-700"
                              : "bg-white border-gray-200 text-gray-900 hover:bg-gray-50",
                            "cursor-pointer border rounded-md py-1 px-1 flex items-center justify-center text-sm font-medium sm:flex-1"
                          )
                        }
                      >
                        <RadioGroup.Label as="span">{option}</RadioGroup.Label>
                      </RadioGroup.Option>
                    ))}
                  </div>
                </RadioGroup>
              </div>
            </div> */}
            <div className="h-full w-full"></div>
          </div>
        </div>
      ) : null}
    </>
  );
};
