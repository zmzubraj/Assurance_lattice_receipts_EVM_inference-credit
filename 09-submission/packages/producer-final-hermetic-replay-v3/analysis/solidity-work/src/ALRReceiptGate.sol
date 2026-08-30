// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice Development-only deterministic gate for ALR-MPP-PILOT-V1.
contract ALRReceiptGate {
    enum Reason {
        ELIGIBLE,
        EXECUTION_FAIL,
        EXECUTION_UNKNOWN,
        SEMANTIC_FAIL,
        SEMANTIC_UNKNOWN,
        AUTHORITY_FAIL,
        AUTHORITY_UNKNOWN,
        PROVENANCE_FAIL,
        PROVENANCE_UNKNOWN,
        FRESHNESS_FAIL,
        FRESHNESS_UNKNOWN,
        ORIGIN_SCOPE_FAIL,
        ORIGIN_SCOPE_UNKNOWN,
        RECEIPT_REPLAY,
        REQUEST_HASH_MISMATCH,
        RESPONSE_HASH_MISMATCH,
        AUTHORITY_EPOCH_STALE,
        EVIDENCE_ORIGIN_DISALLOWED,
        CLAIM_SCOPE_MISMATCH,
        TYPE_TAG_INVALID
    }

    uint8 internal constant PASS = 0;
    uint8 internal constant FAIL = 1;
    uint8 internal constant UNKNOWN = 2;

    function evaluate(uint8[6] memory states, uint8 bindingFlags)
        external
        pure
        returns (bool eligible, Reason reason)
    {
        Reason[6] memory failReasons = [
            Reason.EXECUTION_FAIL,
            Reason.SEMANTIC_FAIL,
            Reason.AUTHORITY_FAIL,
            Reason.PROVENANCE_FAIL,
            Reason.FRESHNESS_FAIL,
            Reason.ORIGIN_SCOPE_FAIL
        ];
        Reason[6] memory unknownReasons = [
            Reason.EXECUTION_UNKNOWN,
            Reason.SEMANTIC_UNKNOWN,
            Reason.AUTHORITY_UNKNOWN,
            Reason.PROVENANCE_UNKNOWN,
            Reason.FRESHNESS_UNKNOWN,
            Reason.ORIGIN_SCOPE_UNKNOWN
        ];
        for (uint256 index = 0; index < states.length; index++) {
            if (states[index] == FAIL) return (false, failReasons[index]);
            if (states[index] == UNKNOWN) return (false, unknownReasons[index]);
            if (states[index] != PASS) return (false, Reason.TYPE_TAG_INVALID);
        }
        if (!_flag(bindingFlags, 0)) return (false, Reason.RECEIPT_REPLAY);
        if (!_flag(bindingFlags, 1)) return (false, Reason.REQUEST_HASH_MISMATCH);
        if (!_flag(bindingFlags, 2)) return (false, Reason.RESPONSE_HASH_MISMATCH);
        if (!_flag(bindingFlags, 3)) return (false, Reason.AUTHORITY_EPOCH_STALE);
        if (!_flag(bindingFlags, 4)) return (false, Reason.EVIDENCE_ORIGIN_DISALLOWED);
        if (!_flag(bindingFlags, 5)) return (false, Reason.CLAIM_SCOPE_MISMATCH);
        if (!_flag(bindingFlags, 6)) return (false, Reason.TYPE_TAG_INVALID);
        return (true, Reason.ELIGIBLE);
    }

    function _flag(uint8 flags, uint8 position) internal pure returns (bool) {
        return flags & (uint8(1) << position) != 0;
    }
}
