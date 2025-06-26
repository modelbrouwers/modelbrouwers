import {useState} from 'react';
import {createPortal} from 'react-dom';
import {FormattedMessage} from 'react-intl';

import FAIcon from '@/components/FAIcon.js';
import Modal from '@/components/modals/Modal';
import {CreateKitResponseData} from '@/data/kits/modelkit';

import KitReviewKitAdd from './KitreviewKitAdd';

const FORM_ID = 'add-kit-form';

export interface AddNewKitButtonProps {
  modalNode?: HTMLElement;
  onKitAdded: (kit: CreateKitResponseData) => void;
}

const AddNewKitButton: React.FC<AddNewKitButtonProps> = ({modalNode, onKitAdded}) => {
  const [modalOpen, setModalOpen] = useState<boolean>(false);

  const modal = (
    <Modal
      isOpen={modalOpen}
      onRequestClose={() => setModalOpen(false)}
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
      <div className="container-fluid">
        <KitReviewKitAdd onKitAdded={onKitAdded} formId={FORM_ID} />
      </div>
      <div className="modal__footer modal__footer--reverse">
        <button type="submit" className="btn bg-main-blue" form={FORM_ID}>
          <FormattedMessage description="Save form button" defaultMessage="Save" />
        </button>
        <button type="button" className="btn bg-main-grey" onClick={() => setModalOpen(false)}>
          <FormattedMessage description="Modal close button" defaultMessage="Close" />
        </button>
      </div>
    </Modal>
  );

  return (
    <>
      <button
        type="button"
        className="button button--icon button--orange"
        onClick={() => setModalOpen(true)}
      >
        <FAIcon icon="plus" />
        <FormattedMessage description="Add new kit button label" defaultMessage="Add new kit" />
      </button>
      {modalNode ? createPortal(modal, modalNode) : modal}
    </>
  );
};

export default AddNewKitButton;
