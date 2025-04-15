import {FormattedMessage} from 'react-intl';
import {Link} from 'react-router-dom';

const LOGIN_URL = '/login/';
const SIGNUP_URL = '/regiser/';

export interface AccountProps {
  nextAfterLogin: string extends '' ? never : string;
}

const Account: React.FC<AccountProps> = ({nextAfterLogin}) => {
  return (
    <>
      <div className="layout layout--columns">
        <div className="layout__column layout__column--center">
          <Link
            to="/address"
            className="button button--vertical-center button--large button--icon button--blue"
          >
            <i className="fa fa-user-secret fa-2x" />
            <FormattedMessage
              description="Checkout with account link"
              defaultMessage="Continue without signup"
            />
          </Link>
        </div>

        <div className="layout__separator layout__separator--vertical"></div>

        <div className="layout__column layout__column--center">
          <div className="layout layout--rows">
            <div className="layout__row">
              <a
                href={`${LOGIN_URL}?next=${nextAfterLogin}`}
                className="button button--blue button--large button--icon button--vertical-center"
              >
                <i className="fa fa-sign-in" />
                <FormattedMessage description="Checkout with login" defaultMessage="Sign in" />
              </a>
            </div>

            <div className="layout__separator layout__separator--horizontal">
              <FormattedMessage
                description="'Or' (Separator between options)"
                defaultMessage="or"
              />
            </div>

            <div className="layout__row">
              <a
                href={`${SIGNUP_URL}?next=${nextAfterLogin}&from=checkout`}
                className="button button--plain button--large button--icon button--vertical-center"
              >
                <i className="fa fa-user-plus" />
                <FormattedMessage
                  description="Checkout with account creation"
                  defaultMessage="Sign up"
                />
              </a>
            </div>
          </div>
        </div>
      </div>

      <div className="message message--info">
        <i className="fa fa-fw fa-info-circle" />
        <FormattedMessage
          description="Checkout account options description"
          defaultMessage="Please select how you'd like to continue. No account is required for checkout, but if you do have or create one, we can fill out your details for you (in the future)."
        />
      </div>
    </>
  );
};

export default Account;
