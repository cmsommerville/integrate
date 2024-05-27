import { createFileRoute, useLoaderData } from "@tanstack/react-router";
import AppPanel from "@/components/layout/AppPanel";
import { getSelectedBenefits, getSelectableBenefits } from "./queries";

export const Route = createFileRoute(
  "/selection/plan/$selection_plan_id/benefits"
)({
  component: () => <SelectionBenefits />,
  loader: async ({ params }) => {
    const [sel, config] = await Promise.all([
      getSelectedBenefits(params.selection_plan_id),
      getSelectableBenefits(params.selection_plan_id),
    ]);
    return { selection: sel, config: config };
  },
});

const SelectionBenefits = () => {
  //   const { selection_plan_id } = Route.useParams();
  const { selection, config } = useLoaderData({
    from: `/selection/plan/$selection_plan_id/benefits`,
  });

  return (
    <div>
      <AppPanel>
        <ul>
          {selection.map((benefit) => (
            <li key={benefit.selection_benefit_id}>
              {benefit.selection_benefit_id} {benefit.selection_value}
            </li>
          ))}
        </ul>
      </AppPanel>
    </div>
  );
};
