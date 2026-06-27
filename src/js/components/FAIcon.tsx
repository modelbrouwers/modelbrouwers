import React from 'react';

export interface FAIconProps {
  icon: string;
  extra?: string[];
}

const FAIcon: React.FC<FAIconProps> = ({icon, extra = []}) => {
  const classNames = ['fa', `fa-${icon}`, ...extra];
  return <i className={classNames.join(' ')} aria-hidden="true" />;
};

export default FAIcon;
