import React from "react";

interface Props extends React.ComponentProps<"div"> {
  children: React.ReactElement;
}

function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const AppPanel = ({ className, children }: Props) => {
  return (
    <div
      className={classNames(
        "px-4 py-6 bg-white rounded-lg border border-gray-200 shadow-md",
        className
      )}
    >
      {children}
    </div>
  );
};

export default AppPanel;
