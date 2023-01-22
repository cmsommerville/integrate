import { Fragment, useState, useMemo, useCallback, useEffect } from "react";
import { Dialog, Transition } from "@headlessui/react";
import { XMarkIcon } from "@heroicons/react/24/outline";
import { authServerAxiosInstance } from "@/services/axios";
import { ConfigBenefitAuth } from "./types";
import { AuthRole } from "@/types/auth";
import AppMultiselect from "@/components/AppMultiselect";

interface Props {
  benefit_auth?: ConfigBenefitAuth;
  open: boolean;
  onClose: () => void;
  onSave: (benefitDetail: ConfigBenefitAuth) => void;
}

const ConfigBenefitDetailValues = ({
  benefit_auth,
  open,
  onClose,
  onSave,
}: Props) => {
  const [isDirty, setIsDirty] = useState(false);
  const [benefitDetail, setBenefitDetail] = useState<ConfigBenefitAuth>({});
  const [authRoles, setAuthRoles] = useState<AuthRole[]>([]);

  const _onClose = () => {
    setBenefitDetail({});
    onClose();
  };

  const _onSave = () => {
    onSave(benefitDetail);
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
      setBenefitDetail((old) => ({ ...old, [key]: val }));
      setIsDirty(true);
    },
    [setBenefitDetail]
  );
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
                    <div className="h-0 flex-1 overflow-y-auto">
                      <div className="bg-primary-700 py-6 px-4 sm:px-6">
                        <div className="flex items-center justify-between">
                          <Dialog.Title className="text-lg font-medium text-white">
                            Benefit Values
                          </Dialog.Title>
                          <div className="ml-3 flex h-7 items-center">
                            <button
                              type="button"
                              className="rounded-md bg-primary-700 text-primary-200 hover:text-white focus:outline-none focus:ring-2 focus:ring-white"
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
                          <p className="text-sm text-primary-300">
                            Select which user roles have access to these benefit
                            values. Then fill in the default, min, max, and step
                            values.
                          </p>
                        </div>
                      </div>
                      <div className="flex flex-1 flex-col justify-between">
                        <div className="divide-y divide-gray-200 px-4 sm:px-6">
                          <div className="space-y-6 pt-6 pb-5">
                            <div className="pb-8 mb-6 border-b-2 border-b-gray-200 space-y-1">
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
                                Which roles will be able to use these benefit
                                values?
                              </p>
                            </div>
                            <div>
                              <label
                                htmlFor="default_value"
                                className="block text-sm font-medium text-gray-700"
                              >
                                Default Value
                              </label>
                              <div className="mt-1">
                                <input
                                  type="number"
                                  name="default_value"
                                  id="default_value"
                                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm placeholder:text-gray-400"
                                  placeholder="1000"
                                  onChange={(e) =>
                                    setter(
                                      "default_value",
                                      Number(e.target.value)
                                    )
                                  }
                                  value={benefitDetail?.default_value ?? ""}
                                />
                              </div>
                            </div>
                            <div>
                              <label
                                htmlFor="min_value"
                                className="block text-sm font-medium text-gray-700"
                              >
                                Min Value
                              </label>
                              <div className="mt-1">
                                <input
                                  type="number"
                                  name="min_value"
                                  id="min_value"
                                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm placeholder:text-gray-400"
                                  placeholder="0"
                                  onChange={(e) =>
                                    setter("min_value", Number(e.target.value))
                                  }
                                  value={benefitDetail?.min_value ?? ""}
                                />
                              </div>
                            </div>
                            <div>
                              <label
                                htmlFor="max_value"
                                className="block text-sm font-medium text-gray-700"
                              >
                                Max Value
                              </label>
                              <div className="mt-1">
                                <input
                                  type="number"
                                  name="max_value"
                                  id="max_value"
                                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm placeholder:text-gray-400"
                                  placeholder="5000"
                                  onChange={(e) =>
                                    setter("max_value", Number(e.target.value))
                                  }
                                  value={benefitDetail?.max_value ?? ""}
                                />
                              </div>
                            </div>
                            <div>
                              <label
                                htmlFor="step_value"
                                className="block text-sm font-medium text-gray-700"
                              >
                                Step Value
                              </label>
                              <div className="mt-1">
                                <input
                                  type="number"
                                  name="step_value"
                                  id="step_value"
                                  className="block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm placeholder:text-gray-400"
                                  placeholder="0"
                                  onChange={(e) =>
                                    setter("step_value", Number(e.target.value))
                                  }
                                  value={benefitDetail?.step_value ?? ""}
                                />
                              </div>
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
