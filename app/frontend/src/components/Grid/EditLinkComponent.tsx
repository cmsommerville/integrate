import { useMemo } from "react";
import { Link } from "react-router-dom";

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const EditLinkComponent = (props: any) => {
  return (
    <Link to={props.url(props)}>
      <span
        className={classNames(
          "text-primary-600 font-semibold cursor-pointer",
          "hover:underline hover:text-primary-400"
        )}
      >
        Edit
      </span>
    </Link>
  );
};

export default EditLinkComponent;
