import { cn } from "@/lib/utils";

interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: "success" | "warning" | "error";
  children: React.ReactNode;
}
export default function Badge({ children, className, variant }: BadgeProps) {
  const variant_color = () => {
    if (variant === "success") {
      return "bg-green-400/30 text-green-700";
    }
    if (variant === "warning") {
      return "bg-amber-400/30 text-amber-700";
    }
    if (variant === "error") {
      return "bg-red-400/30 text-red-700";
    }
    return "bg-green-400/30 text-green-700";
  };

  return (
    <div className="flex items-end">
      <span
        className={cn(
          "px-2 py-1 rounded font-semibold text-xs",
          variant_color(),
          className
        )}
      >
        {children}
      </span>
    </div>
  );
}
