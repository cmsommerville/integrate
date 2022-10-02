import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import _ from "lodash";
import {
  SelectCensusSet,
  SelectSmokerStatus,
  SelectGender,
} from "@/pages/RatingWorkbench";
import { RateDisplayTemplateAgeBand } from "./RateDisplayTemplates";

const RatingWorkbench = () => {
  const { plan_id } = useParams();

  const [product, setProduct] = useState<any>({});
  const [rates, setRates] = useState<any>([]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/data/selection/plan/${plan_id}/product`, { signal })
      .then((res) => res.json())
      .then((res) => {
        setProduct(res);
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

    fetch(`/api/data/selection/plan/${plan_id}/rate-table`, { signal })
      .then((res) => res.json())
      .then((res) => {
        setRates(res);
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

  const onCensusSelection = useCallback(() => {
    fetch(`/api/crud/selection/rate-table/${plan_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((res) => {
        setRates(res);
      });
  }, [plan_id]);

  const onGenderSelection = useCallback(() => {
    fetch(`/api/crud/selection/rate-table/${plan_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((res) => {
        setRates(res);
      });
  }, [plan_id]);

  const onSmokerStatusSelection = useCallback(() => {
    fetch(`/api/crud/selection/rate-table/${plan_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((res) => {
        setRates(res);
      });
  }, [plan_id]);

  return (
    <>
      <div className="grid grid-cols-3 gap-8">
        {plan_id ? (
          <>
            <SelectCensusSet plan_id={plan_id} onChange={onCensusSelection}>
              Census
            </SelectCensusSet>

            {["rating"].includes(
              product?.smoker_status_rating_strategy?.ref_attr_code
            ) ? (
              <SelectSmokerStatus
                plan_id={plan_id}
                onChange={onSmokerStatusSelection}
              >
                Smoker Status
              </SelectSmokerStatus>
            ) : null}

            {["rating"].includes(
              product?.gender_rating_strategy?.ref_attr_code
            ) ? (
              <SelectGender plan_id={plan_id} onChange={onGenderSelection}>
                Gender
              </SelectGender>
            ) : null}
          </>
        ) : null}
      </div>
      <div className="">
        <div className="col-span-2">
          <RateDisplayTemplateAgeBand rates={rates} product={product} />
        </div>
      </div>
    </>
  );
};

export default RatingWorkbench;
