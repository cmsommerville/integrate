import { useState, useEffect, useMemo, useCallback } from "react";
import moment from "moment";
import { ConfigProduct } from "./types";

type Props = {
  product: ConfigProduct;
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
            htmlFor="product_issue_date"
            className="block text-sm font-medium text-gray-700"
          >
            Issue Date
          </label>
          <div className="mt-1">
            <input
              type="date"
              name="product_issue_date"
              id="product_issue_date"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              onChange={(e) => onChange("product_issue_date", e.target.value)}
              value={product.product_issue_date ?? ""}
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="master_product_code"
            className="block text-sm font-medium text-gray-700"
          >
            Master Product Code
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="master_product_code"
              id="master_product_code"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              onChange={(e) => onChange("master_product_code", e.target.value)}
              value={product.master_product_code ?? ""}
            />
          </div>
        </div>

        <div>
          <label
            htmlFor="form_code"
            className="block text-sm font-medium text-gray-700"
          >
            Form Code
          </label>
          <div className="mt-1">
            <input
              type="text"
              name="form_code"
              id="form_code"
              className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
              onChange={(e) => onChange("form_code", e.target.value)}
              value={product.form_code ?? ""}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label
              htmlFor="min_issue_age"
              className="block text-sm font-medium text-gray-700"
            >
              Min Issue Age
            </label>
            <div className="mt-1">
              <input
                type="number"
                name="min_issue_age"
                id="min_issue_age"
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                onChange={(e) => onChange("min_issue_age", e.target.value)}
                value={product.min_issue_age ?? 0}
              />
            </div>
          </div>
          <div>
            <label
              htmlFor="max_issue_age"
              className="block text-sm font-medium text-gray-700"
            >
              Max Issue Age
            </label>
            <div className="mt-1">
              <input
                type="number"
                name="max_issue_age"
                id="max_issue_age"
                className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                onChange={(e) => onChange("max_issue_age", e.target.value)}
                value={product.max_issue_age ?? 120}
              />
            </div>
          </div>
        </div>
      </form>
    </>
  );
};

export default ConfigProductDetailOptionalFields;
