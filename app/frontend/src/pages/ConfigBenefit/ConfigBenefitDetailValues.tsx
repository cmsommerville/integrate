import { Fragment, useState, useMemo, useCallback, useEffect } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { authServerAxiosInstance } from "@/services/axios";
import { ConfigBenefitAuth, ConfigBenefit } from "./types";
import { AuthRole } from "@/types/auth";
import AppMultiselect from "@/components/AppMultiselect";

interface Props {
  benefit_auth: Partial<ConfigBenefitAuth>;
  benefit: Partial<ConfigBenefit>;
  open: boolean;
  onClose: () => void;
  onSave: (benefitDetail: Partial<ConfigBenefitAuth>) => void;
}

const ConfigBenefitDetailValues = ({
  benefit_auth,
  benefit,
  open,
  onClose,
  onSave,
}: Props) => {
  const [isDirty, setIsDirty] = useState(false);
  const [benefitDetail, setBenefitDetail] = useState<
    Partial<ConfigBenefitAuth>
  >({});
  const [authRoles, setAuthRoles] = useState<AuthRole[]>([]);

  const _onClose = () => {
    setBenefitDetail({});
    onClose();
  };

  const _onSave = () => {
    if (benefitDetail) {
      onSave(benefitDetail);
    }
    setBenefitDetail({});
    onClose();
  };
  useEffect(() => {
    const controller = new AbortController();
    const signal = controller.signal;

    authServerAxiosInstance
      .get(`/roles`, { signal })
      .then((res) => {
        setAuthRoles(res.data);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.log(err.name);
        }
      });

    return () => {
      controller.abort();
    };
  }, []);

  useEffect(() => {
    if (benefit_auth) {
      setBenefitDetail({ ...benefit_auth });
      return;
    }
  }, [benefit_auth]);

  const defaultRoles = useMemo(() => {
    if (!benefitDetail) return [];
    if (!benefitDetail.acl) return [];
    if (!authRoles) return [];
    if (!authRoles.length) return [];
    const permitted_roles = benefitDetail.acl.map(
      (item) => item.auth_role_code
    );
    return authRoles.filter((r) => permitted_roles.includes(r.auth_role_code));
  }, [benefitDetail, authRoles]);

  const setter = useCallback(
    (key: keyof ConfigBenefitAuth, val: any) => {
      setBenefitDetail((old) => {
        return { ...old, [key]: val };
      });
      setIsDirty(true);
    },
    [setBenefitDetail]
  );

  const frontIcon = benefit.unit_type?.ref_attr_symbol === "$" ? "$" : null;
  const rearIcon =
    benefit.unit_type?.ref_attr_symbol === "$"
      ? "USD"
      : benefit.unit_type?.ref_attr_symbol === "%"
      ? "%"
      : null;

  return (
    <Transition.Root show={open} as={Fragment}>
      <Dialog as="div" className="relative z-10" onClose={_onClose}>
        <Transition.Child
          as={Fragment}
          enter="ease-in-out duration-500"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in-out duration-500"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>

        <div className="fixed inset-0 overflow-hidden">
          <div className="absolute inset-0 overflow-hidden">
            <div className="pointer-events-none fixed inset-y-0 right-0 flex max-w-full pl-10 sm:pl-16">
              <Transition.Child
                as={Fragment}
                enter="transform transition ease-in-out duration-500 sm:duration-700"
                enterFrom="translate-x-full"
                enterTo="translate-x-0"
                leave="transform transition ease-in-out duration-500 sm:duration-700"
                leaveFrom="translate-x-0"
                leaveTo="translate-x-full"
              >
                <Dialog.Panel className="pointer-events-auto w-screen max-w-md">
                  <form className="flex h-full flex-col divide-y divide-gray-200 bg-white shadow-xl">
                    <div className="h-0 flex-1 overflow-y-auto divide-y">
                      <div className="bg-gray-100 py-6 px-4 sm:px-6">
                        <div className="flex items-center justify-between">
                          <Dialog.Title className="text-lg font-medium">
                            Benefit Values
                          </Dialog.Title>
                          <div className="ml-3 flex h-7 items-center">
                            <button
                              type="button"
                              className="rounded-md text-gray-400 transition duration-100 hover:text-primary-600"
                              onClick={_onClose}
                            >
                              <span className="sr-only">Close panel</span>
                              <XMarkIcon
                                className="h-6 w-6"
                                aria-hidden="true"
                              />
                            </button>
                          </div>
                        </div>
                        <div className="mt-1">
                          <p className="text-sm text-gray-400">
                            Select which user roles have access to these benefit
                            values. Then fill in the default, min, max, and step
                            values.
                          </p>
                        </div>
                      </div>
                      <div className="px-4 py-8 space-y-1">
                        <AppMultiselect
                          group="role"
                          label="Permitted Roles"
                          items={authRoles}
                          selected={defaultRoles}
                          itemId="auth_role_id"
                          itemLabel="auth_role_label"
                          onChange={(items) => {
                            setter(
                              "acl",
                              items.map((i) => ({
                                auth_role_code: i.auth_role_code,
                              }))
                            );
                          }}
                        />
                        <p className="text-sm text-gray-400">
                          Which roles will be able to use these benefit values?
                        </p>
                      </div>
                      <div className="flex flex-1 flex-col justify-between">
                        <div className="space-y-6 px-4 pt-6 pb-5">
                          <div>
                            <label
                              htmlFor="default_value"
                              className="block text-sm font-medium text-gray-700"
                            >
                              Default Value
                            </label>
                            <div className="relative mt-1 rounded-md shadow-sm">
                              {frontIcon ? (
                                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                  <span className="text-gray-500 sm:text-sm">
                                    {frontIcon}
                                  </span>
                                </div>
                              ) : null}
                              <input
                                type="number"
                                name="default_value"
                                id="default_value"
                                className="block w-full rounded-md border-gray-300 pr-12 focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                                placeholder="1000"
                                onChange={(e) =>
                                  setter(
                                    "default_value",
                                    Number(e.target.value)
                                  )
                                }
                                value={benefitDetail?.default_value ?? ""}
                              />
                              {rearIcon ? (
                                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                                  <span
                                    className="text-gray-500 sm:text-sm"
                                    id="price-percent"
                                  >
                                    {rearIcon}
                                  </span>
                                </div>
                              ) : null}
                            </div>
                          </div>
                          <div>
                            <label
                              htmlFor="min_value"
                              className="block text-sm font-medium text-gray-700"
                            >
                              Min Value
                            </label>
                            <div className="relative mt-1 rounded-md shadow-sm">
                              {frontIcon ? (
                                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                  <span className="text-gray-500 sm:text-sm">
                                    {frontIcon}
                                  </span>
                                </div>
                              ) : null}
                              <input
                                type="number"
                                name="min_value"
                                id="min_value"
                                className="block w-full rounded-md border-gray-300 pr-12 focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                                placeholder="0"
                                onChange={(e) =>
                                  setter("min_value", Number(e.target.value))
                                }
                                value={benefitDetail?.min_value ?? ""}
                              />
                              {rearIcon ? (
                                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                                  <span
                                    className="text-gray-500 sm:text-sm"
                                    id="price-percent"
                                  >
                                    {rearIcon}
                                  </span>
                                </div>
                              ) : null}
                            </div>
                          </div>
                          <div>
                            <label
                              htmlFor="max_value"
                              className="block text-sm font-medium text-gray-700"
                            >
                              Max Value
                            </label>
                            <div className="relative mt-1 rounded-md shadow-sm">
                              {frontIcon ? (
                                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                  <span className="text-gray-500 sm:text-sm">
                                    {frontIcon}
                                  </span>
                                </div>
                              ) : null}
                              <input
                                type="number"
                                name="max_value"
                                id="max_value"
                                className="block w-full rounded-md border-gray-300 pr-12 focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                                placeholder="5000"
                                onChange={(e) =>
                                  setter("max_value", Number(e.target.value))
                                }
                                value={benefitDetail?.max_value ?? ""}
                              />
                              {rearIcon ? (
                                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                                  <span
                                    className="text-gray-500 sm:text-sm"
                                    id="price-percent"
                                  >
                                    {rearIcon}
                                  </span>
                                </div>
                              ) : null}
                            </div>
                          </div>
                          <div>
                            <label
                              htmlFor="step_value"
                              className="block text-sm font-medium text-gray-700"
                            >
                              Step Value
                            </label>
                            <div className="relative mt-1 rounded-md shadow-sm">
                              {frontIcon ? (
                                <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
                                  <span className="text-gray-500 sm:text-sm">
                                    {frontIcon}
                                  </span>
                                </div>
                              ) : null}
                              <input
                                type="number"
                                name="step_value"
                                id="step_value"
                                className="block w-full rounded-md border-gray-300 pr-12 focus:border-primary-500 focus:ring-primary-500 sm:text-sm"
                                placeholder="0"
                                onChange={(e) =>
                                  setter("step_value", Number(e.target.value))
                                }
                                value={benefitDetail?.step_value ?? ""}
                              />
                              {rearIcon ? (
                                <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
                                  <span
                                    className="text-gray-500 sm:text-sm"
                                    id="price-percent"
                                  >
                                    {rearIcon}
                                  </span>
                                </div>
                              ) : null}
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="flex flex-shrink-0 justify-end px-4 py-4">
                      <button
                        type="button"
                        className="rounded-md border border-gray-300 bg-white py-2 px-4 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                        onClick={_onClose}
                      >
                        Cancel
                      </button>
                      <button
                        type="button"
                        onClick={_onSave}
                        className="ml-4 inline-flex justify-center rounded-md border border-transparent bg-primary-600 py-2 px-4 text-sm font-medium text-white shadow-sm hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
                      >
                        Save
                      </button>
                    </div>
                  </form>
                </Dialog.Panel>
              </Transition.Child>
            </div>
          </div>
        </div>
      </Dialog>
    </Transition.Root>
  );
};

export default ConfigBenefitDetailValues;
