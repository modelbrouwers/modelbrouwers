import PropTypes from 'prop-types';
import React from 'react';

import {Label} from './Label';

const FormField = ({
  htmlId,
  label,
  required = false,
  labelGrid = 'col-sm-4',
  fieldGrid = 'col-sm-8',
  children,
}) => {
  return (
    <div className="form-group clearfix">
      <Label label={label} htmlId={htmlId} required={required} labelGrid={labelGrid} />
      <div className={fieldGrid}>{children}</div>
    </div>
  );
};

FormField.propTypes = {
  htmlId: PropTypes.string.isRequired,
  label: PropTypes.string.isRequired,
  required: PropTypes.bool,
  labelGrid: PropTypes.string,
  fieldGrid: PropTypes.string,
};

export {FormField};
