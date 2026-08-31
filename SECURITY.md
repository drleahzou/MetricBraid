# Security and sensitive data

MetricBraid is a framework for analysing personal wearable data. This
repository must remain a template and must not contain secrets or personal
health data.

## Never commit sensitive material

Never commit any of the following, even temporarily or on a private branch:

- OAuth access tokens, refresh tokens, authorisation codes, or session tokens;
- Garmin or Oura usernames, passwords, client secrets, credentials, session
  cookies, or cached authentication files;
- raw health exports, including downloaded archives, CSV files, JSON files, or
  provider exports;
- `.env` files or local configuration files containing secrets; or
- personally identifiable health observations, including measurements,
  symptoms, diagnoses, medications, sleep, activity, or location data linked
  to a real person.

The repository's `.gitignore` reduces the chance of accidental commits, but it
is not a security boundary. Review every staged change before committing. Use
only synthetic or properly de-identified data for examples and fixtures.

## Handle credentials locally

Keep credentials outside the repository and supply them through local
environment variables or the provider's recommended credential store. Grant
the minimum access required, and revoke or rotate credentials when they are no
longer needed.

If a credential or personal health record is committed, treat it as exposed:
revoke or rotate the credential immediately and notify the maintainers
privately. Deleting the file in a later commit does not remove it from Git
history.

## Report security concerns privately

Do not include credentials, health data, or exploit details in a public issue.
Use the repository host's private vulnerability-reporting channel when
available, or contact a maintainer privately before sharing sensitive details.

## Medical disclaimer

MetricBraid supports analytical data-quality and provenance work. It is not a
medical device, does not provide medical advice, and must not be used to
diagnose illness or make treatment decisions. Consult a qualified healthcare
professional for medical concerns and local emergency services for urgent
symptoms.
