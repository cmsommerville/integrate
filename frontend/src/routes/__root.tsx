import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import TopNavbar from "../components/layout/TopNavbar";
import SideNavbar from "../components/layout/SideNavbar";

function Layout() {
  return (
    <>
      <div className="grid grid-cols-[200px_1fr]">
        <div className="h-screen">
          <SideNavbar />
        </div>
        <div className="w-full">
          <TopNavbar />
          <main
            id="detail"
            className="pt-20 pb-4 px-4 bg-gray-100 min-h-screen h-full"
          >
            <Outlet />
          </main>
        </div>
      </div>
      <TanStackRouterDevtools />
    </>
  );
}

export const Route = createRootRoute({
  component: () => <Layout />,
});
