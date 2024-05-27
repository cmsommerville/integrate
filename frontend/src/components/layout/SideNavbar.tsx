import { cn } from "@/lib/utils";
import {
  FaUser,
  FaHouse,
  FaFolder,
  FaCalendar,
  FaFile,
  FaChartPie,
} from "react-icons/fa6";
import { Link } from "@tanstack/react-router";

const navigation = [
  { name: "Dashboard", to: "#", icon: FaHouse },
  {
    name: "Login",
    icon: FaUser,
    to: "/auth/login",
  },
  {
    name: "Projects",
    icon: FaFolder,
    to: "/projects",
  },
  { name: "Calendar", to: "#", icon: FaCalendar },
  { name: "Documents", to: "#", icon: FaFile },
  { name: "Reports", to: "#", icon: FaChartPie },
];

export default function SideNavbar() {
  return (
    <div className="fixed h-full w-[200px] flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6">
      <div className="flex h-16 shrink-0 items-center">
        <img
          className="h-8 w-auto"
          src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600"
          alt="Your Company"
        />
      </div>
      <nav className="flex flex-1 flex-col">
        <ul role="list" className="flex flex-1 flex-col gap-y-7">
          <li>
            <ul role="list" className="-mx-2 space-y-1">
              {navigation.map((item) => (
                <li key={item.name}>
                  <Link
                    to={item.to}
                    className={cn(
                      "group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold text-gray-700 hover:bg-indigo-50"
                    )}
                    activeProps={{ className: "bg-gray-100" }}
                  >
                    <item.icon
                      className="h-6 w-6 shrink-0 text-gray-400"
                      aria-hidden="true"
                    />
                    {item.name}
                  </Link>
                </li>
              ))}
            </ul>
          </li>
          <li className="-mx-6 mt-auto">
            <Link
              to="/"
              className="flex items-center gap-x-4 px-6 py-3 text-sm font-semibold leading-6 text-gray-900 hover:bg-gray-50"
            >
              <img
                className="h-8 w-8 rounded-full bg-gray-50"
                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                alt=""
              />
              <span className="sr-only">Your profile</span>
              <span aria-hidden="true">Tom Cook</span>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
