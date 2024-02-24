import { classNames } from "@/utils";

export default function AppCard({
  children,
  className,
  ...props
}: React.HTMLProps<HTMLDivElement>) {
  return (
    <div
      className={classNames(
        "overflow-hidden bg-white shadow sm:rounded-lg px-4 py-5 sm:p-6",
        className ?? ""
      )}
      {...props}
    >
      {children}
    </div>
  );
}
