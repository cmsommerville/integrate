import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import {
  ConfigProduct_Basic,
  ConfigProduct_RatingStrategies,
} from "@/types/config";
import { RefRatingStrategy } from "../ConfigProduct/types";
import { CalendarIcon, HeartIcon, MoonIcon } from "@heroicons/react/24/outline";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";
import AppRadioSelect from "@/components/AppRadioSelect";
import { Breadcrumb, PageTitle } from "./Components";

const PAGE_DETAILS = {
  id: "attr-sets",
  title: "Attributes",
  subtitle:
    "Specify the attributes used for smoker disposition, gender, and relationships...",
};

const ConfigProductDetailRatingGender = () => {
  const { product_id } = useParams();

  const [isDirty, setIsDirty] = useState(false);
  const [isValid, setIsValid] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  const [product, setProduct] = useState<
    ConfigProduct_Basic & ConfigProduct_RatingStrategies
  >();
  const [strategies, setStrategies] = useState<RefRatingStrategy[]>([]);

  const [selection, setSelection] = useState<ConfigProduct_RatingStrategies>(
    DEFAULT_RATING_STRATEGY
  );

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/config/product/${product_id}`)
      .then((res) => res.json())
      .then((res) => {
        setProduct(res);
        if (res.gender_rating_strategy_id) {
          setSelection({
            gender_rating_strategy_id: res.gender_rating_strategy_id,
            smoker_status_rating_strategy_id:
              res.smoker_status_rating_strategy_id,
            age_rating_strategy_id: res.age_rating_strategy_id,
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

    fetch("/api/ref/rating-strategies", { signal })
      .then((res) => res.json())
      .then((res) => {
        setStrategies(res);
      });

    return () => {
      controller.abort();
    };
  }, []);

  const setter = (key: keyof ConfigProduct_RatingStrategies, val: number) => {
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
              <div className="px-4 pb-4">
                <AppRadioSelect
                  group="gender"
                  items={strategies}
                  itemId="ref_id"
                  itemLabel="ref_attr_label"
                  itemDescription={(item) => {
                    return item.ref_attr_description;
                  }}
                  defaultValue={product?.gender_rating_strategy_id}
                  onClick={(item) =>
                    setter("gender_rating_strategy_id", item.ref_id)
                  }
                />
              </div>
            </>
          </AppPanel>

          <AppPanel className="pt-0 pl-0 pr-0 h-fit space-y-6">
            <>
              <h3 className="font-normal text-white py-4 px-4 bg-primary-700 rounded-t-lg flex space-x-2">
                <MoonIcon className="h-6 w-6" aria-hidden="true" />
                <span>Smoker Dispositions</span>
              </h3>
              <div className="px-4 pb-4">
                <AppRadioSelect
                  group="smoker_status"
                  items={strategies}
                  itemId="ref_id"
                  itemLabel="ref_attr_label"
                  itemDescription={(item) => {
                    return item.ref_attr_description;
                  }}
                  defaultValue={product?.smoker_status_rating_strategy_id}
                  onClick={(item) =>
                    setter("smoker_status_rating_strategy_id", item.ref_id)
                  }
                />
              </div>
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

              <div className="px-4 pb-4">
                <AppRadioSelect
                  group="age"
                  items={strategies}
                  itemId="ref_id"
                  itemLabel="ref_attr_label"
                  itemDescription={(item) => {
                    return item.ref_attr_description;
                  }}
                  defaultValue={product?.age_rating_strategy_id}
                  onClick={(item) =>
                    setter("age_rating_strategy_id", item.ref_id)
                  }
                />
              </div>
            </>
          </AppPanel>
        </div>
        <div className="col-span-2 flex flex-col items-end">
          <Breadcrumb step="rating-strategies" />
        </div>
      </div>
    </>
  );
};

const DEFAULT_RATING_STRATEGY = {
  gender_rating_strategy_id: undefined,
  smoker_status_rating_strategy_id: undefined,
  age_rating_strategy_id: undefined,
};

export default ConfigProductDetailRatingGender;
