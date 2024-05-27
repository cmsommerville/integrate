import { cn } from "@/lib/utils";
import { UserType } from "@/types/auth";
import { FaRegUser } from "react-icons/fa6";

interface AvatarProps {
  user: UserType | undefined;
  className?: string;
}

export default function Avatar({ user, className }: AvatarProps) {
  if (!user)
    return (
      <div
        className={cn(
          "h-10 w-10 rounded-full bg-gray-200 text-gray-700 flex justify-center items-center",
          className
        )}
      >
        <FaRegUser />
      </div>
    );
  if (!user.avatar)
    return (
      <div
        className={cn(
          "h-10 w-10 rounded-full bg-gray-200 text-gray-700 flex justify-center items-center",
          className
        )}
      >
        {Array.from(user.first_name)[0].toUpperCase() +
          Array.from(user.last_name)[0].toUpperCase()}
      </div>
    );

  return (
    <img className="h-10 w-10 rounded-full" src={user.avatar} alt="avatar" />
  );
}
