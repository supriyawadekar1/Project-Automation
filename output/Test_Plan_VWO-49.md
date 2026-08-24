# Test Plan — VWO-49 (KAN-6): VWO Login Dashboard

> Status: **DRAFT — pending human review.** Not approved until a QA owner signs off.
> Author: Supriya Wadekar
> Source ticket: KAN-6 (summary: "VWO-49") — VWO Login Dashboard PRD

## 1. Scope & Objectives

- **In scope:**
  - Functional: email/password login, Remember Me, Forgot Password / reset flow, real-time validation, error handling, session timeout, 2FA (optional), SSO (enterprise), light/dark mode
  - Non-functional: security (HTTPS, rate limiting, secure storage, GDPR/CCPA), performance (sub-2s load, concurrency), accessibility (WCAG 2.1 AA), responsive/mobile
  - Integration: transition to VWO core dashboard, analytics login success/failure events, support system links
- **Out of scope:**
  - VWO core platform features (experiments, heatmaps, personalization) beyond the login transition
  - Social login (Google/Microsoft) — listed as optional/future
  - Biometric / adaptive authentication (future enhancement)
  - Backend password hashing internals (verified only indirectly / via design review)
- **Objective:** Define what "tested" means for the VWO login dashboard so that a QA engineer can confirm the login experience meets the PRD's functional, security, performance, and accessibility requirements — and surface gaps that block sign-off.

## 2. Gaps & Questions for the author

| # | Area | Finding (⚠️/❌) | Question to author |
|---|------|----------------|--------------------|
| 1 | Acceptance criteria | ❌ No explicit, testable ACs (pass/fail) anywhere in the ticket | Can you provide numbered ACs per feature (login, reset, 2FA, SSO)? |
| 2 | 2FA | ⚠️ "Optional 2FA support" — no methods (TOTP/SMS/email) or enrollment flow | Which 2FA methods are in scope for this release? Where is enrollment managed? |
| 3 | SSO | ⚠️ SAML/OAuth mentioned, no IdP config or test accounts | Which IdP(s) must be supported (Okta/Azure AD/other)? Can we get a test tenant? |
| 4 | Session timeout | ⚠️ "Configurable timeout periods" — no default value | What is the default idle timeout? Is it per-role or global config? |
| 5 | Password rules | ⚠️ "Enforced security standards" — no complexity spec | What are the min length / complexity rules for new passwords? |
| 6 | Rate limiting | ⚠️ "Request throttling" — no threshold N | After how many failed attempts does lockout trigger? What's the lockout duration / message? |
| 7 | Error messages | ⚠️ "Clear, actionable" — no verbatim strings | Provide exact error text for invalid credentials, locked account, empty fields, invalid email |
| 8 | Remember Me | ⚠️ Persistent session — no expiry | What's the Remember Me session duration vs normal session? Cookie vs token? |
| 9 | Dark mode | ⚠️ Announcement banner mentions Light/Dark toggle — no spec | Is dark mode part of this ticket? Default mode? Persisted preference? |
| 10 | Test data/env | ❌ No URLs, accounts, or environments given | Which env URLs (QA/UAT), test accounts, and IdP test users should we use? |
| 11 | Analytics | ⚠️ "Login success/failure tracking" — no event names | What are the exact event names/properties to assert? |
| 12 | Roles/permissions | ❌ No role matrix | What roles exist (admin/user/enterprise) and how do they affect the login flow? |
| 13 | i18n | ❌ Not mentioned | Is the login page localized? Which locales? |
| 14 | Boundaries | ⚠️ Empty/0/1/max not specified | Confirm behavior for empty fields, 1-char password, max-length input, unicode email |
| 15 | A11y tooling | ⚠️ WCAG 2.1 AA target — no audit baseline | Which screen readers/browsers form the a11y test matrix? Any existing audit? |

## 3. Test Scenarios

