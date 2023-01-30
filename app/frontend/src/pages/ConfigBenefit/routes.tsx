import { RouteObject } from "react-router-dom";

import ConfigBenefitDetailBasicInfo from "./ConfigBenefitDetailBasicInfo";
import ConfigBenefitDetailAddlInfo from "./ConfigBenefitDetailAddlInfo";
import ConfigBenefitDetailValuesList from "./ConfigBenefitDetailValuesList";

interface AppRouteObject extends RouteObject {
  props?: any;
  children?: AppRouteObject[];
}

export const routes: AppRouteObject[] = [
  {
    path: "benefit",
    element: <ConfigBenefitDetailBasicInfo />,
  },
  {
    path: "benefit/:benefit_id",
    children: [
      {
        path: "basic",
        element: <ConfigBenefitDetailBasicInfo />,
      },
      {
        path: "addl",
        element: <ConfigBenefitDetailAddlInfo />,
      },
      {
        path: "values",
        element: <ConfigBenefitDetailValuesList />,
      },
    ],
  },
];
