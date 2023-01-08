import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import { Link } from "react-router-dom";
import { Switch } from "@headlessui/react";
import {
  ConfigProduct_Basic,
  ConfigProduct_EmployerPaid,
} from "@/types/config";
import { RefCensusStrategy } from "./types";
import { ChevronRightIcon, ChevronLeftIcon } from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";
import AppRadioSelect from "@/components/AppRadioSelect";
import { Breadcrumb, PageTitle } from "./Components";

const PAGE_DETAILS = {
  id: "employer-paid",
  title: "Employer Paid",
  subtitle: "Specify employer paid options...",
};

const ConfigProductDetailCensus = () => {
  const { product_id } = useParams();

  const [isDirty, setIsDirty] = useState(false);
  const [isValid, setIsValid] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  const [product, setProduct] = useState<
    ConfigProduct_Basic & ConfigProduct_EmployerPaid
  >();
  const [strategies, setStrategies] = useState<RefCensusStrategy[]>([]);

  const [selection, setSelection] = useState<ConfigProduct_EmployerPaid>(
    DEFAULT_EMPLOYER_PAID
  );

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/config/product/${product_id}`)
      .then((res) => res.json())
      .then((res) => {
        setProduct(res);
        if (res.voluntary_census_strategy_id) {
          setSelection({
            allow_employer_paid: res.allow_employer_paid,
            voluntary_census_strategy_id: res.voluntary_census_strategy_id,
            employer_paid_census_strategy_id:
              res.employer_paid_census_strategy_id,
          });
        }
      });

    return () => {
      controller.abort();
    };
  }, [product_id]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch("/api/ref/census-strategies", { signal })
      .then((res) => res.json())
      .then((res) => {
        setStrategies(res);
      });

    return () => {
      controller.abort();
    };
  }, []);

  const setter = (
    key: keyof ConfigProduct_EmployerPaid,
    val: number | boolean
  ) => {
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
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot save to database");
        }
        return res.json();
      })
      .then((res) => {
        setProduct(res);
      })
      .finally(() => {
        setIsSaving(false);
      });
  };

  return (
    <>
      <PageTitle title={PAGE_DETAILS.title} subtitle={PAGE_DETAILS.subtitle}>
        <div className="space-x-6 flex">
          <Link to={`/app/config/product/${product_id}/rating/strategy`}>
            <span className="flex items-center text-sm font-semibold text-primary-700 hover:text-accent-600 transition duration-300">
              <ChevronLeftIcon className="h-5 w-5" />
              Prev
            </span>
          </Link>
        </div>
      </PageTitle>
      <div className="grid grid-cols-3 gap-x-6">
        <div className="col-span-2 flex flex-col space-y-6">
          <AppPanel className="px-0 py-0">
            <>
              <div className="mt-4 mb-8 px-4 space-y-6">
                <Switch.Group
                  as="div"
                  className="flex flex-col justify-center space-y-1"
                >
                  <Switch.Label as="span" className="">
                    <span className="text-sm font-medium text-gray-900">
                      Allow Employer Paid
                    </span>
                  </Switch.Label>
                  <Switch
                    checked={selection.allow_employer_paid}
                    onChange={() =>
                      setter(
                        "allow_employer_paid",
                        !selection.allow_employer_paid
                      )
                    }
                    className={classNames(
                      selection.allow_employer_paid
                        ? "bg-indigo-600"
                        : "bg-gray-200",
                      "relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                    )}
                  >
                    <span
                      aria-hidden="true"
                      className={classNames(
                        selection.allow_employer_paid
                          ? "translate-x-5"
                          : "translate-x-0",
                        "pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
                      )}
                    />
                  </Switch>
                </Switch.Group>
                <AppRadioSelect
                  radioMax={1}
                  group="voluntary"
                  label="Voluntary Census Strategy"
                  items={strategies}
                  itemId="ref_id"
                  itemLabel="ref_attr_label"
                  itemDescription={(item) => item.ref_attr_description}
                  defaultValue={selection.voluntary_census_strategy_id}
                  onClick={(item) =>
                    setter("voluntary_census_strategy_id", item.ref_id)
                  }
                />
                <AppRadioSelect
                  radioMax={1}
                  group="er_paid"
                  label="Employer Paid Census Strategy"
                  items={strategies}
                  itemId="ref_id"
                  itemLabel="ref_attr_label"
                  itemDescription={(item) => item.ref_attr_description}
                  defaultValue={selection.employer_paid_census_strategy_id}
                  onClick={(item) =>
                    setter("employer_paid_census_strategy_id", item.ref_id)
                  }
                />
              </div>
            </>
          </AppPanel>
        </div>
        <div className="flex flex-col items-end space-y-6">
          <Breadcrumb step="rating-strategies" />

          <AppButton
            disabled={!isValid || !isDirty}
            isLoading={isSaving}
            onClick={clickHandler}
          >
            Save
          </AppButton>
        </div>
      </div>
    </>
  );
};

const DEFAULT_EMPLOYER_PAID = {
  employer_paid_census_strategy_id: undefined,
  voluntary_census_strategy_id: undefined,
  allow_employer_paid: undefined,
} as ConfigProduct_EmployerPaid;

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

export default ConfigProductDetailCensus;
