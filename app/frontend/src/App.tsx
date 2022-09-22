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
  const [rates, setRates] = useState<any>([]);

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
    setRates([]);
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
      .then((res) => setRates(res));
  };

  return (
    <MainLayout>
      <div className="grid grid-cols-3 gap-8">
        <AppSelect
          options={optionsCensusSet}
          selected={optionsCensusSet[0]}
          onChange={(opt: IAppSelectOption) =>
            onSelectCensusSet(Number(opt.id))
          }
        >
          Census Set
        </AppSelect>
      </div>
      <div className="mt-8 flex flex-col">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table className="min-w-full divide-y divide-gray-300">
                <thead className="bg-gray-50">
                  <tr>
                    <th
                      scope="col"
                      className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6"
                    >
                      ID
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
                    >
                      Age Band
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
                    >
                      Gender
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
                    >
                      Smoker Status
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
                    >
                      Relationship
                    </th>
                    <th
                      scope="col"
                      className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
                    >
                      Annual Rate
                    </th>
                    <th
                      scope="col"
                      className="relative py-3.5 pl-3 pr-4 sm:pr-6"
                    >
                      <span className="sr-only">Edit</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {rates.map((rate: any) => (
                    <tr key={rate.email}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                        {rate.selection_rate_table_id}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {rate.age_band.lower_age_value} -{" "}
                        {rate.age_band.upper_age_value}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {rate.gender.config_attr_detail_label}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {rate.smoker_status.config_attr_detail_label}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {rate.relationship.config_attr_detail_label}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                        {rate.annual_rate}
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                        <a
                          href="#"
                          className="text-indigo-600 hover:text-indigo-900"
                        >
                          Edit<span className="sr-only">, {rate.name}</span>
                        </a>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </MainLayout>
  );
};

export default App;
