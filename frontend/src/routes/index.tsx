import { createFileRoute } from "@tanstack/react-router";
import AppPanel from "@/components/layout/AppPanel";
import AppTile from "@/components/layout/AppTile";
import Badge from "@/components/layout/Badge";
import { HiSparkles, HiOutlineDocumentPlus } from "react-icons/hi2";
import { FaEllipsisVertical } from "react-icons/fa6";

function HomePage() {
  return (
    <div className="grid grid-cols-3 gap-8 h-full">
      <div className="col-span-2 grid grid-cols-3 gap-8">
        <div>
          <AppTile className="bg-cyan-500/50" icon={<HiOutlineDocumentPlus />}>
            <div className="relative w-full flex justify-between items-center">
              <span>Create a new plan</span>
              <Badge
                variant="success"
                className="absolute -top-12 right-0 bg-green-200"
              >
                Popular
              </Badge>
              <button>
                <FaEllipsisVertical className="text-gray-400" />
              </button>
            </div>
          </AppTile>
        </div>
        <div>
          <AppTile>
            <div className="w-full flex justify-between items-center">
              <span>Setup a new product</span>
              <button>
                <FaEllipsisVertical className="text-gray-400" />
              </button>
            </div>
          </AppTile>
        </div>
        <div>
          <AppTile className="bg-emerald-600/50" icon={<HiSparkles />}>
            <div className="w-full flex justify-between items-center">
              <span>Create a new plan</span>
              <button>
                <FaEllipsisVertical className="text-gray-400" />
              </button>
            </div>
          </AppTile>
        </div>
      </div>
      <div>
        <AppPanel className="h-full">
          <span></span>
        </AppPanel>
      </div>
    </div>
  );
}

export const Route = createFileRoute("/")({
  component: () => <HomePage />,
});
