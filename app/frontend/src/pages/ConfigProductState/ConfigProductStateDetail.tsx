import { useState, useEffect, useMemo, useCallback, useRef } from "react";
import { useParams } from "react-router";
import moment from "moment";

import { AppPanel } from "@/components/AppPanel";
import Map from "@/components/Map";
import AppButton from "@/components/AppButton";
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
  const refState = useRef(null);
  const { product_id } = useParams();

  const [selectedState, setSelectedState] = useState<ConfigProductStateType>(
    DEFAULT_CONFIG_PRODUCT_STATE
  );
  const [selectedStateBBox, setSelectedStateBBox] = useState("0 0 0 0");
  const [productStateList, setProductStateList] = useState<
    ConfigProductStateType[]
  >([]);
  const [isSaving, setIsSaving] = useState(false);

  const changeInputHandler = useCallback(
    (
      key: keyof ConfigProductStateType,
      val: number | string | null | undefined
    ) => {
      setSelectedState((old) => ({ ...old, [key]: val }));
    },
    [setSelectedState]
  );

  const selectStateHandler = useCallback(
    (states: StateSVG[]) => {
      if (states.length === 0) return;

      const selState = productStateList.find(
        (st) => st.state_id === states[0].state_id
      );
      if (selState) {
        setSelectedState(selState);
      } else {
        setSelectedState({
          config_product_id: Number(product_id),
          config_product_state_effective_date: moment().format("YYYY-MM-DD"),
          config_product_state_expiration_date: "9999-12-31",
          state_id: states[0].state_id,
          state: states[0],
        });
      }
    },
    [productStateList, refState]
  );

  const clickHandler = () => {
    setIsSaving(true);
    let payload;
    const { config_product_state_id, state, ...rest } = selectedState;
    payload = { ...rest };
    if (config_product_state_id && config_product_state_id > 0) {
      payload = { ...payload, config_product_state_id };
    }
    fetch(`/api/config/product/${product_id}/state`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((res) => {
        return res.json();
      })
      .then((res) => {
        setSelectedState(res);
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

    fetch(`/api/config/product/${product_id}/states`, { signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get data for product states");
        }
        return res.json();
      })
      .then((stateList) => {
        if (stateList.length > 0) {
          setProductStateList(stateList);
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

  useEffect(() => {
    const svgpath = refState.current as SVGGraphicsElement | null;
    if (svgpath) {
      const { x, y, width, height } = svgpath.getBBox();
      console.log(svgpath.getBBox());
      setSelectedStateBBox(`${x} ${y} ${width} ${height}`);
    }
  }, [refState, selectedState]);

  const Tooltip = (hoverState: StateSVG) => {
    return (
      <ConfigProductStateMapTooltip
        productStates={productStateList}
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
          <AppPanel className="">
            <div>
              <Map
                tooltip={Tooltip}
                onClickState={selectStateHandler}
                fill={{ selected: "fill-accent-600" }}
              />
            </div>
          </AppPanel>
        </div>
        <div className="col-span-2 flex flex-col space-y-4">
          <AppPanel className="">
            <form className="">
              <div className="flex justify-center border-b border-gray-200 pb-4 mb-6">
                <h3 className="tracking-wide font-light">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    xmlnsXlink="http://www.w3.org/1999/xlink"
                    version="1.1"
                    id="us-map"
                    preserveAspectRatio="xMinYMin meet"
                    x="0px"
                    y="0px"
                    width="100px"
                    height="100px"
                    viewBox={selectedStateBBox}
                    xmlSpace="preserve"
                  >
                    <g ref={refState}>
                      <path
                        className={classNames(
                          "transition duration-300 ease",
                          "fill-gray-200"
                        )}
                        id="selected-state"
                        d={selectedState.state.svg_path}
                      />
                    </g>
                  </svg>
                  {selectedState.state.state_name
                    ? selectedState.state.state_name
                    : "Select a state"}
                </h3>
              </div>
              <div className="flex flex-col space-y-8">
                <div>
                  <label
                    htmlFor="config_product_effective_date"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Effective Date
                  </label>
                  <div className="mt-1">
                    <input
                      type="date"
                      name="config_product_effective_date"
                      id="config_product_effective_date"
                      className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      onChange={(e) =>
                        changeInputHandler(
                          "config_product_state_effective_date",
                          e.target.value
                        )
                      }
                      value={
                        selectedState.config_product_state_effective_date ?? ""
                      }
                    />
                  </div>
                </div>
                <div>
                  <label
                    htmlFor="config_product_expiration_date"
                    className="block text-sm font-medium text-gray-700"
                  >
                    Expiration Date
                  </label>
                  <div className="mt-1">
                    <input
                      type="date"
                      name="config_product_expiration_date"
                      id="config_product_expiration_date"
                      className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                      onChange={(e) =>
                        changeInputHandler(
                          "config_product_state_expiration_date",
                          e.target.value
                        )
                      }
                      value={
                        selectedState.config_product_state_expiration_date ?? ""
                      }
                    />
                  </div>
                </div>
              </div>
            </form>
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

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const DEFAULT_STATE_SVG = {
  state_id: 0,
  state_name: "",
  state_code: "",
  svg_path: "",
};

const DEFAULT_CONFIG_PRODUCT_STATE = {
  config_product_state_id: 0,
  config_product_id: 0,
  state_id: 0,
  config_product_state_effective_date: moment().format("YYYY-MM-DD"),
  config_product_state_expiration_date: "9999-12-31",
  state: DEFAULT_STATE_SVG,
};

export default ConfigProductState;
