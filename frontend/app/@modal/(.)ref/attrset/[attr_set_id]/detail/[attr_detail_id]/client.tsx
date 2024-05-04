"use client";
import { useRouter } from "next/navigation";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import ConfigAttributeDetailDisplay from "@/ref/attrset/[attr_set_id]/detail/[attr_detail_id]/client";
import { ConfigAttributeDetail } from "@/ref/types";

export default function ViewConfigAttributeDetailModalClient({
  data,
}: {
  data: ConfigAttributeDetail;
}) {
  const router = useRouter();
  return (
    <Dialog defaultOpen={true} onOpenChange={router.back}>
      <DialogContent className="sm:max-w-[425px] space-y-4">
        <DialogHeader>
          <DialogTitle>View Attribute</DialogTitle>
        </DialogHeader>
        <div className="">
          <ConfigAttributeDetailDisplay data={data} />
        </div>
      </DialogContent>
    </Dialog>
  );
}
