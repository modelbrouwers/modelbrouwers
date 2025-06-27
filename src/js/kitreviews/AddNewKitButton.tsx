import {useState} from 'react';
import {createPortal} from 'react-dom';
import {FormattedMessage} from 'react-intl';

import FAIcon from '@/components/FAIcon.js';
import {CreateKitResponseData} from '@/data/kits/modelkit';
import AddKitModal from '@/kits/AddKitModal';

import KitReviewKitAdd from './KitreviewKitAdd';

const FORM_ID = 'add-kit-form';

export interface AddNewKitButtonProps {
  modalNode?: HTMLElement;
  onKitAdded: (kit: CreateKitResponseData) => void;
}

const AddNewKitButton: React.FC<AddNewKitButtonProps> = ({modalNode, onKitAdded}) => {
  const [modalOpen, setModalOpen] = useState<boolean>(false);

  const modal = (
    <AddKitModal isOpen={modalOpen} onRequestClose={() => setModalOpen(false)} formId={FORM_ID}>
      <KitReviewKitAdd onKitAdded={onKitAdded} formId={FORM_ID} />
    </AddKitModal>
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