| ID | Priority | Type (pos/neg/boundary) | Scenario | Maps to (AC / gap) |
|----|----------|-------------------------|----------|--------------------|
| TS-1 | P0 | positive | Successful login with valid email + password redirects to VWO core dashboard | PRD §Functional (Gap 1) |
| TS-2 | P0 | positive | Auto-focus lands on first input field on page load | PRD UX |
| TS-3 | P0 | positive | Remember Me checked → session persists across browser restart | PRD Remember Me (Gap 8) |
| TS-4 | P1 | positive | Remember Me unchecked → re-auth required after browser restart | PRD Remember Me (Gap 8) |
| TS-5 | P0 | positive | Forgot Password: registered email → reset link sent, token valid once | PRD Password Mgmt (Gap 1) |
| TS-6 | P1 | positive | Password reset with strong new password succeeds; re-login works | PRD Password Mgmt (Gap 5) |
| TS-7 | P1 | positive | Enterprise SSO login via IdP redirects back authenticated | PRD SSO (Gap 3) |
| TS-8 | P1 | positive | Optional 2FA: valid code completes login | PRD 2FA (Gap 2) |
| TS-9 | P0 | negative | Invalid credentials → generic error, no field-specific leakage | PRD Error Handling (Gap 7) |
| TS-10 | P0 | negative | Empty email/password on submit → inline validation errors, no request | PRD Validation |
| TS-11 | P1 | negative | Malformed email (e.g. `user@domain`) on blur → format error | PRD Validation |
| TS-12 | P1 | negative | Non-registered email in Forgot Password → generic response (no account enumeration) | PRD Security (Gap 7) |
| TS-13 | P0 | negative | Exceed rate limit → lockout message, further attempts blocked | PRD Rate Limiting (Gap 6) |
| TS-14 | P1 | negative | Expired/used reset token → error, token cannot be reused | PRD Password Mgmt |
| TS-15 | P1 | negative | Invalid 2FA code (wrong/expired) → error, login blocked | PRD 2FA (Gap 2) |
| TS-16 | P0 | negative | Session idle timeout → auto logout, re-auth required | PRD Session Mgmt (Gap 4) |
| TS-17 | P1 | boundary | Password at min length (boundary) accepted; one char below rejected | PRD Password Rules (Gap 5) |
| TS-18 | P2 | boundary | Max-length input (email/password) handled without truncation error | Gap 14 |
| TS-19 | P1 | boundary | Empty-state: no accounts/roles → appropriate error or signup CTA | Gap 14 |
| TS-20 | P0 | security | `http://` URL redirects to `https://` (HTTPS enforcement) | PRD Security |
| TS-21 | P0 | security | Network capture: credentials transmitted over TLS, no plaintext | PRD Data Protection |
| TS-22 | P1 | security | No session hijacking: token regenerated on login, session cookie flags (Secure/HttpOnly) | PRD Session Security |
| TS-23 | P1 | security | GDPR/CCPA: data export/delete request path functional | PRD Compliance |
| TS-24 | P0 | performance | Login page loads and is interactive within 2s on standard connection | PRD Performance (Gap 10) |
| TS-25 | P2 | performance | Concurrent logins (thousands simulated) — no degradation / 99.9% uptime | PRD Scalability |
| TS-26 | P0 | a11y | Full keyboard navigation (Tab/Shift+Tab/Enter/Space) with visible focus | PRD A11y |
| TS-27 | P1 | a11y | Screen reader (NVDA/VoiceOver) announces all fields, labels, errors | PRD A11y (Gap 15) |
| TS-28 | P1 | a11y | High contrast mode renders all elements accessible | PRD A11y |
| TS-29 | P1 | responsive | Mobile viewport: touch targets ≥ recommended size, usable layout | PRD Responsive |
| TS-30 | P2 | positive | Light/Dark mode toggle renders correctly in both modes, persisted | PRD Theme (Gap 9) |
| TS-31 | P1 | positive | Loading state shown during auth processing; double-submit prevented | PRD UX |
| TS-32 | P1 | integration | After login, analytics fires login-success event with expected properties | PRD Analytics (Gap 11) |
| TS-33 | P2 | integration | Failed logins fire login-failure event | PRD Analytics (Gap 11) |
| TS-34 | P2 | compatibility | Login works on Chrome, Firefox, Edge, Safari (desktop + mobile) | PRD Platforms |

## 4. Test Data & Environment

- **Data:**
  - Valid user: active email + password (QA-created)
  - Invalid user: wrong password; unregistered email
  - Boundary passwords: exactly at min length, one char below, max length
  - Registered + unregistered emails for Forgot Password
  - 2FA: valid, wrong, expired codes
  - SSO: test IdP user (pending IdP details — Gap 3)
- **Environment / flags:**
  - QA URL: **TBD** (Gap 10) — expected `https://app.vwo.com`
  - Feature flags: 2FA, SSO, dark mode toggles per env
  - HTTPS enforced; CDN in use
- **Roles / permissions:**
  - Standard user, enterprise/SSO user, admin (role matrix TBD — Gap 12)

## 5. Risks & Assumptions

- **Assumptions made:**
  - Ticket KAN-6 (summary "VWO-49") describes the VWO login dashboard at `https://app.vwo.com`
  - "Optional 2FA" and "SSO" are in scope for this release unless marked future
  - Light/dark mode toggle is part of the current UI (announcement banner) and in scope
  - WCAG 2.1 AA is the accessibility bar; mobile-first responsive design expected
- **Risks:**
  - No explicit ACs → test interpretation may diverge from product intent (blocking)
  - Missing env URLs/accounts → execution cannot start in QA (blocking)
  - 2FA/SSO details undefined → scenarios TS-7/8 may need rework
  - Rate-limit threshold unknown → TS-13 cannot assert exact lockout behavior
  - Analytics event names unconfirmed → TS-32/33 assertions provisional

## 6. Entry / Exit criteria

- **Entry:**
  - QA environment URL + test accounts available
  - Build with login dashboard changes deployed
  - Test plan reviewed and approved
  - ACs confirmed by author (or gaps resolved)
- **Exit:**
  - All P0/P1 scenarios executed and passed (or defects logged)
  - P0 security/perf/a11y scenarios verified
  - Critical/High defects resolved or waived by product owner
  - Test summary + defect report delivered

---
## HUMAN REVIEW GATE

- **I assumed:** KAN-6 ↔ VWO-49 login dashboard scope; 2FA/SSO/dark mode in scope; `app.vwo.com` is the target
- **I could not confirm:** explicit ACs, env URLs, test accounts, rate-limit threshold, timeout value, password rules, IdP details, analytics event names, role matrix, i18n scope
- **Open questions blocking sign-off:** Gap #1 (ACs), #10 (env/data), #6 (rate limit), #4 (timeout), #5 (password rules), #3 (SSO), #2 (2FA), #7 (error text), #11 (analytics), #12 (roles), #15 (a11y matrix)
- ▶ **Approve, or edit, before I write test cases / automation.**
