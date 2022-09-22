/* This example requires Tailwind CSS v2.0+ */
import { Fragment, useEffect, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon, ChevronUpDownIcon } from "@heroicons/react/20/solid";

export type IAppSelectOption = {
  id: number | string;
  label: number | string | boolean;
};

interface IProps {
  options: IAppSelectOption[];
  selected?: IAppSelectOption;
  onChange?: any;
  children?: any;
}

function classNames(...classes: any[]) {
  return classes.filter(Boolean).join(" ");
}

const AppSelect = ({ options, selected, ...props }: IProps) => {
  const [selection, setSelection] = useState<IAppSelectOption>();

  useEffect(() => {
    if (selected) {
      setSelection(selected);
    }
  }, [selected]);

  const _onChange = (val: IAppSelectOption) => {
    setSelection(val);
    props.onChange(val);
  };

  return (
    <div>
      <Listbox value={selection} onChange={_onChange}>
        {({ open }) => (
          <>
            <Listbox.Label className="block text-sm font-medium text-gray-700">
              {props.children}
            </Listbox.Label>
            <div className="relative mt-1">
              <Listbox.Button className="relative w-full cursor-default rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 text-left shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm">
                <span className="block truncate">
                  {selection ? selection.label : null}
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
                  {options.map((opt) => (
                    <Listbox.Option
                      key={opt.id}
                      className={({ active }) =>
                        classNames(
                          active ? "text-white bg-indigo-600" : "text-gray-900",
                          "relative cursor-default select-none py-2 pl-3 pr-9"
                        )
                      }
                      value={opt}
                    >
                      {({ selected, active }) => (
                        <>
                          <span
                            className={classNames(
                              selected ? "font-semibold" : "font-normal",
                              "block truncate"
                            )}
                          >
                            {opt.label}
                          </span>

                          {selected ? (
                            <span
                              className={classNames(
                                active ? "text-white" : "text-indigo-600",
                                "absolute inset-y-0 right-0 flex items-center pr-4"
                              )}
                            >
                              <CheckIcon
                                className="h-5 w-5"
                                aria-hidden="true"
                              />
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
    </div>
  );
};

export default AppSelect;
