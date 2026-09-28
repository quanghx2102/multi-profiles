# Fixture Policy

Use synthetic, disposable profiles/accounts/services with unique sentinel values. Record fixture version and expected state types. Fixtures must contain no personal data, reusable credential, production cookie/token, real proxy credential, or copied user profile.

Browser-state fixtures are stored as reproducible setup procedures where possible. Any generated profile artifact is treated as sensitive, kept outside Git by default, hashed, access-controlled, and destroyed according to the evidence retention policy.

