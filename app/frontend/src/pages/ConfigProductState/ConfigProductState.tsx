import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import moment from "moment";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";
import Map from "@/components/Map";
import { ConfigProductStateType } from "./types";
import { StateSVG } from "@/components/Map";

type TooltipProps = {
  productStates: ConfigProductStateType[];
  hoverState: StateSVG;
};

const ConfigProductStateMapTooltip = ({
  productStates,
  hoverState,
}: TooltipProps) => {
  const productState = productStates.find((ps) => {
    return ps.state.state_id === hoverState.state_id;
  });

  return (
    <>
      <h3 className="text-sm mb-1 pa-2">{hoverState.state_name}:</h3>
      {productState &&
      productState.config_product_state_effective_date &&
      productState.config_product_state_expiration_date ? (
        <p className="text-xs">
          {moment(productState.config_product_state_effective_date).format(
            "MM/DD/YYYY"
          )}
          <span> - </span>
          {moment(productState.config_product_state_expiration_date).format(
            "MM/DD/YYYY"
          )}
        </p>
      ) : (
        <p className="text-xs">Not configured yet!</p>
      )}
    </>
  );
};

const ConfigProductState = () => {
  const { product_id } = useParams();

  const [productStates, setProductStates] = useState<ConfigProductStateType[]>(
    []
  );
  const [isSaving, setIsSaving] = useState(false);

  const disabledStates = useMemo(() => {
    return productStates.map((st) => st.state);
  }, [productStates]);

  const clickHandler = () => {
    setIsSaving(true);
    fetch(`/api/config/product/${product_id}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(""),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Could not save data to database");
        }
        return res.json();
      })
      .then((res) => {})
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

    fetch(`/api/config/product/${product_id}/states`, { signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get data for product");
        }
        return res.json();
      })
      .then((res) => {
        if (res.length > 0) {
          setProductStates(res);
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

  const Tooltip = (hoverState: StateSVG) => {
    return (
      <ConfigProductStateMapTooltip
        productStates={productStates}
        hoverState={hoverState}
      />
    );
  };

  return (
    <>
      <div className="flex justify-between pb-6">
        <div className="">
          <h2 className="text-2xl font-light tracking-wide text-gray-700">
            Configure Product States
          </h2>
          <p className="text-sm text-gray-400">
            Enable or disallow the product to be quoted by state
          </p>
        </div>
      </div>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-4 flex flex-col space-y-4">
          <AppPanel className="pb-16 pt-2 h-fit">
            <>
              <Map tooltip={Tooltip} disabled={disabledStates} />
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

export default ConfigProductState;
