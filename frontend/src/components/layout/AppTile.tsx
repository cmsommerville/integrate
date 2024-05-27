import { cn } from "@/lib/utils";
import React from "react";

interface AppTileProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  icon?: React.ReactNode;
}

export default function AppTile({
  children,
  className,
  icon,
  ...props
}: AppTileProps) {
  return (
    <div
      className="relative col-span-1 flex flex-col divide-y divide-gray-200 rounded-lg bg-white shadow overflow-hidden"
      {...props}
    >
      <div className="absolute text-white h-6 w-6 top-2 right-0">{icon}</div>
      <div
        className={cn("h-40 w-full flex-shrink-0 bg-rose-400", className)}
      ></div>
      <div className="flex justify-between items-center p-4">
        <div className="flex flex-1 justify-between text-sm font-semibold text-gray-900 space-x-8">
          {children}
        </div>
      </div>
    </div>
  );
}
