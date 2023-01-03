import React, { useState, useImperativeHandle } from "react";
import { XMarkIcon } from "@heroicons/react/20/solid";

interface Props extends React.ComponentProps<"div"> {
  timeout?: number;
  message?: string;
  children?: JSX.Element;
}

const DEFAULT_PROPS = {
  timeout: 5000,
};

const AppSnackbar = React.forwardRef((props: Props, ref) => {
  const [showSnackbar, setShowSnackbar] = useState(false);

  useImperativeHandle(ref, () => ({
    clickHandler: () => {
      setShowSnackbar(true);
      if (props.timeout && props.timeout > 0)
        setTimeout(() => {
          setShowSnackbar(false);
        }, props.timeout);
    },
  }));

  if (!showSnackbar) return <></>;

  return (
    <div className="absolute bottom-0 right-1/2 translate-x-1/2 py-4 px-6 bg-warning-600 text-white rounded-t-lg min-w-fit w-72 flex justify-center items-center">
      <XMarkIcon
        className="absolute top-1 right-1 w-4 h-4 cursor-pointer transition ease duration-300 hover:text-warning-900"
        onClick={() => setShowSnackbar(false)}
      />
      {props.message ? props.message : null}
    </div>
  );
});

AppSnackbar.defaultProps = DEFAULT_PROPS;

export default AppSnackbar;
