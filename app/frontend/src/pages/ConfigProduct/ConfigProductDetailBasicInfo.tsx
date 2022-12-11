import { useState, useEffect, useMemo, useCallback } from "react";
import moment from "moment";
import { Product } from "./types";

type Props = {
  product: Product;
  onChange(key: string, val: string): void;
};

function classNames(...classes: string[]) {
  return classes.filter(Boolean).join(" ");
}

const ConfigProductDetailOptionalFields = ({
  product,
  onChange,
  ...props
}: Props) => {
  return (
    <>
      <form className="space-y-4">
        <div>
          <label
            htmlFor="config_product_code"
            className="block text-sm font-medium text-gray-700"
          >
            Product Code
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="config_product_code"
              id="config_product_code"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm placeholder:text-gray-400"
              placeholder="C21000"
              onChange={(e) => onChange("config_product_code", e.target.value)}
              value={product.config_product_code ?? ""}
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="config_product_label"
            className="block text-sm font-medium text-gray-700"
          >
            Product Label
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="config_product_label"
              id="config_product_label"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm placeholder:text-gray-400"
              placeholder="Critical Illness Series C21000"
              onChange={(e) => onChange("config_product_label", e.target.value)}
              value={product.config_product_label ?? ""}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label
              htmlFor="config_product_effective_date"
              className="block text-sm font-medium text-gray-700"
            >
              Effective Date
            </label>
            <div className="mt-1">
              <input
                type="date"
                name="config_product_effective_date"
                id="config_product_effective_date"
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                onChange={(e) =>
                  onChange("config_product_effective_date", e.target.value)
                }
                value={product.config_product_effective_date ?? ""}
              />
            </div>
          </div>
          <div>
            <label
              htmlFor="config_product_expiration_date"
              className="block text-sm font-medium text-gray-700"
            >
              Expiration Date
            </label>
            <div className="mt-1">
              <input
                type="date"
                name="config_product_expiration_date"
                id="config_product_expiration_date"
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                onChange={(e) =>
                  onChange("config_product_expiration_date", e.target.value)
                }
                value={product.config_product_expiration_date ?? ""}
              />
            </div>
          </div>
        </div>
      </form>
    </>
  );
};

export default ConfigProductDetailOptionalFields;
