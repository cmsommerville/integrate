import React from "react";
import { RouteObject, createBrowserRouter } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import App from "./App";

import AuthUser from "./pages/AuthUser";
import { AuthRefresh } from "./pages/AuthUser";
import {
  ConfigProductList,
  ConfigProductDetail,
  ConfigProductDetailRatingAttributes,
  ConfigProductDetailRatingDistributions,
  ConfigProductDetailRatingStrategy,
  ConfigProductDetailCensus,
} from "./pages/ConfigProduct";
import { ConfigBenefitList, ConfigBenefitDetail } from "./pages/ConfigBenefit";
import { ConfigProductStateDetail } from "./pages/ConfigProductState";

interface AppRouteObject extends RouteObject {
  props?: any;
  children?: AppRouteObject[];
}

export const routes: AppRouteObject[] = [
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/auth/login",
        element: <AuthUser />,
      },
      {
        path: "/auth/refresh",
        element: <AuthRefresh />,
      },
      {
        path: "/app/config/products",
        element: <ConfigProductList />,
      },
      {
        path: "/app/config/product",
        element: <ConfigProductDetail />,
      },
      {
        path: "/app/config/product/:product_id",
        element: <ConfigProductDetail />,
      },
      {
        path: "app/config/product/:product_id/rating/attrs",
        element: <ConfigProductDetailRatingAttributes />,
      },
      {
        path: "app/config/product/:product_id/rating/dists",
        element: <ConfigProductDetailRatingDistributions />,
      },
      {
        path: "app/config/product/:product_id/rating/strategy",
        element: <ConfigProductDetailRatingStrategy />,
      },
      {
        path: "app/config/product/:product_id/rating/census",
        element: <ConfigProductDetailCensus />,
      },
      {
        path: "/app/config/product/:product_id/states",
        element: <ConfigProductStateDetail />,
      },

      {
        path: "/app/config/product/:product_id/benefits",
        element: <ConfigBenefitList />,
      },
      {
        path: "/app/config/product/:product_id/benefit",
        element: <ConfigBenefitDetail />,
      },
      {
        path: "/app/config/product/:product_id/benefit/:benefit_id",
        element: <ConfigBenefitDetail />,
      },
    ],
  },
];

export const router = createBrowserRouter(routes);
