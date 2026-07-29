"""Tests for the Billing resource and the organization header it needs.

Billing is organization-scoped: the server rejects API-key callers outright and
requires ``X-Organization-ID`` from a dashboard session token, so the header
plumbing is part of the resource's contract rather than an optional extra.
"""

from __future__ import annotations

from typing import Any, Callable, Optional, Union

import httpx

from transcodely._transport.transport import Transport
from transcodely.resources.billing import Billing
from transcodely.v1 import billing_pb2, common_pb2


class FakeTransport:
    """Duck-typed stand-in for Transport that returns canned responses per method."""

    def __init__(self, responses: dict[str, Union[Any, Callable[[Any], Any]]]) -> None:
        self._responses = responses
        self.calls: list[tuple[str, Any]] = []

    def unary(
        self,
        service_name: str,
        method_name: str,
        request: Any,
        response: Any,
        opts: Optional[Any] = None,
    ) -> Any:
        self.calls.append((method_name, request))
        r = self._responses[method_name]
        return r(request) if callable(r) else r


class TestListInvoices:
    def test_limit_passes_through(self) -> None:
        resp = billing_pb2.ListInvoicesResponse(
            invoices=[billing_pb2.Invoice(id="inv_1")],
            pagination=common_pb2.PaginationResponse(next_cursor=""),
        )
        t = FakeTransport({"ListInvoices": resp})
        Billing(t).list_invoices(limit=20).items  # type: ignore[arg-type]
        method, req = t.calls[0]
        assert method == "ListInvoices"
        assert req.pagination.limit == 20

    def test_auto_paging_forwards_cursor(self) -> None:
        page1 = billing_pb2.ListInvoicesResponse(
            invoices=[billing_pb2.Invoice(id="inv_1"), billing_pb2.Invoice(id="inv_2")],
            pagination=common_pb2.PaginationResponse(next_cursor="c1"),
        )
        page2 = billing_pb2.ListInvoicesResponse(
            invoices=[billing_pb2.Invoice(id="inv_3")],
            pagination=common_pb2.PaginationResponse(next_cursor=""),
        )
        t = FakeTransport(
            {"ListInvoices": lambda req: page2 if req.pagination.cursor == "c1" else page1}
        )
        page = Billing(t).list_invoices()  # type: ignore[arg-type]
        assert [i.id for i in page.auto_paging_iter()] == ["inv_1", "inv_2", "inv_3"]
        assert t.calls[1][1].pagination.cursor == "c1"


class TestRetrieveInvoice:
    def test_forwards_id_and_returns_line_items(self) -> None:
        invoice = billing_pb2.Invoice(
            id="inv_a1b2c3d4e5f6",
            object="invoice",
            status=billing_pb2.INVOICE_STATUS_OPEN,
            currency="EUR",
            subtotal_cents=1300,
            total_cents=1250,
            line_items=[
                billing_pb2.InvoiceLineItem(
                    id="li_x",
                    line_type=billing_pb2.INVOICE_LINE_TYPE_USAGE,
                    description="Encoding — h264 1080p standard",
                    amount_cents=1300,
                    dimensions={"app_id": "app_k1l2m3n4o5", "codec": "h264"},
                ),
                billing_pb2.InvoiceLineItem(
                    id="li_y",
                    line_type=billing_pb2.INVOICE_LINE_TYPE_ADJUSTMENT,
                    amount_cents=-50,
                ),
            ],
        )
        t = FakeTransport({"GetInvoice": billing_pb2.GetInvoiceResponse(invoice=invoice)})
        got = Billing(t).retrieve("inv_a1b2c3d4e5f6")  # type: ignore[arg-type]

        method, req = t.calls[0]
        assert method == "GetInvoice"
        assert req.id == "inv_a1b2c3d4e5f6"
        assert got.total_cents == 1250
        assert len(got.line_items) == 2
        assert dict(got.line_items[0].dimensions) == {
            "app_id": "app_k1l2m3n4o5",
            "codec": "h264",
        }
        # The adjustment line is signed and routinely negative.
        assert got.line_items[1].amount_cents == -50


class TestRetrieveUpcoming:
    def test_computed_statement_has_no_id_and_is_draft(self) -> None:
        upcoming = billing_pb2.Invoice(status=billing_pb2.INVOICE_STATUS_DRAFT, total_cents=400)
        t = FakeTransport(
            {"GetUpcomingInvoice": billing_pb2.GetUpcomingInvoiceResponse(invoice=upcoming)}
        )
        got = Billing(t).retrieve_upcoming()  # type: ignore[arg-type]

        assert t.calls[0][0] == "GetUpcomingInvoice"
        assert got.id == ""
        assert got.status == billing_pb2.INVOICE_STATUS_DRAFT


class TestOrganizationHeader:
    """The header goes out on the real request, not just into a builder."""

    def _request_headers(self, **kwargs: Any) -> httpx.Headers:
        captured: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(200, json={"invoice": {}})

        http_client = httpx.Client(transport=httpx.MockTransport(handler))
        with Transport(
            "tk_test", base_url="https://example.invalid", http_client=http_client, **kwargs
        ) as transport:
            Billing(transport).retrieve_upcoming()
        return captured[0].headers

    def test_sent_when_organization_id_is_configured(self) -> None:
        headers = self._request_headers(organization_id="org_f6g7h8i9j0")
        assert headers["x-organization-id"] == "org_f6g7h8i9j0"

    def test_absent_when_no_organization_id(self) -> None:
        # Absent, not empty: a blank header would read as a supplied-but-empty
        # organization on the server rather than as "none given".
        assert "x-organization-id" not in self._request_headers()
