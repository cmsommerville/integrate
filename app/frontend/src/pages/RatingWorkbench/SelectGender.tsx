import { useState, useEffect } from "react";
import { IAppSelectOption, AppSelect } from "@/components/Form";

export interface IProductMapper {
  config_product_mapper_set_id: number;
  mapper_type_label: string;
}

type SelectProps = JSX.IntrinsicElements["select"];

type IProps = {
  plan_id: number | string;
  onChange(payload: any): any;
} & SelectProps;

const SelectGender = ({ plan_id, ...props }: IProps) => {
  const [options, setOptions] = useState<IAppSelectOption[]>([]);
  const [selection, setSelection] = useState<IAppSelectOption | undefined>();

  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    fetch(`/api/crud/selection/plan/${plan_id}`, { signal })
      .then((res) => res.json())
      .then((res) => {
        setSelection({
          id: res.gender_mapper_set.config_product_mapper_set_id,
          label: res.gender_mapper_set.mapper_type_label,
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

    fetch(`/api/data/selection/plan/${plan_id}/gender-mapper-list`, {
      signal,
    })
      .then((res) => res.json())
      .then((res) => {
        setOptions(
          res.map((opt: IProductMapper) => {
            return {
              id: opt.config_product_mapper_set_id,
              label: opt.mapper_type_label,
            };
          })
        );
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

  const _onChange = (val: IAppSelectOption) => {
    setSelection(val);
    fetch(`/api/crud/selection/plan/${plan_id}`, {
      method: "PATCH",
      body: JSON.stringify({
        config_gender_product_mapper_set_id: val.id,
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

export default SelectGender;
