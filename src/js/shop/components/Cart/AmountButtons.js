import PropTypes from 'prop-types';
import React from 'react';
import {useIntl} from 'react-intl';

import FAIcon from '../../../components/FAIcon';

const BaseButton = ({icon, onClick, ...props}) => (
  <button type="button" className="button button--blue" onClick={onClick} {...props}>
    <FAIcon icon={icon} />
  </button>
);

BaseButton.propTypes = {
  icon: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
};

const IncrementButton = ({onClick, ...props}) => {
  const intl = useIntl();
  const label = intl.formatMessage({
    description: 'Increment button accessible label',
    defaultMessage: 'Add one',
  });
  return <BaseButton icon="plus" onClick={onClick} aria-label={label} {...props} />;
};

IncrementButton.propTypes = {
  onClick: PropTypes.func.isRequired,
};

const DecrementButton = ({onClick, ...props}) => {
  const intl = useIntl();
  const label = intl.formatMessage({
    description: 'Decrement button accessible label',
    defaultMessage: 'Remove one',
  });
  return <BaseButton icon="minus" onClick={onClick} aria-label={label} {...props} />;
};

DecrementButton.propTypes = {
  onClick: PropTypes.func.isRequired,
};

export {IncrementButton, DecrementButton};
