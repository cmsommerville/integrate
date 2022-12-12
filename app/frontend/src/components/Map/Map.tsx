import { useState, useEffect, useMemo, useCallback, useRef } from "react";

import { StateSVG } from "./types";

interface FillInterface {
  default?: string;
  disabled?: string;
  selected?: string;
}

interface Coordinates {
  top?: string;
  right?: string;
  bottom?: string;
  left?: string;
}

interface Props extends React.ComponentPropsWithRef<"div"> {
  disabled?: StateSVG[];
  fill?: FillInterface;
  tooltip?: (hoverState: StateSVG) => JSX.Element;
}

const Map = ({ disabled, fill, ...props }: Props) => {
  const ref = useRef<HTMLDivElement>(null);
  const [states, setStates] = useState<StateSVG[]>([]);
  const [hoverState, setHoverState] = useState<StateSVG | undefined>();
  const [coords, setCoords] = useState<Coordinates>({
    top: "0px",
    left: "0px",
  });
  const [localSelected, setLocalSelected] = useState<StateSVG[]>([]);

  const fillHandler = useCallback(
    (state: StateSVG) => {
      // check if state is disabled
      if (disabled) {
        const isDisabled = disabled.findIndex(
          (st) => st.state_id === state.state_id
        );
        if (isDisabled > -1) return "fill-primary-900 cursor-not-allowed";
      }

      // check if state is selected
      const isSelected = localSelected.findIndex(
        (st) => st.state_id === state.state_id
      );
      if (isSelected > -1)
        return "fill-primary-300 hover:fill-primary-500 cursor-pointer";

      // return fallback
      return "fill-gray-300 hover:fill-primary-500 cursor-pointer";
    },
    [localSelected, disabled]
  );

  const setTooltipCoordinates = useCallback(
    (ev: React.MouseEvent<SVGPathElement, MouseEvent>) => {
      let c: Coordinates = {};

      // get the reference to the containing div
      if (!ref.current) return;
      const div = ref.current.parentElement;
      if (!div) return;

      // switch the tooltip from the right to left if approaching right edge of div
      if (ev.nativeEvent.offsetX > div.offsetWidth - 250) {
        c.right = `${div.offsetWidth - ev.nativeEvent.offsetX - 30}px`;
      } else {
        c.left = `${ev.nativeEvent.offsetX + 20}px`;
      }

      // switch the tooltip from the bottom to top if approaching bottom edge
      if (ev.nativeEvent.offsetY > div.offsetHeight - 50) {
        c.bottom = `${div.offsetHeight - ev.nativeEvent.offsetY}px`;
      } else {
        c.top = `${ev.nativeEvent.offsetY}px`;
      }
      setCoords(c);
    },
    []
  );

  const onMouseOverState = useCallback(
    (state: StateSVG) => {
      setHoverState(state);
    },
    [setHoverState]
  );

  const onMouseLeaveState = useCallback(() => {
    setHoverState(undefined);
  }, [setHoverState]);

  const onClickState = useCallback(
    (state: StateSVG) => {
      const isSelected = localSelected.findIndex(
        (st) => st.state_id === state.state_id
      );

      if (isSelected === -1) {
        setLocalSelected((prev) => [...prev, state]);
      } else {
        setLocalSelected((prev) =>
          prev.filter((st) => st.state_id !== state.state_id)
        );
      }
    },
    [localSelected]
  );

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/ref/state-list`, { signal })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot get states");
        }
        return res.json();
      })
      .then((res) => {
        if (res.length) {
          setStates(res);
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

  const _states = useMemo(() => {
    return states.filter((state) => state.state_code !== "DC");
  }, [states]);

  const _dc = useMemo(() => {
    return states
      .filter((state) => state.state_code === "DC")
      .map((st) => {
        return {
          stroke: "#FFFFFF",
          strokeWidth: "1.5",
          cx: "975.3",
          cy: "351.8",
          r: "7",
          ...st,
        };
      });
  }, [states]);

  return (
    <>
      <div ref={ref} className="relative">
        <>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            xmlnsXlink="http://www.w3.org/1999/xlink"
            version="1.1"
            id="us-map"
            preserveAspectRatio="xMinYMin meet"
            x="0px"
            y="0px"
            viewBox="110 100 1000 600"
            enableBackground="new 0 0 959 593"
            xmlSpace="preserve"
          >
            <defs>
              <pattern
                id="disabled"
                width="8"
                height="10"
                patternUnits="userSpaceOnUse"
                patternTransform="rotate(45 50 50)"
              >
                <line stroke="#d1d5db" strokeWidth="7px" y2="10" />
              </pattern>
            </defs>
            <g id="g5">
              {_states.map((state) => {
                return (
                  <path
                    className={fillHandler(state)}
                    key={state.state_code}
                    id={state.state_code}
                    d={state.svg_path}
                    onClick={() => onClickState(state)}
                    onMouseLeave={onMouseLeaveState}
                    onMouseOver={() => onMouseOverState(state)}
                    onMouseMove={setTooltipCoordinates}
                  />
                );
              })}
              {_dc.map((dist) => {
                return (
                  <g id="gDC" key={dist.state_code}>
                    <path
                      id="pathDC"
                      className="fill-gray-300"
                      d={dist.svg_path}
                    />
                    <circle
                      id="circleDC"
                      className={fillHandler(dist)}
                      stroke={dist.stroke}
                      strokeWidth={dist.strokeWidth}
                      cx={dist.cx}
                      cy={dist.cy}
                      r={dist.r}
                      onClick={() => onClickState(dist)}
                      onMouseLeave={onMouseLeaveState}
                      onMouseOver={() => onMouseOverState(dist)}
                    />
                  </g>
                );
              })}
            </g>
            <path
              id="path67"
              fill="none"
              stroke="#A9A9A9"
              strokeWidth="2"
              d="M385,593v55l36,45 M174,525h144l67,68h86l53,54v46"
            />
          </svg>
          {hoverState ? (
            <div
              className="absolute p-3 rounded-md bg-gray-700 text-white"
              style={coords}
            >
              {!!props.tooltip ? props.tooltip(hoverState) : null}
            </div>
          ) : null}
        </>
      </div>
    </>
  );
};

export default Map;
