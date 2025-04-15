import clsx from 'clsx';

export interface LoaderProps {
  center?: boolean;
  size?: 4 | 2 | 1;
}

/**
 * Note - where you use this loader, you need to emit the accessible role and aria-live,
 * see https://codeburst.io/how-to-create-a-simple-css-loading-spinner-make-it-accessible-e5c83c2e464c
 */
const Loader: React.FC<LoaderProps> = ({center, size = 4}) => {
  return (
    <div className={clsx('loader', {'loader--centered': center})}>
      <span className="sr-only">Loading...</span>
      <i
        className={clsx('loader__spinner', 'fa', 'fa-pulse', 'fa-spinner', `fa-${size}x`)}
        aria-hidden="true"
      />
    </div>
  );
};

export default Loader;
