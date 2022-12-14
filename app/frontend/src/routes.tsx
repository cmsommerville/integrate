import React from "react";
import { Routes, Route, Link } from "react-router-dom";

import { ConfigProductDetail } from "./pages/ConfigProduct";
import { ConfigProductStateDetail } from "./pages/ConfigProductState";

export const routes = [
  {
    key: "ConfigProductDetail",
    path: "/app/config/product/:product_id",
    element: <ConfigProductDetail />,
  },
  {
    key: "ConfigProductState",
    path: "/app/config/product/:product_id/states",
    element: <ConfigProductStateDetail />,
  },
];
