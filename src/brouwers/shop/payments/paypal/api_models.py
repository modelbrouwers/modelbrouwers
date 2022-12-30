from typing import List, Literal

from pydantic import BaseModel


class Link(BaseModel):
    href: str
    rel: str
    method: Literal["GET", "POST", "PATCH", "PUT", "DELETE"]


class PaypalOrder(BaseModel):
    id: str
    status: Literal[
        "CREATED", "SAVED", "APPROVED", "VOIDED", "COMPLETED", "PAYER_ACTION_REQUIRED"
    ]
    links: List[Link]

    def get_redirect_url(self) -> str:
        assert self.status == "PAYER_ACTION_REQUIRED"
        relevant_link = next(link for link in self.links if link.rel == "payer-action")
        return relevant_link.href

    def get_capture_url(self):
        assert self.status == "APPROVED"
        relevant_link = next(link for link in self.links if link.rel == "capture")
        return relevant_link.href
