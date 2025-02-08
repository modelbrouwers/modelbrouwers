import camelCase from "lodash/camelCase";
import isObject from "lodash/isObject";

// Temporary solution - we should use drf-camelcase-renderer to the backend later.
export const camelize = (obj) => {
  // recurse into arrays
  if (Array.isArray(obj)) {
    return obj.map(camelize);
  }

  if (!isObject(obj)) {
    return obj;
  }

  // convert keys to camelCase
  const newObj = {};
  Object.entries(obj).forEach(([key, value]) => {
    const newKey = camelCase(key);
    const newValue = camelize(value);
    newObj[newKey] = newValue;
  });

  return newObj;
};
