import { Fragment, useState } from "react";
import { Combobox, Dialog, Transition, RadioGroup } from "@headlessui/react";
import { MagnifyingGlassIcon } from "@heroicons/react/20/solid";
import {
  ChevronDownIcon,
  ChevronUpIcon,
  ExclamationCircleIcon,
  PencilSquareIcon,
} from "@heroicons/react/24/outline";

const items = [
  {
    id: 0,
    name: "Rating Attributes",
    description: "Toggle the rates",
    url: "#",
    color: "bg-indigo-500",
  },
  {
    id: 1,
    name: "Smoker Disposition",
    description: "Change the smoker disposition",
    url: "#",
    color: "bg-indigo-500",
  },
  {
    id: 2,
    name: "Gender Disposition",
    description: "Change the geender disposition",
    url: "#",
    color: "bg-indigo-500",
  },
  // More items...
];

function classNames(...classes: any) {
  return classes.filter(Boolean).join(" ");
}

const Accordion = () => {
  const [query, setQuery] = useState("");
  const [selection, setSelection] = useState<{ id: number | string }>({
    id: 0,
  });

  const filteredItems =
    query === ""
      ? items
      : items.filter((item) => {
          return item.name.toLowerCase().includes(query.toLowerCase());
        });

  return (
    <div className="mx-auto max-w-xl w-96 min-h-full transform divide-y divide-gray-100 overflow-hidden rounded-xl bg-white shadow-2xl ring-1 ring-black ring-opacity-5 transition-all">
      <Combobox onChange={(item: any) => (window.location = item.url)}>
        <div className="relative">
          <MagnifyingGlassIcon
            className="pointer-events-none absolute top-3.5 left-4 h-5 w-5 text-gray-400"
            aria-hidden="true"
          />
          <Combobox.Input
            className="h-12 w-full border-0 bg-transparent pl-11 pr-4 text-gray-800 placeholder-gray-400 focus:ring-0 sm:text-sm focus-visible:outline-none"
            placeholder="Search..."
            onChange={(event) => setQuery(event.target.value)}
          />
        </div>

        {filteredItems.length > 0 && (
          <Combobox.Options
            static
            className="max-h-96 scroll-py-3 overflow-y-auto p-3"
          >
            {filteredItems.map((item) => (
              <Combobox.Option
                key={item.id}
                value={item}
                className={({ active }) =>
                  classNames(
                    "flex cursor-default select-none rounded-xl p-3",
                    active && "bg-gray-100"
                  )
                }
              >
                {({ active }) => (
                  <div>
                    <div
                      className={classNames(
                        "flex flex-none items-center rounded-lg cursor-pointer space-x-2"
                      )}
                      onClick={() => setSelection(item)}
                    >
                      <ChevronDownIcon
                        className="h-4 w-4 text-primary-500"
                        aria-hidden="true"
                      />
                      <p
                        className={classNames(
                          "text-sm font-medium",
                          active ? "text-gray-900" : "text-gray-700"
                        )}
                      >
                        {item.name}
                      </p>
                    </div>
                    {item.id === selection.id ? <div>Hello world!</div> : null}
                  </div>
                )}
              </Combobox.Option>
            ))}
          </Combobox.Options>
        )}

        {query !== "" && filteredItems.length === 0 && (
          <div className="py-14 px-6 text-center text-sm sm:px-14">
            <ExclamationCircleIcon
              type="outline"
              name="exclamation-circle"
              className="mx-auto h-6 w-6 text-gray-400"
            />
            <p className="mt-4 font-semibold text-gray-900">No results found</p>
            <p className="mt-2 text-gray-500">
              No components found for this search term. Please try again.
            </p>
          </div>
        )}
      </Combobox>
    </div>
  );
};

export default Accordion;
