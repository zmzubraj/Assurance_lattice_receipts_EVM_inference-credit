"""Deterministic Assurance-Lattice Receipt (ALR) reference kernel.

This module is a development prototype. Generated states are synthetic test
fixtures and are not evidence of real-world reliability or semantic correctness.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from itertools import product
from typing import Iterable, Iterator


class AssuranceState(IntEnum):
    PASS = 0
    FAIL = 1
    UNKNOWN = 2


class ReasonCode(IntEnum):
    ELIGIBLE = 0
    EXECUTION_FAIL = 1
    EXECUTION_UNKNOWN = 2
    SEMANTIC_FAIL = 3
    SEMANTIC_UNKNOWN = 4
    AUTHORITY_FAIL = 5
    AUTHORITY_UNKNOWN = 6
    PROVENANCE_FAIL = 7
    PROVENANCE_UNKNOWN = 8
    FRESHNESS_FAIL = 9
    FRESHNESS_UNKNOWN = 10
    ORIGIN_SCOPE_FAIL = 11
    ORIGIN_SCOPE_UNKNOWN = 12
    RECEIPT_REPLAY = 13
    REQUEST_HASH_MISMATCH = 14
    RESPONSE_HASH_MISMATCH = 15
    AUTHORITY_EPOCH_STALE = 16
    EVIDENCE_ORIGIN_DISALLOWED = 17
    CLAIM_SCOPE_MISMATCH = 18
    TYPE_TAG_INVALID = 19


DIMENSION_NAMES = (
    "execution",
    "semantic",
    "authority",
    "provenance",
    "freshness",
    "origin_scope",
)

_DIMENSION_REASONS = (
    (ReasonCode.EXECUTION_FAIL, ReasonCode.EXECUTION_UNKNOWN),
    (ReasonCode.SEMANTIC_FAIL, ReasonCode.SEMANTIC_UNKNOWN),
    (ReasonCode.AUTHORITY_FAIL, ReasonCode.AUTHORITY_UNKNOWN),
    (ReasonCode.PROVENANCE_FAIL, ReasonCode.PROVENANCE_UNKNOWN),
    (ReasonCode.FRESHNESS_FAIL, ReasonCode.FRESHNESS_UNKNOWN),
    (ReasonCode.ORIGIN_SCOPE_FAIL, ReasonCode.ORIGIN_SCOPE_UNKNOWN),
)


@dataclass(frozen=True, slots=True)
class BindingChecks:
    receipt_unused: bool = True
    request_hash_match: bool = True
    response_hash_match: bool = True
    authority_epoch_live: bool = True
    evidence_origin_allowed: bool = True
    claim_scope_match: bool = True
    type_tag_valid: bool = True

    def bitmask(self) -> int:
        checks = (
            self.receipt_unused,
            self.request_hash_match,
            self.response_hash_match,
            self.authority_epoch_live,
            self.evidence_origin_allowed,
            self.claim_scope_match,
            self.type_tag_valid,
        )
        return sum((1 << index) for index, passed in enumerate(checks) if passed)


@dataclass(frozen=True, slots=True)
class AssuranceReceipt:
    execution: AssuranceState
    semantic: AssuranceState
    authority: AssuranceState
    provenance: AssuranceState
    freshness: AssuranceState
    origin_scope: AssuranceState
    bindings: BindingChecks = BindingChecks()

    def states(self) -> tuple[AssuranceState, ...]:
        return (
            self.execution,
            self.semantic,
            self.authority,
            self.provenance,
            self.freshness,
            self.origin_scope,
        )


@dataclass(frozen=True, slots=True)
class EligibilityDecision:
    eligible: bool
    reason: ReasonCode


def evaluate(receipt: AssuranceReceipt) -> EligibilityDecision:
    """Apply the frozen fail-closed precedence rule."""
    for state, (fail_reason, unknown_reason) in zip(
        receipt.states(), _DIMENSION_REASONS, strict=True
    ):
        if state is AssuranceState.FAIL:
            return EligibilityDecision(False, fail_reason)
        if state is AssuranceState.UNKNOWN:
            return EligibilityDecision(False, unknown_reason)

    bindings = receipt.bindings
    ordered_binding_failures = (
        (bindings.receipt_unused, ReasonCode.RECEIPT_REPLAY),
        (bindings.request_hash_match, ReasonCode.REQUEST_HASH_MISMATCH),
        (bindings.response_hash_match, ReasonCode.RESPONSE_HASH_MISMATCH),
        (bindings.authority_epoch_live, ReasonCode.AUTHORITY_EPOCH_STALE),
        (bindings.evidence_origin_allowed, ReasonCode.EVIDENCE_ORIGIN_DISALLOWED),
        (bindings.claim_scope_match, ReasonCode.CLAIM_SCOPE_MISMATCH),
        (bindings.type_tag_valid, ReasonCode.TYPE_TAG_INVALID),
    )
    for passed, reason in ordered_binding_failures:
        if not passed:
            return EligibilityDecision(False, reason)
    return EligibilityDecision(True, ReasonCode.ELIGIBLE)


def base_receipts() -> Iterator[AssuranceReceipt]:
    """Enumerate the complete 3^6 base state space in canonical order."""
    for states in product(AssuranceState, repeat=len(DIMENSION_NAMES)):
        yield AssuranceReceipt(*states)


def mutation_receipts() -> Iterable[tuple[str, AssuranceReceipt, ReasonCode]]:
    all_pass = dict.fromkeys(DIMENSION_NAMES, AssuranceState.PASS)
    mutations = (
        ("consumed_receipt_replay", "receipt_unused", ReasonCode.RECEIPT_REPLAY),
        ("request_hash_substitution", "request_hash_match", ReasonCode.REQUEST_HASH_MISMATCH),
        ("response_hash_substitution", "response_hash_match", ReasonCode.RESPONSE_HASH_MISMATCH),
        ("stale_authority_epoch", "authority_epoch_live", ReasonCode.AUTHORITY_EPOCH_STALE),
        ("disallowed_evidence_origin", "evidence_origin_allowed", ReasonCode.EVIDENCE_ORIGIN_DISALLOWED),
        ("claim_scope_mismatch", "claim_scope_match", ReasonCode.CLAIM_SCOPE_MISMATCH),
        ("invalid_type_tag", "type_tag_valid", ReasonCode.TYPE_TAG_INVALID),
    )
    for name, field, expected in mutations:
        binding_values = {
            "receipt_unused": True,
            "request_hash_match": True,
            "response_hash_match": True,
            "authority_epoch_live": True,
            "evidence_origin_allowed": True,
            "claim_scope_match": True,
            "type_tag_valid": True,
        }
        binding_values[field] = False
        yield name, AssuranceReceipt(**all_pass, bindings=BindingChecks(**binding_values)), expected

