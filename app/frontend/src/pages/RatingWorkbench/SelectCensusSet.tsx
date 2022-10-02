import { useState, useEffect } from "react";
import { IAppSelectOption, AppSelect } from "@/components/Form";

export interface ICensusSet {
  selection_census_set_id: number;
  selection_census_description: string;
  selection_plan_id: number;
  selection_census_filepath?: string | null | undefined;
}

type SelectProps = JSX.IntrinsicElements["select"];

type IProps = {
  plan_id: number | string;
  onChange(payload: any): any;
} & SelectProps;

const SelectCensusSet = ({ plan_id, ...props }: IProps) => {
  const [options, setOptions] = useState<IAppSelectOption[]>([]);
  const [selection, setSelection] = useState<IAppSelectOption | undefined>();

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/crud/selection/plan/${plan_id}`, { signal })
      .then((res) => res.json())
      .then((res) => {
        setSelection({
          id: res.census_set.selection_census_set_id,
          label: res.census_set.selection_census_description,
        });
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, [plan_id]);

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/dd/selection/census-set/${plan_id}`, { signal })
      .then((res) => res.json())
      .then((res) =>
        setOptions(
          res.map((item: ICensusSet) => {
            return {
              id: item.selection_census_set_id,
              label: item.selection_census_description,
            };
          })
        )
      )
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, [plan_id]);

  const _onChange = (val: IAppSelectOption) => {
    setSelection(val);
    fetch(`/api/crud/selection/plan/${plan_id}`, {
      method: "PATCH",
      body: JSON.stringify({
        selection_census_set_id: val.id,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    }).then((res) => {
      props.onChange(res);
    });
  };

  return (
    <AppSelect
      options={options}
      selected={selection ?? options[0]}
      onChange={_onChange}
    >
      {props.children}
    </AppSelect>
  );
};

export default SelectCensusSet;
