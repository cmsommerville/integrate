import * as z from "zod";
import * as api from "@/api-fetcher";
import { NewRatingMapperCollectionType } from "@/config/types";
import { RatingMapperCollectionFormSchema } from "@/config/schemas";

export const INITIAL_DATA: NewRatingMapperCollectionType = {
  config_attribute_set_id: -999,
  config_rating_mapper_collection_label: "",
  default_config_rating_mapper_set_id: undefined,
  is_selectable: false,
};

export const getSingleRatingMapperCollection = async (id: number) => {
  const res = await api.GET(`/api/config/mappers/collection/${id}`, {
    cache: "no-cache",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};

export const getNewCollectionDropdowns = async () => {
  const res = await api.GET(`/api/config/attribute/sets`, {
    cache: "no-cache",
  });
  if (res.ok) {
    const data = await res.json();
    return data;
  }
  throw new Error(res.statusText);
};

export const createNewRatingMapperCollection = async (
  data: z.infer<typeof RatingMapperCollectionFormSchema>
) => {
  const output = RatingMapperCollectionFormSchema.safeParse(data);
  if (output.success) {
    const res = await api.POST(`/api/config/mappers/collection`, {
      body: JSON.stringify(output.data),
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      const data = await res.json();
      return data;
    }
    throw new Error(res.statusText);
  }
};
