from typing import Dict, List, Literal

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

    @property
    def parsed_links(self) -> Dict[str, Link]:
        return {link.rel: link for link in self.links}

    def get_redirect_url(self) -> str:
        assert self.status == "PAYER_ACTION_REQUIRED"
        return self.parsed_links["payer-action"].href

    def get_capture_url(self):
        assert self.status == "APPROVED"
        return self.parsed_links["capture"].href
