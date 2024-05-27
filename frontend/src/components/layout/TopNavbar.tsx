import { FaMagnifyingGlass, FaRegUser } from "react-icons/fa6";
import { useQuery } from "@tanstack/react-query";
import { useAuthContext } from "@/providers/AuthContext";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuTrigger,
  DropdownMenuItem,
  DropdownMenuGroup,
} from "@/components/ui/dropdown-menu";
import { DropdownMenuSeparator } from "@radix-ui/react-dropdown-menu";
import { UserType } from "@/types/auth";
import Avatar from "./Avatar";

const getUser = async () => {
  const res = await fetch("/api/auth/me", { credentials: "include" });
  if (!res.ok) {
    const data = await res.json();
    throw new Error(data.msg);
  }
  return res.json();
};

interface UserAvatarMenuProps {
  user: UserType | undefined;
}
const UserAvatarMenu = ({ user }: UserAvatarMenuProps) => {
  if (!user)
    return (
      <div className="hidden lg:ml-4 lg:flex lg:items-center pr-4">
        <div className="relative flex-shrink-0 rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
          <Avatar user={user} />
        </div>
      </div>
    );

  return (
    <div className="hidden lg:ml-4 lg:flex lg:items-center pr-4">
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <button
            type="button"
            className="relative flex-shrink-0 rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            <span className="absolute -inset-1.5" />
            <span className="sr-only">View notifications</span>
            <Avatar user={user} />
          </button>
        </DropdownMenuTrigger>
        <DropdownMenuContent className="w-56 text-gray-700">
          <DropdownMenuLabel>Profile</DropdownMenuLabel>
          <DropdownMenuSeparator />
          <DropdownMenuGroup>
            <DropdownMenuItem>
              <FaRegUser className="inline-block mr-3" />
              {user?.first_name} {user?.last_name}
            </DropdownMenuItem>
          </DropdownMenuGroup>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  );
};

export default function TopNavbar() {
  const { user, setUser } = useAuthContext();

  const qry_user = useQuery({
    queryKey: ["user.me"],
    queryFn: getUser,
    retry: false,
  });

  if (qry_user.isSuccess) {
    setUser(qry_user.data);
  }
  if (qry_user.isError) {
    setUser(undefined);
  }

  return (
    <>
      <div className="bg-white fixed left-[200px] w-[calc(100%-200px)]">
        <div className="flex h-16 justify-between">
          <div className="flex px-2 lg:px-0">
            <div className="hidden lg:ml-6 lg:flex lg:space-x-8">
              <a
                href="#"
                className="inline-flex items-center border-b-2 border-indigo-500 px-1 pt-1 text-sm font-medium text-gray-900"
              >
                Dashboard
              </a>
              <a
                href="#"
                className="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700"
              >
                Team
              </a>
              <a
                href="#"
                className="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700"
              >
                Projects
              </a>
              <a
                href="#"
                className="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium text-gray-500 hover:border-gray-300 hover:text-gray-700"
              >
                Calendar
              </a>
            </div>
          </div>
          <div className="flex flex-1 items-center justify-center px-2 lg:ml-6 lg:justify-end">
            <div className="w-full max-w-lg lg:max-w-xs">
              <label htmlFor="search" className="sr-only">
                Search
              </label>
              <div className="relative">
                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                  <FaMagnifyingGlass
                    className="h-5 w-5 text-gray-400"
                    aria-hidden="true"
                  />
                </div>
                <input
                  id="search"
                  name="search"
                  className="block w-full rounded-md border-0 bg-white py-1.5 pl-10 pr-3 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                  placeholder="Search"
                  type="search"
                />
              </div>
            </div>
          </div>
          <div className="flex items-center lg:hidden">
            {/* Mobile menu button */}
          </div>
          <UserAvatarMenu user={user} />
        </div>
      </div>
    </>
  );
}
