import { BriefcaseIcon, PuzzlePieceIcon } from "@heroicons/react/20/solid";

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const tabs = [
  { code: "basic", label: "Basic Info", icon: BriefcaseIcon },
  { code: "addl", label: "Additional Data", icon: PuzzlePieceIcon },
  { code: "values", label: "Values", icon: PuzzlePieceIcon },
] as const;

export type TabCode = typeof tabs[number]["code"];

interface TabProps {
  selected: TabCode;
  onClick: (selected: TabCode) => any;
}

export const Tabs = ({ selected, onClick }: TabProps) => {
  return (
    <div className="hidden sm:block mb-4">
      <div className="border-b border-gray-200">
        <nav aria-label="Tabs">
          <ul className="-mb-px flex space-x-8">
            {tabs.map((tab, ix) => (
              <li
                key={tab.label}
                className={classNames(
                  tab.code === selected
                    ? "border-indigo-500 text-indigo-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300",
                  "group inline-flex items-center py-4 px-1 border-b-2 font-medium text-sm cursor-pointer"
                )}
                aria-current={tab.code === selected ? "page" : undefined}
                onClick={() => onClick(tab.code)}
              >
                <tab.icon
                  className={classNames(
                    tab.code === selected
                      ? "text-indigo-500"
                      : "text-gray-400 group-hover:text-gray-500",
                    "-ml-0.5 mr-2 h-5 w-5"
                  )}
                  aria-hidden="true"
                />
                <span>{tab.label}</span>
              </li>
            ))}
          </ul>
        </nav>
      </div>
    </div>
  );
};
