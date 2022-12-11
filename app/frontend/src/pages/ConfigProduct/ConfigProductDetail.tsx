import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import moment from "moment";
import { BriefcaseIcon, PuzzlePieceIcon } from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";
import ConfigProductDetailBasicInfo from "./ConfigProductDetailBasicInfo";
import ConfigProductDetailOptionalFields from "./ConfigProductDetailOptionalFields";
import { Product } from "./types";

const ConfigProductDetail = () => {
  const { product_id } = useParams();

  const [selectedTab, setSelectedTab] = useState(0);
  const [product, setProduct] = useState<Product>(DEFAULT_CONFIG_PRODUCT);
  const [isSaving, setIsSaving] = useState(false);

  const productSetter = useCallback(
    (key: keyof Product, val: number | string | null | undefined) => {
      setProduct((old) => ({ ...old, [key]: val }));
    },
    [setProduct]
  );

  const clickHandler = () => {
    setIsSaving(true);
    fetch(`/api/config/product/${product_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(product),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Could not save data to database");
        }
        return res.json();
      })
      .then((res) => {
        setProduct(res);
      })
      .catch((err) => {
        console.log(err);
      })
      .finally(() => {
        setIsSaving(false);
      });
  };

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;
    if (!product_id) return;

    fetch(`/api/config/product/${product_id}`, { signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get data for product");
        }
        return res.json();
      })
      .then((res) => {
        if (res.config_product_id) {
          setProduct(res);
        }
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
      <div className="flex justify-between pb-6">
        <div className="">
          <h2 className="text-2xl font-light tracking-wide text-gray-700">
            Configure the Product
          </h2>
          <p className="text-sm text-gray-400">
            Enter the basics, then add optional fields.
          </p>
        </div>
      </div>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-4 flex flex-col space-y-4">
          <AppPanel className="pb-16 pt-2 h-fit">
            <>
              <div className="hidden sm:block mb-4">
                <div className="border-b border-gray-200">
                  <nav aria-label="Tabs">
                    <ul className="-mb-px flex space-x-8">
                      {tabs.map((tab, ix) => (
                        <li
                          key={tab.label}
                          className={classNames(
                            ix === selectedTab
                              ? "border-indigo-500 text-indigo-600"
                              : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300",
                            "group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm cursor-pointer"
                          )}
                          aria-current={ix === selectedTab ? "page" : undefined}
                          onClick={() => setSelectedTab(ix)}
                        >
                          <tab.icon
                            className={classNames(
                              ix === selectedTab
                                ? "text-indigo-500"
                                : "text-gray-400 group-hover:text-gray-500",
                              "-ml-0.5 mr-2 h-5 w-5"
                            )}
                            aria-hidden="true"
                          />
                          <span>{tab.label}</span>
                        </li>
                      ))}
                    </ul>
                  </nav>
                </div>
              </div>
              {tabComponentPicker(selectedTab, product, productSetter)}
            </>
          </AppPanel>

          <div className="flex justify-end items-end">
            <AppButton isLoading={isSaving} onClick={clickHandler}>
              Save
            </AppButton>
          </div>
        </div>
      </div>
    </>
  );
};

const DEFAULT_CONFIG_PRODUCT = {
  config_product_id: 0,
  config_product_code: "",
  config_product_label: "",
  config_product_effective_date: moment().format("YYYY-MM-DD"),
  config_product_expiration_date: "9999-12-31",
};

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const tabs = [
  { code: "basic", label: "Basic Info", icon: BriefcaseIcon },
  { code: "optional", label: "Optional Data", icon: PuzzlePieceIcon },
];

const tabComponentPicker = (
  selectedTab: number,
  product: Product,
  setter: (key: keyof Product, val: number | string | null | undefined) => void
) => {
  switch (tabs[selectedTab].code) {
    case "basic":
      return (
        <ConfigProductDetailBasicInfo product={product} onChange={setter} />
      );
    case "optional":
      return (
        <ConfigProductDetailOptionalFields
          product={product}
          onChange={setter}
        />
      );
    default:
      return (
        <ConfigProductDetailBasicInfo product={product} onChange={setter} />
      );
  }
};

export default ConfigProductDetail;
