import {FormattedMessage} from 'react-intl';

import Modal from '@/components/modals/Modal';

export interface AddKitModalProps {
  isOpen: boolean;
  onRequestClose: () => void;
  children: React.ReactNode;
  formId?: string;
}

const AddKitModal: React.FC<AddKitModalProps> = ({isOpen, onRequestClose, formId, children}) => (
  <Modal
    isOpen={isOpen}
    onRequestClose={onRequestClose}
    title={
      <FormattedMessage
        description="Create kit modal title"
        defaultMessage="Add new kit to the database"
      />
    }
  >
    <p>
      <FormattedMessage
        description="Create kit modal subheading"
        defaultMessage="Please, only add new kits if they were not available via the search function."
      />
    </p>
    <div className="container-fluid">{children}</div>
    <div className="modal__footer modal__footer--reverse">
      <button type="submit" className="btn bg-main-blue" form={formId}>
        <FormattedMessage description="Save form button" defaultMessage="Save" />
      </button>
      <button type="button" className="btn bg-main-grey" onClick={onRequestClose}>
        <FormattedMessage description="Modal close button" defaultMessage="Close" />
      </button>
    </div>
  </Modal>
);

export default AddKitModal;
