import clsx from 'clsx';
import {NavLink as RRNavLink} from 'react-router';

import FAIcon from '@/components/FAIcon.js';

export interface NavLinkProps extends React.ComponentProps<typeof RRNavLink> {
  isEnabled?: boolean;
  hasErrors?: boolean;
  children: React.ReactNode;
}

const NavLink: React.FC<NavLinkProps> = ({
  isEnabled = false,
  hasErrors = false,
  children,
  ...props
}) => {
  // wrap to display error icon in nav if there are known errors
  if (hasErrors) {
    children = (
      <span className="nav-link-wrapper">
        <span className="nav-link-wrapper__text">{children}</span>
        <span className="nav-link-wrapper__icon">
          <FAIcon icon="exclamation-circle" />
        </span>
      </span>
    );
  }

  const getClassName: NavLinkProps['className'] = ({isActive}) =>
    clsx('navigation__link', {
      'navigation__link--enabled': isEnabled,
      'navigation__link--active': isActive,
    });

  if (!isEnabled) {
    return (
      <span className={getClassName({isActive: false, isPending: false, isTransitioning: false})}>
        {children}
      </span>
    );
  }

  return (
    <RRNavLink className={getClassName} {...props}>
      {children}
    </RRNavLink>
  );
};

export default NavLink;
