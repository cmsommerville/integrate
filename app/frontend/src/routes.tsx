import React from "react";
import { Routes, Route, Link } from "react-router-dom";

import RatingWorkbench from "@/pages/RatingWorkbench";

export const routes = [
  {
    key: "RatingWorkbench",
    path: "/app/plan/:plan_id/rating/workbench",
    element: <RatingWorkbench />,
  },
];
