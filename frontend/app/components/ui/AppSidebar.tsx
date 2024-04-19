import Link from "next/link";
import {
  PiAtom,
  PiBriefcase,
  PiCalculator,
  PiFilePlus,
  PiGear,
  PiUser,
} from "react-icons/pi";
import { classNames } from "@/utils";

const navigation = [
  { name: "New Quote", href: "#", icon: PiFilePlus, current: true },
  {
    name: "Products",
    href: "/config/products",
    icon: PiBriefcase,
    current: false,
  },
  { name: "Benefits", href: "#", icon: PiAtom, current: false },
  { name: "Provisions", href: "#", icon: PiCalculator, current: false },
  { name: "Admin", href: "#", icon: PiGear, current: false },
];
const teams = [
  { id: 1, name: "Heroicons", href: "#", initial: "H", current: false },
  { id: 2, name: "Tailwind Labs", href: "#", initial: "T", current: false },
  { id: 3, name: "Workcation", href: "#", initial: "W", current: false },
];

export default function AppSidebar() {
  return (
    <>
      <div className="fixed inset-y-0 z-50 flex w-72 flex-col">
        <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6">
          <div className="flex h-16 shrink-0 items-center"></div>
          <nav className="flex flex-1 flex-col">
            <ul role="list" className="flex flex-1 flex-col gap-y-7">
              <li>
                <ul role="list" className="-mx-2 space-y-1">
                  {navigation.map((item) => (
                    <li key={item.name}>
                      <Link
                        href={item.href}
                        className={classNames(
                          item.current
                            ? "bg-gray-50 text-primary-600"
                            : "text-gray-700 hover:text-primary-600 hover:bg-gray-50",
                          "group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold"
                        )}
                      >
                        <item.icon
                          className={classNames(
                            item.current
                              ? "text-primary-600"
                              : "text-gray-400 group-hover:text-primary-600",
                            "h-6 w-6 shrink-0"
                          )}
                          aria-hidden="true"
                        />
                        {item.name}
                      </Link>
                    </li>
                  ))}
                </ul>
              </li>
              <li>
                <div className="text-xs font-semibold leading-6 text-gray-400">
                  Your teams
                </div>
                <ul role="list" className="-mx-2 mt-2 space-y-1">
                  {teams.map((team) => (
                    <li key={team.name}>
                      <Link
                        href={team.href}
                        className={classNames(
                          team.current
                            ? "bg-gray-50 text-primary-600"
                            : "text-gray-700 hover:text-primary-600 hover:bg-gray-50",
                          "group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold"
                        )}
                      >
                        <span
                          className={classNames(
                            team.current
                              ? "text-primary-600 border-primary-600"
                              : "text-gray-400 border-gray-200 group-hover:border-primary-600 group-hover:text-primary-600",
                            "flex h-6 w-6 shrink-0 items-center justify-center rounded-lg border text-[0.625rem] font-medium bg-white"
                          )}
                        >
                          {team.initial}
                        </span>
                        <span className="truncate">{team.name}</span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </li>
              <li className="-mx-6 mt-auto">
                <Link
                  href="#"
                  className="flex items-center gap-x-4 px-6 py-3 text-sm font-semibold leading-6 text-gray-900 hover:bg-gray-50"
                >
                  <PiUser
                    className={classNames(
                      "text-gray-400 group-hover:text-primary-600",
                      "h-6 w-6 shrink-0"
                    )}
                    aria-hidden="true"
                  />
                  <span className="sr-only">Your profile</span>
                  <span aria-hidden="true">Tom Cook</span>
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </>
  );
}
