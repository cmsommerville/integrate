import { cn } from "@/lib/utils";

interface ErrorTextProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
}

export const ErrorText = ({ className, children }: ErrorTextProps) => (
  <div className={cn("text-red-500 text-xs line-clamp-3 leading-6", className)}>
    {children}
  </div>
);
