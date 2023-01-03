import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import moment from "moment";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";

const ConfigProductVariationDetail = () => {
  const { product_id, product_variation_id } = useParams();
  return;
};

export default ConfigProductVariationDetail;
