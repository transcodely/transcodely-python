"""Billing resource — an organization's invoices, read-only."""

from __future__ import annotations

from typing import Optional

from .._transport.transport import CallOptions, Transport
from ..pagination import Page, PageContents
from ..v1 import billing_pb2
from ._helpers import assign_pagination

_SERVICE = "transcodely.v1.BillingService"


class Billing:
    """An organization's billing statements.

    Unlike every other resource, billing settles a whole organization rather
    than a single app, so it is **not** available to API-key callers: a key is
    scoped to one app, and there is no app-scoped subset of an invoice worth
    serving. An API key gets a :class:`~transcodely.errors.PermissionError`.

    Reading invoices needs a dashboard session token for an organization
    **owner**, plus the organization the request is for::

        client = Transcodely(session_token, organization_id="org_f6g7h8i9j0")
        upcoming = client.billing.retrieve_upcoming()

    Invoices are generated automatically when a period closes. There is no API
    to create, edit, or delete one — a statement records what happened.

    Monetary amounts are integer minor units (cents) of the invoice currency:
    ``total_cents == 1250`` in EUR is 12.50 EUR.
    """

    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def list_invoices(
        self,
        *,
        limit: Optional[int] = None,
        opts: Optional[CallOptions] = None,
    ) -> Page[billing_pb2.Invoice]:
        """Page through finalized invoices, newest period first.

        Line items are omitted here — use :meth:`retrieve` for one invoice's
        breakdown. A statement still being generated for a just-ended period is
        never returned; for the period currently accruing use
        :meth:`retrieve_upcoming`.
        """

        def fetch(cursor: Optional[str]) -> PageContents[billing_pb2.Invoice]:
            req = billing_pb2.ListInvoicesRequest()
            assign_pagination(req.pagination, limit=limit, cursor=cursor)
            res = self._t.unary(
                _SERVICE, "ListInvoices", req, billing_pb2.ListInvoicesResponse(), opts
            )
            return PageContents(
                items=list(res.invoices),
                next_cursor=res.pagination.next_cursor or None,
            )

        return Page(fetch)

    def retrieve(self, invoice_id: str, opts: Optional[CallOptions] = None) -> billing_pb2.Invoice:
        """Retrieve one invoice by ID (``inv_*``), including its line items."""
        req = billing_pb2.GetInvoiceRequest(id=invoice_id)
        return self._t.unary(
            _SERVICE,
            "GetInvoice",
            req,
            billing_pb2.GetInvoiceResponse(),
            opts,
        ).invoice

    def retrieve_upcoming(self, opts: Optional[CallOptions] = None) -> billing_pb2.Invoice:
        """Retrieve the statement for the period currently accruing.

        Computed live from settled jobs rather than stored, so its ``id`` is
        empty, its status is ``draft``, and its totals move as jobs finish. Jobs
        still running are not included at any price — a job is billed only once
        it settles.
        """
        req = billing_pb2.GetUpcomingInvoiceRequest()
        return self._t.unary(
            _SERVICE,
            "GetUpcomingInvoice",
            req,
            billing_pb2.GetUpcomingInvoiceResponse(),
            opts,
        ).invoice
