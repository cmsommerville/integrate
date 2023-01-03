import React, { useState, useEffect, useCallback } from "react";
import { RouterProvider } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";

import { router } from "./routes";

const App = () => {
  return (
    <MainLayout>
      <RouterProvider router={router} />
    </MainLayout>
  );
};

export default App;
