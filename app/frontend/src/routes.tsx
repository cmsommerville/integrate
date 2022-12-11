import React from "react";
import { Routes, Route, Link } from "react-router-dom";

import { ConfigProductDetail } from "./pages/ConfigProduct";

export const routes = [
  {
    key: "ConfigProductDetail",
    path: "/app/config/product/:product_id",
    element: <ConfigProductDetail />,
  },
];
