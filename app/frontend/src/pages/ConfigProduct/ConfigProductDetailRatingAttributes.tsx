import { useState, useEffect, useMemo, useCallback } from "react";
import { useParams, useNavigate } from "react-router";
import { Link } from "react-router-dom";
import {
  ConfigProduct_Basic,
  ConfigAttributeSet,
  ConfigProduct_AttrSets,
} from "@/types/config";
import { UsersIcon, HeartIcon, MoonIcon } from "@heroicons/react/24/outline";
import { ChevronLeftIcon, ChevronRightIcon } from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";
import AppRadioSelect from "@/components/AppRadioSelect";
import { Breadcrumb, PageTitle } from "./Components";

const PAGE_DETAILS = {
  id: "attr-sets",
  title: "Attributes",
  subtitle:
    "Specify the attributes used for smoker disposition, gender, and relationships...",
};

const ConfigProductDetailRatingAttributes = () => {
  const { product_id } = useParams();
  const navigate = useNavigate();

  const [isDirty, setIsDirty] = useState(false);
  const [isValid, setIsValid] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  const [product, setProduct] = useState<
    ConfigProduct_Basic & ConfigProduct_AttrSets
  >();
  const [genders, setGenders] = useState<ConfigAttributeSet[]>([]);
  const [smokerDisps, setSmokerDisps] = useState<ConfigAttributeSet[]>([]);
  const [relationships, setRelationships] = useState<ConfigAttributeSet[]>([]);

  const [selection, setSelection] = useState<ConfigProduct_AttrSets>(
    DEFAULT_PRODUCT_ATTRS
  );

  useEffect(() => {
    fetch(`/api/config/product/${product_id}`)
      .then((res) => res.json())
      .then((res) => {
        setProduct(res);
        if (res.gender_attr_set_id) {
          setSelection({
            gender_attr_set_id: res.gender_attr_set_id,
            smoker_status_attr_set_id: res.smoker_status_attr_set_id,
            relationship_attr_set_id: res.relationship_attr_set_id,
          });
        }
      });
  }, [product_id]);

  useEffect(() => {
    fetch("/api/config/attribute/sets/smoker_status")
      .then((res) => res.json())
      .then((res) => {
        setSmokerDisps(res);
      });

    fetch("/api/config/attribute/sets/gender")
      .then((res) => res.json())
      .then((res) => {
        setGenders(res);
      });

    fetch("/api/config/attribute/sets/relationship")
      .then((res) => res.json())
      .then((res) => {
        setRelationships(res);
      });
  }, []);

  const setter = (key: keyof ConfigProduct_AttrSets, val: number) => {
    setSelection((prev) => ({ ...prev, [key]: val }));
    setIsDirty(true);
  };

  const clickHandler = () => {
    if (!isDirty) {
      return;
    }
    fetch(`/api/config/product/${product_id}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(selection),
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error("Cannot save to database");
        }
        return res.json();
      })
      .then((res) => {
        setProduct(res);
        setIsDirty(false);
      })
      .finally(() => {});
  };

  return (
    <>
      <PageTitle title={PAGE_DETAILS.title} subtitle={PAGE_DETAILS.subtitle}>
        <div className="space-x-6 flex">
          <Link to={`/app/config/product/${product_id}/`}>
            <span className="flex items-center text-sm font-semibold text-primary-700 hover:text-accent-600 transition duration-300">
              <ChevronLeftIcon className="h-5 w-5" />
              Prev
            </span>
          </Link>
          <Link to={`/app/config/product/${product_id}/rating/dists`}>
            <span className="flex items-center text-sm font-semibold text-primary-700 hover:text-accent-600 transition duration-300">
              Next
              <ChevronRightIcon className="h-5 w-5" />
            </span>
          </Link>
        </div>
      </PageTitle>
      <div className="grid grid-cols-6 gap-x-6">
        <div className="col-span-2 flex flex-col space-y-6">
          <AppPanel className="pt-0 pl-0 pr-0 h-fit space-y-6">
            <>
              <h3 className="font-normal text-white py-4 px-4 bg-primary-700 rounded-t-lg flex space-x-2">
                <HeartIcon className="h-6 w-6" aria-hidden="true" />
                <span>Genders</span>
              </h3>
              <div className="px-4 pb-4">
                <AppRadioSelect
                  group="gender"
                  items={genders}
                  itemId="config_attr_set_id"
                  itemLabel="config_attr_set_label"
                  itemDescription={(item) => {
                    return item.attributes
                      .map(
                        (a: any) =>
                          `${a.config_attr_detail_label}${"\xa0"}(${
                            a.config_attr_detail_code
                          })`
                      )
                      .join(" / ");
                  }}
                  defaultValue={product?.gender_attr_set_id}
                  onClick={(item) =>
                    setter("gender_attr_set_id", item.config_attr_set_id)
                  }
                />
              </div>
            </>
          </AppPanel>

          <AppPanel className="pt-0 pl-0 pr-0 h-fit space-y-6">
            <>
              <h3 className="font-normal text-white py-4 px-4 bg-primary-700 rounded-t-lg flex space-x-2">
                <MoonIcon className="h-6 w-6" aria-hidden="true" />
                <span>Smoker Dispositions</span>
              </h3>
              <div className="px-4 pb-4">
                <AppRadioSelect
                  group="smoker-status"
                  items={smokerDisps}
                  itemId="config_attr_set_id"
                  itemLabel="config_attr_set_label"
                  itemDescription={(item) => {
                    return item.attributes
                      .map(
                        (a: any) =>
                          `${a.config_attr_detail_label}${"\xa0"}(${
                            a.config_attr_detail_code
                          })`
                      )
                      .join(" / ");
                  }}
                  defaultValue={product?.smoker_status_attr_set_id}
                  onClick={(item) =>
                    setter("smoker_status_attr_set_id", item.config_attr_set_id)
                  }
                />
              </div>
            </>
          </AppPanel>
        </div>
        <div className="col-span-2 flex flex-col space-y-4">
          <AppPanel className="pt-0 pl-0 pr-0 h-fit space-y-6">
            <>
              <h3 className="font-normal text-white py-4 px-4 bg-primary-700 rounded-t-lg flex space-x-2">
                <UsersIcon className="h-6 w-6" aria-hidden="true" />
                <span>Relationships</span>
              </h3>

              <div className="px-4 pb-4">
                <AppRadioSelect
                  group="relationships"
                  items={relationships}
                  itemId="config_attr_set_id"
                  itemLabel="config_attr_set_label"
                  itemDescription={(item) => {
                    return item.attributes
                      .map((a: any) => `${a.config_attr_detail_label}`)
                      .join(" / ");
                  }}
                  defaultValue={product?.relationship_attr_set_id}
                  onClick={(item) =>
                    setter("relationship_attr_set_id", item.config_attr_set_id)
                  }
                />
              </div>
            </>
          </AppPanel>
        </div>
        <div className="col-span-2 flex flex-col items-end space-y-6">
          <Breadcrumb step="attr-sets" />
          <AppButton
            disabled={!isValid || !isDirty}
            isLoading={isSaving}
            onClick={clickHandler}
          >
            Save
          </AppButton>
        </div>
      </div>
    </>
  );
};

const DEFAULT_PRODUCT_ATTRS = {
  gender_attr_set_id: undefined,
  smoker_status_attr_set_id: undefined,
  relationship_attr_set_id: undefined,
};

export default ConfigProductDetailRatingAttributes;
