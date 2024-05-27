import { cn } from "@/lib/utils";

interface AppPanelProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export default function AppPanel({
  children,
  className,
  ...props
}: AppPanelProps) {
  return (
    <div
      className={cn("overflow-hidden bg-white shadow sm:rounded-lg", className)}
      {...props}
    >
      <div className="px-4 py-5 sm:p-6">{children}</div>
    </div>
  );
}
