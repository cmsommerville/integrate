export interface IAPIResponseSuccess<T> {
  status: "success";
  msg?: string;
  data: T;
}
export interface IAPIResponseError {
  status: "error";
  msg: string;
}

export type IAPIResponse = IAPIResponseSuccess | IAPIResponseError;

export interface ILabelValue {
  label: string;
  value: string | number;
}
