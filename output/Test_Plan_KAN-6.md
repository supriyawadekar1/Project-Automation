# Test Plan — KAN-6: VWO-49

## 1. Scope & Objectives
- **In scope:**
    - Verification of the VWO Login Dashboard functionality at `http://app.vwo.com`.
    - Authentication flows (Email/Password, Forgot Password).
    - UI/UX features (Responsive design, Light/Dark mode, Auto-focus, Loading states).
    - Security features (HTTPS enforcement, Rate limiting, Input validation).
    - Accessibility compliance (WCAG 2.1 AA, Keyboard navigation, Screen reader support).
    - Performance metrics (Page load < 2s).
- **Out of scope:**
    - Internal VWO Core Platform dashboard functionality post-login (only the transition is in scope).
    - Future enhancements (Biometric auth, PWA, Adaptive auth) as they are listed under "Future Enhancements" and not current requirements.
    - Marketing site content other than the login page.
- **Objective:**
    - Ensure the login dashboard meets the defined functional, security, performance, and accessibility requirements for both primary (marketers/PMs) and secondary (enterprise) users.

## 2. Gaps & Questions for the author
| # | Area | Finding (⚠️/❌) | Question to author |
| :--- | :--- | :--- | :--- |
| 1 | Acceptance Criteria | ❌ Missing | The ticket states "None found in the ticket." Please provide specific, testable Acceptance Criteria (ACs) for each functional requirement (e.g., exact error message text, specific timeout durations). |
| 2 | Test Data | ❌ Missing | No test accounts are provided. Please specify: 1) Valid user credentials, 2) User with 2FA enabled, 3) User with SSO enabled, 4) Locked/Inactive user account. |
| 3 | Environment | ⚠️ Ambiguous | The URL `http://app.vwo.com` is listed. Is this the production URL or a staging/QA environment? Testing against production is risky; please confirm the target environment URL. |
| 4 | Security/Rate Limiting | ⚠️ Ambiguous | "Rate Limiting: Protection against brute force attacks" is mentioned, but no threshold is defined. How many failed attempts trigger a lockout or CAPTCHA? What is the lockout duration? |
| 5 | Performance | ⚠️ Ambiguous | "Standard connections" for the 2-second load time is undefined. Please specify the network conditions (e.g., 4G, 3G, Cable) and device types (Desktop vs. Mobile) for performance testing. |
| 6 | SSO/2FA | ⚠️ Ambiguous | SSO (SAML/OAuth) and 2FA are listed as features. Are these currently implemented and active for all users, or only for specific enterprise plans? If active, please provide test IdP configurations. |
| 7 | Accessibility | ⚠️ Ambiguous | "High Contrast Mode" is mentioned. Is this a user-selectable setting within the app, or does it rely on OS-level settings? Please clarify the mechanism for testing. |
| 8 | Error Handling | ⚠️ Ambiguous | "Clear, actionable error messages" are required. Please provide the exact copy for: 1) Invalid email format, 2) Wrong password, 3) Account locked, 4) Network error. |
| 9 | Session Management | ⚠️ Ambiguous | "Configurable timeout periods" is mentioned. What is the default session timeout? Is it configurable by the user or admin? |
| 10 | Regression Surface | ❌ Missing | No mention of existing dependencies or regression risks. Does this change affect the "Remember Me" cookie persistence or the redirect logic to the main dashboard? |

