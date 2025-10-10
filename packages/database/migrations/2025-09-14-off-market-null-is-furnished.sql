-- Purpose: One-time cleanup to prevent stale furnished flags on off-market listings
-- Context: Listings no longer present in latest CSV are marked off-market (is_active = FALSE).
--          Historically, is_furnished might remain TRUE, causing stale detail/exports.
-- Action: Set is_furnished = NULL for all off-market listings that still have TRUE.

BEGIN;

UPDATE properties
SET
  is_furnished = NULL,
  status = 'updated',
  status_changed_at = NOW()
WHERE
  is_active = FALSE
  AND is_furnished IS TRUE;

COMMIT;
