import React from "react";
import { RouteObject, createBrowserRouter } from "react-router-dom";

import {
  ConfigProductDetail,
  ConfigProductDetailRatingAttributes,
  ConfigProductDetailRatingDistributions,
  ConfigProductDetailRatingStrategy,
} from "./pages/ConfigProduct";
import { ConfigProductStateDetail } from "./pages/ConfigProductState";

interface AppRouteObject extends RouteObject {
  props?: any;
  children?: AppRouteObject[];
}

export const routes: AppRouteObject[] = [
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
    path: "/app/config/product/:product_id/states",
    element: <ConfigProductStateDetail />,
  },
];

export const router = createBrowserRouter(routes);
