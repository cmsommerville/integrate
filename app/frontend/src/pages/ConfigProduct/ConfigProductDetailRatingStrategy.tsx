import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import { Link } from "react-router-dom";
import {
  ConfigProduct_Basic,
  ConfigProduct_RatingStrategies,
} from "@/types/config";
import { RefRatingStrategy } from "../ConfigProduct/types";
import { CalendarIcon, HeartIcon, MoonIcon } from "@heroicons/react/24/outline";
import { ChevronRightIcon, ChevronLeftIcon } from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";
import AppRadioSelect from "@/components/AppRadioSelect";
import { Breadcrumb, PageTitle } from "./Components";

const PAGE_DETAILS = {
  id: "rating-strategies",
  title: "Rating Strategy",
  subtitle:
    "Specify whether smoker disposition, gender, and age are rated, underwritten, or neither...",
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
        <div className="space-x-6 flex">
          <Link to={`/app/config/product/${product_id}/rating/dists`}>
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
                <AppRadioSelect
                  radioMax={1}
                  group="gender"
                  label="Gender"
                  items={strategies}
                  itemId="ref_id"
                  itemLabel="ref_attr_label"
                  itemDescription={(item) => item.ref_attr_description}
                  defaultValue={product?.gender_rating_strategy_id}
                  onClick={(item) =>
                    setter("gender_rating_strategy_id", item.ref_id)
                  }
                />
                <AppRadioSelect
                  radioMax={1}
                  group="smoker_status"
                  label="Smoker Disposition"
                  items={strategies}
                  itemId="ref_id"
                  itemLabel="ref_attr_label"
                  itemDescription={(item) => item.ref_attr_description}
                  defaultValue={product?.smoker_status_rating_strategy_id}
                  onClick={(item) =>
                    setter("smoker_status_rating_strategy_id", item.ref_id)
                  }
                />
                <AppRadioSelect
                  radioMax={1}
                  group="age"
                  label="Age"
                  items={strategies}
                  itemId="ref_id"
                  itemLabel="ref_attr_label"
                  itemDescription={(item) => item.ref_attr_description}
                  defaultValue={product?.age_rating_strategy_id}
                  onClick={(item) =>
                    setter("age_rating_strategy_id", item.ref_id)
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

const DEFAULT_RATING_STRATEGY = {
  gender_rating_strategy_id: undefined,
  smoker_status_rating_strategy_id: undefined,
  age_rating_strategy_id: undefined,
};

export default ConfigProductDetailRatingGender;
