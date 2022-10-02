import React, { useState, useEffect, useCallback } from "react";
import { Routes, Route, Link } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";

import { routes } from "./routes";

const App = () => {
  return (
    <MainLayout>
      <Routes>
        {routes.map((route_config) => {
          return React.createElement(Route, route_config);
        })}
      </Routes>
    </MainLayout>
  );
};

export default App;
