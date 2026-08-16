"""Tests for the Billing resource and the organization header it needs.

Billing is organization-scoped: the server rejects API-key callers outright and
requires ``X-Organization-ID`` from a dashboard session token, so the header
plumbing is part of the resource's contract rather than an optional extra.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import httpx

from transcodely._transport.transport import Transport
from transcodely.resources.billing import Billing
from transcodely.v1 import billing_pb2, common_pb2


class FakeTransport:
    """Duck-typed stand-in for Transport that returns canned responses per method."""

    def __init__(self, responses: dict[str, Any | Callable[[Any], Any]]) -> None:
        self._responses = responses
        self.calls: list[tuple[str, Any]] = []

    def unary(
        self,
        service_name: str,
        method_name: str,
        request: Any,
        response: Any,
        opts: Any | None = None,
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
        _ = Billing(t).list_invoices(limit=20).items  # type: ignore[arg-type]
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


class TestRetrieveProfile:
    def test_on_file_for_a_card_the_provider_will_not_describe(self) -> None:
        # A method with no card metadata is still chargeable: the state is the
        # signal, not the digits.
        profile = billing_pb2.BillingProfile(
            object="billing_profile",
            org_id="org_f6g7h8i9j0",
            payment_method_state=billing_pb2.PAYMENT_METHOD_STATE_ON_FILE,
            payment_methods=[billing_pb2.BillingPaymentMethod(id="pm_1", type="card")],
        )
        t = FakeTransport(
            {"GetBillingProfile": billing_pb2.GetBillingProfileResponse(profile=profile)}
        )
        got = Billing(t).retrieve_profile()  # type: ignore[arg-type]

        assert t.calls[0][0] == "GetBillingProfile"
        assert got.payment_method_state == billing_pb2.PAYMENT_METHOD_STATE_ON_FILE
        assert len(got.payment_methods) == 1
        assert got.payment_methods[0].brand == ""
        assert got.payment_methods[0].last4 == ""

    def test_none_for_an_org_that_has_never_touched_billing(self) -> None:
        profile = billing_pb2.BillingProfile(
            payment_method_state=billing_pb2.PAYMENT_METHOD_STATE_NONE
        )
        t = FakeTransport(
            {"GetBillingProfile": billing_pb2.GetBillingProfileResponse(profile=profile)}
        )
        got = Billing(t).retrieve_profile()  # type: ignore[arg-type]

        assert got.payment_method_state == billing_pb2.PAYMENT_METHOD_STATE_NONE
        assert len(got.payment_methods) == 0


class TestBudget:
    def test_retrieve_returns_spend_even_with_no_budget_set(self) -> None:
        # An org that has never set a budget still gets one back, so a card can
        # show current-period spend before a budget exists.
        budget = billing_pb2.Budget(
            object="budget",
            org_id="org_f6g7h8i9j0",
            spent_eur=12.5,
            currency="EUR",
            alert_steps=[50, 80, 100],
        )
        t = FakeTransport({"GetBudget": billing_pb2.GetBudgetResponse(budget=budget)})
        got = Billing(t).retrieve_budget()  # type: ignore[arg-type]

        assert t.calls[0][0] == "GetBudget"
        assert not got.HasField("amount_eur")
        assert not got.HasField("used_percent")
        assert got.spent_eur == 12.5

    def test_set_marks_amount_present(self) -> None:
        t = FakeTransport(
            {
                "UpdateBudget": lambda req: billing_pb2.UpdateBudgetResponse(
                    budget=billing_pb2.Budget(amount_eur=req.amount_eur, spent_eur=30.0)
                )
            }
        )
        got = Billing(t).set_budget(50.0)  # type: ignore[arg-type]

        method, req = t.calls[0]
        assert method == "UpdateBudget"
        assert req.HasField("amount_eur")
        assert req.amount_eur == 50.0
        assert got.amount_eur == 50.0

    def test_clear_omits_amount_entirely(self) -> None:
        # Absence is the clear signal — a zero would be rejected by the server's
        # `> 0` rule rather than read as "turn the alerts off".
        t = FakeTransport({"UpdateBudget": billing_pb2.UpdateBudgetResponse()})
        Billing(t).clear_budget()  # type: ignore[arg-type]

        req = t.calls[0][1]
        assert not req.HasField("amount_eur")

    def test_used_percent_is_not_capped_at_100(self) -> None:
        budget = billing_pb2.Budget(amount_eur=50.0, spent_eur=120.0, used_percent=240.0)
        t = FakeTransport({"GetBudget": billing_pb2.GetBudgetResponse(budget=budget)})
        assert Billing(t).retrieve_budget().used_percent == 240.0  # type: ignore[arg-type]


class TestOutstandingBalance:
    def test_retrieve_reports_tier_source_and_block_state(self) -> None:
        balance = billing_pb2.OutstandingBalance(
            object="outstanding_balance",
            org_id="org_f6g7h8i9j0",
            outstanding_cents=9000,
            tier=billing_pb2.TRUST_TIER_NEW,
            settled_payments=0,
            threshold_cents=5000,
            threshold_source=billing_pb2.EXPOSURE_THRESHOLD_SOURCE_TRUST_TIER,
            hard_stop_cents=10000,
            blocked=False,
            used_percent=180.0,
            alert_steps=[80, 100, 125, 150, 175, 200],
            notified_steps=[80, 100, 125, 150],
            currency="EUR",
            settlement_available=True,
        )
        t = FakeTransport(
            {"GetOutstandingBalance": billing_pb2.GetOutstandingBalanceResponse(balance=balance)}
        )
        got = Billing(t).retrieve_outstanding_balance()  # type: ignore[arg-type]

        assert t.calls[0][0] == "GetOutstandingBalance"
        assert got.tier == billing_pb2.TRUST_TIER_NEW
        assert got.threshold_source == billing_pb2.EXPOSURE_THRESHOLD_SOURCE_TRUST_TIER
        # Past the threshold and past three reminders, still serving: only
        # hard_stop_cents refuses new jobs.
        assert got.outstanding_cents > got.threshold_cents
        assert got.blocked is False
        assert got.hard_stop_cents == 2 * got.threshold_cents

    def test_unbounded_org_has_no_threshold_at_all(self) -> None:
        # The intended destination of the ladder: absent threshold, absent hard
        # stop, absent percentage — not a zero, which would read as "no credit".
        balance = billing_pb2.OutstandingBalance(
            outstanding_cents=42000,
            tier=billing_pb2.TRUST_TIER_PROVEN,
            settled_payments=7,
            threshold_source=billing_pb2.EXPOSURE_THRESHOLD_SOURCE_UNBOUNDED,
        )
        t = FakeTransport(
            {"GetOutstandingBalance": billing_pb2.GetOutstandingBalanceResponse(balance=balance)}
        )
        got = Billing(t).retrieve_outstanding_balance()  # type: ignore[arg-type]

        assert not got.HasField("threshold_cents")
        assert not got.HasField("hard_stop_cents")
        assert not got.HasField("used_percent")
        assert got.blocked is False


class TestSettleOutstandingBalance:
    def test_returns_the_statement_and_the_cleared_balance(self) -> None:
        resp = billing_pb2.SettleOutstandingBalanceResponse(
            settlement=billing_pb2.Settlement(
                object="settlement",
                invoice_id="inv_a1b2c3d4e5f6",
                amount_cents=9000,
                currency="EUR",
            ),
            balance=billing_pb2.OutstandingBalance(
                outstanding_cents=0,
                blocked=False,
                threshold_cents=5000,
                hard_stop_cents=10000,
                used_percent=0.0,
            ),
        )
        t = FakeTransport({"SettleOutstandingBalance": resp})
        got = Billing(t).settle_outstanding_balance()  # type: ignore[arg-type]

        method, req = t.calls[0]
        assert method == "SettleOutstandingBalance"
        # No amount on the request, by design: the ledger names the figure.
        assert req.SerializeToString() == b""
        assert got.settlement.invoice_id == "inv_a1b2c3d4e5f6"
        assert got.balance.outstanding_cents == 0
        assert got.balance.blocked is False


class TestCreatePortalSession:
    def test_returns_the_provider_session_url(self) -> None:
        session = billing_pb2.BillingPortalSession(
            object="billing_portal_session",
            url="https://portal.example/session/abc",
        )
        t = FakeTransport(
            {
                "CreateBillingPortalSession": billing_pb2.CreateBillingPortalSessionResponse(
                    session=session
                )
            }
        )
        got = Billing(t).create_portal_session()  # type: ignore[arg-type]

        assert t.calls[0][0] == "CreateBillingPortalSession"
        assert got.url == "https://portal.example/session/abc"


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
