import { useState, useEffect } from "react";
import MainLayout from "./layouts/MainLayout";
import { AppSelect, IAppSelectOption } from "./components/Form";

interface ICensusSet {
  selection_census_set_id: number;
  selection_census_description: string;
  selection_plan_id: number;
  selection_census_filepath?: string | null | undefined;
}

const App = () => {
  const [optionsCensusSet, setOptionsCensusSet] = useState<
    { id: number; label: string }[]
  >([]);
  const [selectedCensusSet, setSelectedCensusSet] = useState<
    number | undefined
  >();

  useEffect(() => {
    fetch("/api/dd/selection/census-set/1")
      .then((res) => res.json())
      .then((res) =>
        setOptionsCensusSet(
          res.map((item: ICensusSet) => {
            return {
              id: item.selection_census_set_id,
              label: item.selection_census_description,
            };
          })
        )
      );
  }, []);

  const onSelectCensusSet = (val: number) => {
    fetch("/api/crud/selection/plan/1", {
      method: "PATCH",
      body: JSON.stringify({
        selection_census_set_id: val,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(() => {
        return fetch("/api/crud/selection/rate-table/1", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });
      })
      .then((res) => res.json())
      .then((res) => console.log(res));
  };

  return (
    <MainLayout>
      <div className="grid grid-cols-3 gap-8">
        <AppSelect
          options={optionsCensusSet}
          selected={optionsCensusSet[0]}
          onChange={(opt: IAppSelectOption) => console.log(opt)}
        >
          Census Set
        </AppSelect>
      </div>
    </MainLayout>
  );
};

export default App;
