import { useState, useMemo, useCallback } from "react";
import { useParams } from "react-router";
import { Link } from "react-router-dom";
import { CheckCircleIcon } from "@heroicons/react/20/solid";

import { AppPanel } from "@/components/AppPanel";
import AppButton from "@/components/AppButton";

const STEPS = {
  "basic-info": {
    name: "Basic Info",
    order: 0,
    href: (product_id: string) => `/app/config/product/${product_id}`,
  },
  "attr-sets": {
    name: "Attributes",
    order: 10,
    href: (product_id: string) =>
      `/app/config/product/${product_id}/rating/attrs`,
  },
  distributions: {
    name: "Distributions",
    order: 20,
    href: (product_id: string) =>
      `/app/config/product/${product_id}/rating/dists`,
  },
  "rating-strategies": {
    name: "Rating Strategy",
    order: 30,
    href: (product_id: string) =>
      `/app/config/product/${product_id}/rating/strategy`,
  },
};

interface BreadcrumbProps {
  step: keyof typeof STEPS;
}

export const Breadcrumb = ({ step }: BreadcrumbProps) => {
  const { product_id } = useParams();

  const steps = useMemo(() => {
    const current = STEPS[step];
    return Object.values(STEPS)
      .sort((a, b) => (a.order < b.order ? -1 : 1))
      .map((step, i) => {
        const status =
          step.order < current.order
            ? "complete"
            : step.order === current.order
            ? "current"
            : "upcoming";
        return { ...step, status };
      });
  }, [step]);

  return (
    <>
      {product_id ? (
        <AppPanel className="">
          <div className="py-2 px-2">
            <nav className="flex justify-center" aria-label="Progress">
              <ol role="list" className="space-y-6">
                {steps.map((step) => (
                  <li key={step.name}>
                    {step.status === "complete" ? (
                      <Link to={step.href(product_id)} className="group">
                        <span className="flex items-start">
                          <span className="relative flex h-5 w-5 flex-shrink-0 items-center justify-center">
                            <CheckCircleIcon
                              className="h-full w-full text-primary-600 group-hover:text-primary-800"
                              aria-hidden="true"
                            />
                          </span>
                          <span className="ml-3 text-sm font-medium text-gray-500 group-hover:text-gray-900">
                            {step.name}
                          </span>
                        </span>
                      </Link>
                    ) : step.status === "current" ? (
                      <Link
                        to={step.href(product_id)}
                        className="flex items-start"
                        aria-current="step"
                      >
                        <span
                          className="relative flex h-5 w-5 flex-shrink-0 items-center justify-center"
                          aria-hidden="true"
                        >
                          <span className="absolute h-4 w-4 rounded-full bg-primary-200" />
                          <span className="relative block h-2 w-2 rounded-full bg-primary-600" />
                        </span>
                        <span className="ml-3 text-sm font-medium text-primary-600">
                          {step.name}
                        </span>
                      </Link>
                    ) : (
                      <Link to={step.href(product_id)} className="group">
                        <div className="flex items-start">
                          <div
                            className="relative flex h-5 w-5 flex-shrink-0 items-center justify-center"
                            aria-hidden="true"
                          >
                            <div className="h-2 w-2 rounded-full bg-gray-300 group-hover:bg-gray-400" />
                          </div>
                          <p className="ml-3 text-sm font-medium text-gray-500 group-hover:text-gray-900">
                            {step.name}
                          </p>
                        </div>
                      </Link>
                    )}
                  </li>
                ))}
              </ol>
            </nav>
          </div>
        </AppPanel>
      ) : null}
    </>
  );
};

interface PageTitleProps {
  title: string;
  subtitle?: string;
  children?: JSX.Element;
}

export const PageTitle = (props: PageTitleProps) => {
  return (
    <div className="flex justify-between pb-6">
      <div className="">
        <h2 className="text-2xl font-light tracking-wide text-gray-700">
          {props.title}
        </h2>
        {props.subtitle ? (
          <p className="text-sm text-gray-400">{props.subtitle}</p>
        ) : null}
      </div>
      <div className="flex justify-end items-end">{props.children ?? null}</div>
    </div>
  );
};
