"""Billing resource — an organization's invoices, budget and outstanding balance."""

from __future__ import annotations

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
    to create, edit, or delete one — a statement records what happened. The one
    exception is :meth:`settle_outstanding_balance`, which closes the period
    early and produces an ordinary statement for what is owed so far.

    Monetary amounts are integer minor units (cents) of the invoice currency:
    ``total_cents == 1250`` in EUR is 12.50 EUR. The budget is the exception —
    it is stated in whole EUR as a float, matching how a customer types it.
    """

    def __init__(self, transport: Transport) -> None:
        self._t = transport

    def list_invoices(
        self,
        *,
        limit: int | None = None,
        opts: CallOptions | None = None,
    ) -> Page[billing_pb2.Invoice]:
        """Page through finalized invoices, newest period first.

        Line items are omitted here — use :meth:`retrieve` for one invoice's
        breakdown. A statement still being generated for a just-ended period is
        never returned; for the period currently accruing use
        :meth:`retrieve_upcoming`.
        """

        def fetch(cursor: str | None) -> PageContents[billing_pb2.Invoice]:
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

    def retrieve(self, invoice_id: str, opts: CallOptions | None = None) -> billing_pb2.Invoice:
        """Retrieve one invoice by ID (``inv_*``), including its line items."""
        req = billing_pb2.GetInvoiceRequest(id=invoice_id)
        return self._t.unary(
            _SERVICE,
            "GetInvoice",
            req,
            billing_pb2.GetInvoiceResponse(),
            opts,
        ).invoice

    def retrieve_upcoming(self, opts: CallOptions | None = None) -> billing_pb2.Invoice:
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

    def retrieve_profile(self, opts: CallOptions | None = None) -> billing_pb2.BillingProfile:
        """Retrieve the organization's payment standing.

        Reports whether the payment provider holds a chargeable method, and
        whatever it will say about that method for display. Read-only and
        side-effect free — it never creates provider resources. An organization
        that has never touched billing reports ``PAYMENT_METHOD_STATE_NONE``
        and no payment methods.

        ``payment_method_state`` is the only reliable signal. A method's
        ``brand`` and ``last4`` are frequently absent even for a working card,
        because the provider does not always expose card metadata; render such
        a method as "Card on file" rather than treating the missing digits as
        an error.
        """
        req = billing_pb2.GetBillingProfileRequest()
        return self._t.unary(
            _SERVICE,
            "GetBillingProfile",
            req,
            billing_pb2.GetBillingProfileResponse(),
            opts,
        ).profile

    def retrieve_budget(self, opts: CallOptions | None = None) -> billing_pb2.Budget:
        """Retrieve the organization's monthly budget and the spend against it.

        A budget is the organization's own telemetry and it NEVER enforces
        anything: crossing 100% sends an email and changes nothing else. The
        hard cap is the per-app spend limit
        (:meth:`~transcodely.resources.apps.Apps.set_spend_limit`), which does
        refuse new jobs. Limits block; budgets notify.

        Always returns a budget: an organization that has never set one gets
        ``amount_eur`` absent with ``spent_eur`` still populated, so the current
        period's spend can be shown before a budget exists.
        """
        req = billing_pb2.GetBudgetRequest()
        return self._t.unary(
            _SERVICE,
            "GetBudget",
            req,
            billing_pb2.GetBudgetResponse(),
            opts,
        ).budget

    def update_budget(
        self,
        amount_eur: float | None = None,
        opts: CallOptions | None = None,
    ) -> billing_pb2.Budget:
        """Set or clear the organization's monthly budget.

        Pass ``amount_eur`` (must be > 0) to set the budget, or leave it
        ``None`` to clear it and stop the alert emails. :meth:`set_budget` and
        :meth:`clear_budget` are the ergonomic shorthands.

        Moving the amount never re-arms an alert step already sent this period —
        read ``notified_steps`` on the returned budget to see which have fired.
        """
        req = billing_pb2.UpdateBudgetRequest()
        if amount_eur is not None:
            # Setting the optional field marks presence; leaving it unset omits
            # it from the request, which the server reads as "clear the budget".
            req.amount_eur = amount_eur
        return self._t.unary(
            _SERVICE,
            "UpdateBudget",
            req,
            billing_pb2.UpdateBudgetResponse(),
            opts,
        ).budget

    def set_budget(self, amount_eur: float, opts: CallOptions | None = None) -> billing_pb2.Budget:
        """Set the organization's monthly budget in EUR (must be > 0).

        Alert emails go out as spend crosses each step in ``alert_steps`` (50%,
        80% and 100% today). Nothing is restricted at any of them.
        """
        return self.update_budget(amount_eur, opts)

    def clear_budget(self, opts: CallOptions | None = None) -> billing_pb2.Budget:
        """Clear the monthly budget, turning the alert emails off (the default)."""
        return self.update_budget(None, opts)

    def retrieve_outstanding_balance(
        self, opts: CallOptions | None = None
    ) -> billing_pb2.OutstandingBalance:
        """Retrieve the unsettled balance and the threshold it is measured against.

        Usage that has been accrued and not yet captured onto a statement,
        across every app in the organization. It is a different number from
        :meth:`retrieve_upcoming` (which is what the *current period* accrued,
        while this also carries anything an earlier period left uncaptured) and
        from ``Budget.spent_eur`` (which keeps counting after an invoice is
        issued, while this drops to zero when one is).

        Reminder emails go out at 80%, 100%, 125%, 150% and 175% of
        ``threshold_cents`` and restrict nothing. Only at ``hard_stop_cents`` —
        twice the threshold — are new jobs refused, with error code
        ``outstanding_balance_exceeded``; work already queued or running still
        finishes and videos keep playing. ``blocked`` reads the same numbers the
        admission gate reads.

        Always returns a balance: an organization that owes nothing gets one
        with ``outstanding_cents`` 0 and its threshold still populated.
        """
        req = billing_pb2.GetOutstandingBalanceRequest()
        return self._t.unary(
            _SERVICE,
            "GetOutstandingBalance",
            req,
            billing_pb2.GetOutstandingBalanceResponse(),
            opts,
        ).balance

    def settle_outstanding_balance(
        self, opts: CallOptions | None = None
    ) -> billing_pb2.SettleOutstandingBalanceResponse:
        """Pay the outstanding balance now, without waiting for the period to end.

        Closes the current period at this instant and produces a real statement
        for everything owed, which the payment provider then charges. On success
        the balance is zero, any admission block is lifted immediately, and the
        trust tier re-evaluates once the statement is paid.

        Takes no amount on purpose: the figure is whatever the ledger says at
        the instant the settlement runs, so a stale page cannot pay less than is
        owed and leave the difference looking settled.

        Returns both the :class:`~transcodely.types.Settlement` and the balance
        as it now stands, so a caller that just paid can render the new state
        without a second request.

        Raises :class:`~transcodely.errors.PreconditionError` with code
        ``settlement_unavailable`` when the deployment has mid-cycle settlement
        switched off — check ``settlement_available`` on the balance before
        offering a "pay now" action — and ``nothing_outstanding`` when there is
        nothing to pay.
        """
        req = billing_pb2.SettleOutstandingBalanceRequest()
        return self._t.unary(
            _SERVICE,
            "SettleOutstandingBalance",
            req,
            billing_pb2.SettleOutstandingBalanceResponse(),
            opts,
        )

    def create_portal_session(
        self, opts: CallOptions | None = None
    ) -> billing_pb2.BillingPortalSession:
        """Create a session for the payment provider's hosted billing portal.

        The portal is where a payment method is added or replaced and where
        receipts live — card details never touch this SDK.

        The first call for an organization also links it to the payment
        provider, so the returned portal is already attached to this
        organization's billing account. Safe to call repeatedly.

        The session is single-use and expires; request a fresh one per visit
        rather than storing the URL.
        """
        req = billing_pb2.CreateBillingPortalSessionRequest()
        return self._t.unary(
            _SERVICE,
            "CreateBillingPortalSession",
            req,
            billing_pb2.CreateBillingPortalSessionResponse(),
            opts,
        ).session