## 3. Test Scenarios
| ID | Priority | Type (pos/neg/boundary) | Scenario | Maps to (AC / gap) |
| :--- | :--- | :--- | :--- | :--- |
| TS-01 | P0 | Positive | Verify user can successfully log in with valid email and password. | Gap #1 (Missing AC) |
| TS-02 | P0 | Negative | Verify error message displays when entering an invalid email format (e.g., missing @). | Gap #8 |
| TS-03 | P0 | Negative | Verify error message displays when entering a correct email but incorrect password. | Gap #8 |
| TS-04 | P0 | Security | Verify that the login page is served over HTTPS (SSL/TLS). | Technical Req: Security |
| TS-05 | P1 | Boundary | Verify rate limiting triggers after the defined number of failed login attempts (threshold TBD). | Gap #4 |
| TS-06 | P1 | Positive | Verify "Remember Me" checkbox persists the session/credentials across browser restarts. | Functional Req: Auth |
| TS-07 | P1 | Positive | Verify "Forgot Password" link initiates the reset flow and sends a token to the registered email. | Functional Req: Password Mgmt |
| TS-08 | P1 | Accessibility | Verify full keyboard navigation (Tab/Shift+Tab) works through all interactive elements (Email, Password, Buttons). | Functional Req: Accessibility |
| TS-09 | P1 | Accessibility | Verify screen reader compatibility (ARIA labels) for input fields and error messages. | Functional Req: Accessibility |
| TS-10 | P2 | Performance | Verify login page loads within 2 seconds on a standard 4G connection. | Gap #5 |
| TS-11 | P2 | Responsive | Verify layout and touch targets are optimized on mobile devices (iOS/Android). | Functional Req: UX |
| TS-12 | P2 | Positive | Verify Light and Dark Mode toggle (if present) updates the UI correctly. | Functional Req: Branding |
| TS-13 | P1 | Integration | Verify successful login redirects to the main VWO dashboard. | Functional Req: Integration |
| TS-14 | P1 | Security | Verify password input field masks characters (dots/asterisks). | Functional Req: Security |
| TS-15 | P2 | Negative | Verify behavior when submitting the form with empty fields. | Gap #1 (Missing AC) |

## 4. Test Data & Environment
- **Data:**
    - *Pending:* Valid user credentials (Email/Password).
    - *Pending:* User with 2FA enabled.
    - *Pending:* User with SSO enabled.
    - *Pending:* Invalid email formats (e.g., `test.com`, `test@`, `test@@com`).
    - *Pending:* Weak/Strong password examples for validation checks.
- **Environment:**
    - *Pending:* Confirmation of target URL (Production vs. Staging).
    - Browsers: Chrome (Latest), Firefox (Latest), Safari (Latest), Edge (Latest).
    - Devices: Desktop (1920x1080), Tablet (iPad), Mobile (iPhone 14, Pixel 8).
- **Roles:**
    - Standard User.
    - Enterprise User (SSO/2FA).
    - New User (Trial Signup path).

## 5. Risks & Assumptions
- **Risks:**
    - Testing against production (`http://app.vwo.com`) may impact real users or violate security policies if not explicitly approved.
    - Lack of defined rate-limiting thresholds makes security testing for brute force protection impossible without guessing.
    - Ambiguity in "Standard connections" for performance testing may lead to inconsistent results.
- **Assumptions:**
    - The "Light and Dark Mode" mentioned in the banner is a functional toggle or system-preference respect, not just a marketing image.
    - "Clickable Labels" implies that clicking the text label focuses the associated input field.
    - The "Free Trial Signup" link is a separate flow not detailed in this ticket, so only the link's presence/redirect is in scope.

## 6. Entry / Exit criteria
- **Entry Criteria:**
    - Build deployed to the agreed-upon environment.
    - Test data (accounts) provided by the author.
    - Clarifications received for Gaps #1, #3, #4, and #5.
- **Exit Criteria:**
    - All P0 and P1 test scenarios executed and passed.
    - No critical (P0) defects open.
    - Performance metrics (load time) verified against the defined standard.
    - Accessibility audit (WCAG 2.1 AA) completed with no major violations.

---
## HUMAN REVIEW GATE
- **I assumed:** That the URL provided is the target for testing, despite it being HTTP (not HTTPS) in the text, which contradicts the "HTTPS Enforcement" requirement. I assumed this is a typo in the ticket or a staging link.
- **I could not confirm:** The specific error message texts, the rate limiting threshold, the session timeout duration, and whether SSO/2FA are currently active features or just planned.
- **Open questions blocking sign-off:**
    1. What is the exact test environment URL?
    2. What are the specific Acceptance Criteria for error messages and validation?
    3. What is the rate limiting threshold for brute force protection?
    4. Are SSO and 2FA currently live features to be tested?
- ▶ **Approve, or edit, before I write test cases / automation.**
