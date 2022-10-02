import _ from 'lodash'

/**
 * This method pivots an array of objects. 
 * 
 * @param data an array of objects
 * @param index an array of keys which are "grouped by"
 * @param column the key containing the categories which are pivoted to separate columns. Currently only one pivot column is supported.
 * @param value the value which is placed in the pivoted columns
 * @returns an array of objects with the pivoted columns as new keys
 */
export const pivot = (data: any, index: string[], column: string, value: string) => {
  const _data = data.reduce((prev: Object, row: any) => {
    const key = _.pick(row, index);
    const joined_key = Object.values(key).join("#") as keyof typeof prev;

    if (prev[joined_key]) {
      Object.assign(prev[joined_key], {
        [_.get(row, column)]: _.get(row, value),
      });
    } else {
      Object.assign(prev, {
        [joined_key]: {
          ...key,
          [_.get(row, column)]: _.get(row, value),
        },
      });
    }
    return prev;
  }, {});
  return Object.values(_data);
};
