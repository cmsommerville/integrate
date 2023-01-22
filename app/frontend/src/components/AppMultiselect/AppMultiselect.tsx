import { Fragment, useState, useEffect, useMemo, useCallback } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/react/20/solid";

interface Item {
  [key: string | number]: any;
}

interface Props extends Omit<React.ComponentProps<"select">, "onChange"> {
  group: string;
  items: Item[];
  label: string;
  selected?: Item[];
  onChange: (items: Item[]) => void;
  itemId?: keyof Item;
  itemLabel?: keyof Item | ((item: Item) => string);
  itemDescription?: (item: Item) => string;
}

function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const getDescendantProp = (obj: any, path: string) =>
  path.split(".").reduce((acc, part) => acc && acc[part], obj);

const AppMultiselect = (props: Props) => {
  const [selected, setSelected] = useState<Item[]>([]);

  useEffect(() => {
    if (!props.items || props.items.length === 0) return;
    if (!props.selected) return;
    setSelected([...props.selected]);
  }, [props.items, props.defaultValue]);

  const _items = useMemo(() => {
    return [...props.items];
  }, [props.items]);

  const idGetter = useCallback(
    (item: Item) => {
      if (item._id) return item._id;
      if (!props.itemId) return item.id;
      return getDescendantProp(item, props.itemId as string);
    },
    [props.itemId]
  );

  const labelGetter = useCallback(
    (item: Item) => {
      // if "Select an Option", return
      if (item._id) return item._label;
      // if itemLabel not provided, default to label
      if (!props.itemLabel) return item.label;
      // if itemLabel is a function, return the results of the function
      if (typeof props.itemLabel === "function") return props.itemLabel(item);
      // otherwise, return the itemLabel key
      return getDescendantProp(item, props.itemLabel as string);
    },
    [props.itemLabel]
  );

  const _onChange = (items: Item[]) => {
    setSelected(items);
    props.onChange(items);
  };

  return (
    <Listbox value={selected} onChange={_onChange} multiple={true}>
      {({ open }) => (
        <>
          <Listbox.Label className="block text-sm font-medium text-gray-700">
            {props.label}
          </Listbox.Label>
          <div className="relative mt-1">
            <Listbox.Button className="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 sm:text-sm">
              <span className="block truncate">
                {selected.length
                  ? selected.map((item) => labelGetter(item)).join(", ")
                  : "Select an option"}
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
                    key={idGetter(item)}
                    className={({ active }) =>
                      classNames(
                        active ? "text-white bg-primary-600" : "text-gray-900",
                        "relative cursor-default select-none py-2 pl-3 pr-9"
                      )
                    }
                    value={item}
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
                              active ? "text-white" : "text-primary-600",
                              "absolute inset-y-0 right-0 flex items-center pr-4"
                            )}
                          >
                            <CheckIcon className="h-5 w-5" aria-hidden="true" />
                          </span>
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
  );
};

export default AppMultiselect;
