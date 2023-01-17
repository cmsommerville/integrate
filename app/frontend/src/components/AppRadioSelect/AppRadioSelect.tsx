import { Fragment, useState, useMemo, useCallback, useEffect } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/react/20/solid";

interface Item {
  [key: string | number]: any;
}

interface Props
  extends Omit<React.ComponentProps<"input">, "onClick" | "checked"> {
  group: string;
  as?: "radio" | "select";
  items: Item[];
  label?: string;
  defaultValue?: string | number;
  onClick: (id: Item) => void;
  radioMax: number;
  itemId?: keyof Item;
  itemLabel?: keyof Item | ((item: Item) => string);
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
  as,
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

  useEffect(() => {
    if (!items || items.length === 0) return;
    if (!defaultValue) return;
    setSelection(defaultValue);
  }, [items, defaultValue]);

  const _items = useMemo(() => {
    return [
      {
        _id: -1,
        _label: "Select an option",
        hidden: true,
      },
      ...items,
    ];
  }, [items]);

  const idGetter = useCallback(
    (item: Item) => {
      if (item._id) return item._id;
      if (!itemId) return item.id;
      return item[itemId];
    },
    [itemId]
  );

  const labelGetter = useCallback(
    (item: Item) => {
      // if "Select an Option", return
      if (item._id) return item._label;
      // if itemLabel not provided, default to label
      if (!itemLabel) return item.label;
      // if itemLabel is a function, return the results of the function
      if (typeof itemLabel === "function") return itemLabel(item);
      // otherwise, return the itemLabel key

      return item[itemLabel];
    },
    [itemLabel]
  );

  const selectionItem = useMemo(() => {
    if (!selection) return {};
    return _items.find((item) => idGetter(item) === selection);
  }, [selection, idGetter, _items]);

  const _onClickRadio = useCallback(
    (item: Item) => {
      setSelection(idGetter(item));
      if (!onClick) return;
      onClick(item);
    },
    [onClick, idGetter]
  );

  const _onClickSelect = useCallback(
    (item_id: string | number) => {
      const item = items.find((i) => idGetter(i) === item_id);
      if (!item) return;
      setSelection(idGetter(item));
      if (!onClick) return;
      onClick(item);
    },
    [onClick, idGetter]
  );

  return (
    <fieldset name={group} className="w-full">
      {items.length > radioMax || as === "select" ? (
        <Listbox value={selection} onChange={_onClickSelect}>
          {({ open }) => (
            <>
              <Listbox.Label className="block text-sm font-medium text-gray-700">
                {props.label}
              </Listbox.Label>
              <div className="relative mt-1">
                <Listbox.Button className="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm">
                  <span className="block truncate">
                    {selectionItem ? labelGetter(selectionItem) : ""}
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
                        key={`${group}-${idGetter(item)}`}
                        className={({ active }) =>
                          classNames(
                            active
                              ? "text-white bg-indigo-600"
                              : "text-gray-900",
                            "relative cursor-default select-none py-2 pl-10 pr-4"
                          )
                        }
                        value={idGetter(item)}
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
                              {labelGetter(item)}
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
                                id={`${idGetter(item)}`}
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
      ) : (
        <div className="space-y-5">
          {items.map((item) => (
            <div key={idGetter(item)} className="relative flex items-start">
              <div className="flex h-5 items-center">
                <input
                  id={`${group}-${idGetter(item)}`}
                  key={defaultValue} // this makes sure that the defaultvalue gets rendered
                  name={group}
                  type="radio"
                  onClick={() => _onClickRadio(item)}
                  defaultChecked={idGetter(item) == defaultValue}
                  {...props}
                  className="h-4 w-4 border-gray-300 text-primary-600 focus:ring-primary-500 cursor-pointer"
                />
              </div>
              <div className="ml-3 text-sm">
                <label
                  htmlFor={`${group}-${idGetter(item)}`}
                  className="font-medium cursor-pointer"
                >
                  {labelGetter(item)}
                </label>
                {itemDescription ? (
                  <p id={`${idGetter(item)}`} className="text-gray-500">
                    {itemDescription(item)}
                  </p>
                ) : null}
              </div>
            </div>
          ))}
        </div>
      )}
    </fieldset>
  );
};

AppRadioSelect.defaultProps = defaultProps;

export default AppRadioSelect;
