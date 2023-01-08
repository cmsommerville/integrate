import { Fragment, useState, useMemo, useCallback, useEffect } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/react/20/solid";

interface Item {
  [key: string | number]: any;
}

interface Props
  extends Omit<React.ComponentProps<"input">, "onClick" | "checked"> {
  group: string;
  items: Item[];
  label?: string;
  defaultValue?: string | number;
  onClick: (id: Item) => void;
  radioMax: number;
  itemId?: keyof Item;
  itemLabel?: keyof Item;
  itemDescription?: (item: Item) => string;
}

const defaultProps: Props = {
  group: "",
  items: [],
  onClick: (id) => {},
  radioMax: 3,
};

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const AppRadioSelect = ({
  group,
  items,
  defaultValue,
  radioMax,
  itemId,
  itemLabel,
  itemDescription,
  onClick,
  ...props
}: Props) => {
  const [selection, setSelection] = useState<string | number | undefined>(-1);

  const { _id, _label } = useMemo(() => {
    let _id, _label;
    if (itemId) {
      _id = itemId;
    } else {
      _id = "id";
    }
    if (itemLabel) {
      _label = itemLabel;
    } else {
      _label = "label";
    }
    return { _id, _label };
  }, [itemId, itemLabel]);

  const _onClickRadio = useCallback(
    (item: Item) => {
      setSelection(item[_id]);
      if (!onClick) return;
      onClick(item);
    },
    [onClick, _id]
  );

  const _onClickSelect = useCallback(
    (item_id: string | number) => {
      const item = items.find((i) => i[_id] === item_id);
      if (!item) return;
      setSelection(item[_id]);
      if (!onClick) return;
      onClick(item);
    },
    [onClick, _id]
  );

  useEffect(() => {
    if (!items || items.length === 0) return;
    setSelection(defaultValue);
  }, [items, defaultValue]);

  const _items = useMemo(() => {
    return [
      {
        [_id]: -1,
        [_label]: "Select an option",
        hidden: true,
      },
      ...items,
    ];
  }, [items, _id, _label]);

  const selectionItem = useMemo(() => {
    if (!selection) return {};
    return _items.find((item) => item[_id] === selection);
  }, [selection, _id, _items]);

  return (
    <fieldset name={group}>
      {items.length <= radioMax ? (
        <div className="space-y-5">
          {items.map((item) => (
            <div key={item[_id]} className="relative flex items-start">
              <div className="flex h-5 items-center">
                <input
                  id={`${group}-${item[_id]}`}
                  key={defaultValue} // this makes sure that the defaultvalue gets rendered
                  name={group}
                  type="radio"
                  onClick={() => _onClickRadio(item)}
                  defaultChecked={item[_id] == defaultValue}
                  {...props}
                  className="h-4 w-4 border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                />
              </div>
              <div className="ml-3 text-sm">
                <label
                  htmlFor={`${group}-${item[_id]}`}
                  className="font-medium cursor-pointer"
                >
                  {item[_label]}
                </label>
                {itemDescription ? (
                  <p id={`${item[_id]}`} className="text-gray-500">
                    {itemDescription(item)}
                  </p>
                ) : null}
              </div>
            </div>
          ))}
        </div>
      ) : (
        <Listbox value={selection} onChange={_onClickSelect}>
          {({ open }) => (
            <>
              <Listbox.Label className="block text-sm font-medium text-gray-700">
                {props.label}
              </Listbox.Label>
              <div className="relative mt-1">
                <Listbox.Button className="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm">
                  <span className="block truncate">
                    {selectionItem ? selectionItem[_label] : ""}
                  </span>
                  <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
                    <ChevronUpDownIcon
                      className="h-5 w-5 text-gray-400"
                      aria-hidden="true"
                    />
                  </span>
                </Listbox.Button>

                <Transition
                  show={open}
                  as={Fragment}
                  leave="transition ease-in duration-100"
                  leaveFrom="opacity-100"
                  leaveTo="opacity-0"
                >
                  <Listbox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
                    {_items.map((item) => (
                      <Listbox.Option
                        key={`${group}-${item[_id]}`}
                        className={({ active }) =>
                          classNames(
                            active
                              ? "text-white bg-indigo-600"
                              : "text-gray-900",
                            "relative cursor-default select-none py-2 pl-10 pr-4"
                          )
                        }
                        value={item[_id]}
                        hidden={item.hidden ?? false}
                      >
                        {({ selected, active }) => (
                          <>
                            <span
                              className={classNames(
                                selected ? "font-semibold" : "font-normal",
                                "block truncate"
                              )}
                            >
                              {item[_label]}
                            </span>

                            {selected ? (
                              <span
                                className={classNames(
                                  active ? "text-white" : "text-indigo-600",
                                  "absolute inset-y-0 left-0 flex items-center pl-1.5"
                                )}
                              >
                                <CheckIcon
                                  className="h-5 w-5"
                                  aria-hidden="true"
                                />
                              </span>
                            ) : null}
                            {itemDescription ? (
                              <p
                                id={`${item[_id]}`}
                                className={classNames(
                                  active ? "text-primary-200" : "text-gray-500",
                                  ""
                                )}
                              >
                                {itemDescription(item)}
                              </p>
                            ) : null}
                          </>
                        )}
                      </Listbox.Option>
                    ))}
                  </Listbox.Options>
                </Transition>
              </div>
            </>
          )}
        </Listbox>
      )}
    </fieldset>
  );
};

AppRadioSelect.defaultProps = defaultProps;

export default AppRadioSelect;
