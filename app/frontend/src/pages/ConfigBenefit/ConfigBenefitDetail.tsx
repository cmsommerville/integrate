import { useState, useEffect, useMemo, useCallback, useRef } from "react";
import { useParams, useNavigate } from "react-router";
import { BriefcaseIcon, PuzzlePieceIcon } from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppSnackbar from "@/components/AppSnackbar";
import AppButton from "@/components/AppButton";
import ConfigBenefitDetailBasicInfo from "./ConfigBenefitDetailBasicInfo";
import ConfigProductDetailAddlInfo from "./ConfigBenefitDetailAddlInfo";
import { PageTitle } from "../ConfigProduct/Components";
import { ConfigBenefit } from "./types";

const validator = (key: keyof ConfigBenefit, val: any) => {
  switch (key) {
    case "config_benefit_version_code":
      if (!val) return false;
      return true;
    case "config_coverage_id":
      if (!val) return false;
      if (val === -1) return false;
      return true;
    case "config_rate_group_id":
      if (!val) return false;
      if (val === -1) return false;
      return true;
    case "ref_benefit_id":
      if (!val) return false;
      if (val === -1) return false;
      return true;
    case "unit_type_id":
      if (!val) return false;
      if (val === -1) return false;
      return true;
    default:
      return true;
  }
};

const ConfigBenefitDetail = () => {
  const { product_id, benefit_id } = useParams();
  const navigate = useNavigate();
  const ref: any = useRef(null);

  const [isSaving, setIsSaving] = useState(false);
  const [isDirty, setIsDirty] = useState(false);

  const [selectedTab, setSelectedTab] = useState(0);
  const [benefit, setBenefit] = useState<ConfigBenefit>(
    DEFAULT_CONFIG_BENEFIT(Number(product_id))
  );

  const benefitSetter = useCallback(
    (key: keyof ConfigBenefit, val: any) => {
      setBenefit((old) => ({ ...old, [key]: val }));
      setIsDirty(true);
    },
    [setBenefit]
  );

  const showSnackbar = () => {
    if (!ref || !ref.current) return;
    const { clickHandler } = ref.current;
    clickHandler();
  };

  const isValid = useMemo(() => {
    return Object.entries(benefit).reduce((isValid, [k, v]) => {
      return isValid && validator(k as keyof ConfigBenefit, v);
    }, true);
  }, [benefit]);

  const saveHandler = () => {
    setIsSaving(true);
    if (!isDirty) {
      setIsSaving(false);
      return;
    }

    const url = benefit_id
      ? `/api/config/product/${product_id}/benefit/${benefit_id}`
      : `/api/config/product/${product_id}/benefit`;

    let bnft = { ...benefit, config_product_id: Number(product_id) };
    if (benefit_id) {
      bnft = { ...bnft, config_benefit_id: Number(benefit_id) };
    }

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(bnft),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Could not save data to database");
        }
        return res.json();
      })
      .then((res) => {
        setBenefit(res);
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
        if (res.config_benefit_id) {
          setBenefit(res);
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
      <PageTitle title="Benefit" subtitle="Configure this benefit">
        <div className="flex items-end">
          <AppButton
            disabled={!isValid || !isDirty}
            isLoading={isSaving}
            onClick={saveHandler}
          >
            Save
          </AppButton>
        </div>
      </PageTitle>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-3 flex flex-col space-y-4">
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
              {product_id
                ? tabComponentPicker(
                    selectedTab,
                    product_id,
                    benefit,
                    benefitSetter
                  )
                : null}
            </>
          </AppPanel>
        </div>
      </div>
    </>
  );
};

const DEFAULT_CONFIG_BENEFIT = (product_id: number) =>
  ({
    config_product_id: product_id,
    config_benefit_description: "",
    config_benefit_version_code: "",
    ref_benefit_id: -1,
    ref_benefit: {
      ref_id: -1,
      ref_attr_code: "",
      ref_attr_label: "",
      ref_entity_code: "",
    },
    unit_type: {
      ref_id: -1,
      ref_attr_code: "",
      ref_attr_label: "",
      ref_entity_code: "",
    },
    unit_type_id: -1,
  } as ConfigBenefit);

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const tabs = [
  { code: "basic", label: "Basic Info", icon: BriefcaseIcon },
  { code: "addl", label: "Additional Data", icon: PuzzlePieceIcon },
];

const tabComponentPicker = (
  selectedTab: number,
  product_id: number | string,
  benefit: ConfigBenefit,
  setter: (
    key: keyof ConfigBenefit,
    val: number | string | null | undefined
  ) => void
) => {
  switch (tabs[selectedTab].code) {
    case "basic":
      return (
        <ConfigBenefitDetailBasicInfo
          product_id={product_id}
          benefit={benefit}
          onChange={setter}
        />
      );
    case "addl":
      return (
        <ConfigProductDetailAddlInfo
          product_id={product_id}
          benefit={benefit}
          onChange={setter}
        />
      );
    default:
      return (
        <ConfigBenefitDetailBasicInfo
          product_id={product_id}
          benefit={benefit}
          onChange={setter}
        />
      );
  }
};

export default ConfigBenefitDetail;
