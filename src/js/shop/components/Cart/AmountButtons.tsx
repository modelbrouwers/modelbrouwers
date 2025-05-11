import {useIntl} from 'react-intl';

import FAIcon from '../../../components/FAIcon';

export interface BaseButtonProps extends React.ComponentProps<'button'> {
  icon: string;
  onClick: (event: React.MouseEvent<HTMLButtonElement>) => void;
}

const BaseButton: React.FC<BaseButtonProps> = ({icon, onClick, ...props}) => (
  <button type="button" className="button button--blue" onClick={onClick} {...props}>
    <FAIcon icon={icon} />
  </button>
);

const IncrementButton: React.FC<Omit<BaseButtonProps, 'icon'>> = ({onClick, ...props}) => {
  const intl = useIntl();
  const label = intl.formatMessage({
    description: 'Increment button accessible label',
    defaultMessage: 'Add one',
  });
  return <BaseButton icon="plus" onClick={onClick} aria-label={label} {...props} />;
};

const DecrementButton: React.FC<Omit<BaseButtonProps, 'icon'>> = ({onClick, ...props}) => {
  const intl = useIntl();
  const label = intl.formatMessage({
    description: 'Decrement button accessible label',
    defaultMessage: 'Remove one',
  });
  return <BaseButton icon="minus" onClick={onClick} aria-label={label} {...props} />;
};

export {IncrementButton, DecrementButton};
