import { useState, useEffect, useMemo, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router";
import { Link } from "react-router-dom";
import moment from "moment";
import {
  BriefcaseIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  PuzzlePieceIcon,
} from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppSnackbar from "@/components/AppSnackbar";
import AppButton from "@/components/AppButton";
import ConfigProductDetailBasicInfo from "./ConfigProductDetailBasicInfo";
import ConfigProductDetailOptionalFields from "./ConfigProductDetailOptionalFields";
import { ConfigProduct } from "./types";
import { Breadcrumb, PageTitle } from "./Components";

const ConfigProductDetail = () => {
  const { product_id } = useParams();
  const navigate = useNavigate();
  const ref: any = useRef(null);
  const ref2 = useRef(null);

  const [isSaving, setIsSaving] = useState(false);
  const [isValid, setIsValid] = useState(true);
  const [isDirty, setIsDirty] = useState(false);

  const [selectedTab, setSelectedTab] = useState(0);
  const [product, setProduct] = useState<ConfigProduct>(DEFAULT_CONFIG_PRODUCT);

  const productSetter = useCallback(
    (key: keyof ConfigProduct, val: number | string | null | undefined) => {
      setProduct((old) => ({ ...old, [key]: val }));
      setIsDirty(true);
    },
    [setProduct]
  );

  const title = useCallback(
    (isNew: boolean) => {
      return isNew ? "Create New Product" : "Configure the Product";
    },
    [product_id]
  );

  const subtitle = useCallback(
    (isNew: boolean) => {
      return "Enter the basics, then add optional fields.";
    },
    [product_id]
  );

  const showSnackbar = () => {
    if (!ref || !ref.current) return;
    const { clickHandler } = ref.current;
    clickHandler();
  };

  const saveHandler = () => {
    setIsSaving(true);
    if (!isDirty) {
      setIsSaving(false);
      return;
    }

    const url = product_id
      ? `/api/config/product/${product_id}`
      : `/api/config/product`;

    fetch(url, {
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

  const nextUrl = useMemo(() => {
    if (!product.config_product_id) return "#";
    return `/app/config/product/${product.config_product_id}/rating/attrs`;
  }, [product]);

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
          setIsDirty(false);
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
      <AppSnackbar ref={ref} message={"This is a test"}></AppSnackbar>
      <PageTitle title={title(!product_id)} subtitle={subtitle(!product_id)}>
        <div className="space-x-6 flex">
          <Link to={nextUrl}>
            <span className="flex items-center text-sm font-semibold text-primary-700 hover:text-accent-600 transition duration-300">
              Next
              <ChevronRightIcon className="h-5 w-5" />
            </span>
          </Link>
        </div>
      </PageTitle>
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
        </div>
        <div className="col-span-2 flex flex-col items-end space-y-6">
          <Breadcrumb step="basic-info" />
          <AppButton
            disabled={!isValid || !isDirty}
            isLoading={isSaving}
            onClick={saveHandler}
          >
            Save
          </AppButton>
        </div>
      </div>
    </>
  );
};

const DEFAULT_CONFIG_PRODUCT = {
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
  product: ConfigProduct,
  setter: (
    key: keyof ConfigProduct,
    val: number | string | null | undefined
  ) => void
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
