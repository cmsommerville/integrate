"use client";
import { useRouter } from "next/navigation";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import NewForm from "@/ref/attrset/[attr_set_id]/detail/NewForm";
import { INITIAL_DATA } from "@/ref/attrset/[attr_set_id]/detail/data";

export default function ConfigAttributeDetailModal({
  params,
}: {
  params: { attr_set_id: string };
}) {
  const router = useRouter();
  return (
    <Dialog defaultOpen={true} onOpenChange={router.back}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create New Attribute</DialogTitle>
        </DialogHeader>
        <div className="">
          <NewForm
            data={{
              ...INITIAL_DATA,
              config_attr_set_id: parseInt(params.attr_set_id),
            }}
            success_route={`/ref/attrset/${params.attr_set_id}`}
          />
        </div>
      </DialogContent>
    </Dialog>
  );
}
