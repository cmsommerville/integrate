"use client";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useState } from "react";

export default function DeleteRecord(params: any) {
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [errors, setErrors] = useState("");

  const onDelete = async () => {
    const res = await params.onDelete(params.data);
    if (res.ok) {
      setIsOpen(false);
      router.refresh();
    } else {
      setErrors(res.statusText);
    }
  };
  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DialogTrigger asChild>
        <button className="text-primary-500 hover:text-primary-700 transition duration-100 font-sm flex justify-center">
          Delete
        </button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader className="space-y-4">
          <DialogTitle>Are you sure?</DialogTitle>
          <DialogDescription>
            {params.deleteMessage ?? "Do you want to delete this record?"}
          </DialogDescription>
        </DialogHeader>
        <DialogFooter className="sm:flex sm:flex-col items-end space-y-2">
          <Button variant="destructive" onClick={() => onDelete()}>
            Delete
          </Button>
          {errors ? (
            <span className="text-xs text-red-500 text-right">{errors}</span>
          ) : null}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
