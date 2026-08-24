# ENTERPRISE TEST PLAN — MFBOT (Chatbot for IT Services)

## 1. Test Plan Overview

| Item | Detail |
|---|---|
| Project Name | MFBOT – Chatbot for IT Services (PO Module) |
| Application / Product | MFBOT — web-hosted chatbot for internal IT self-help (Mahindra & Mahindra Financial Services Ltd. – MMFSL) |
| Document Version | 1.0 |
| Testing Objective | Validate that MFBOT resolves basic IT queries of internal Mahindra users through a guided self-help flow, operates 24/7 for multiple concurrent users, and correctly raises tickets in the Felicity portal with Insider Trading Compliance content restricted to authorized users. |
| Testing Scope | End-to-end coverage of chatbot flows (launch, category/query selection, solution display, feedback, ticket raising), SAP authentication, Felicity portal integration (incl. call tagging), Insider Trading Compliance authorization, and 24/7 availability/concurrency. |
| Testing Approach | Risk-based, requirement-driven under Agile/Scrum. Functional, UI, API, integration, E2E, regression, smoke, sanity, negative, boundary, data validation, compatibility, security, performance, usability and accessibility testing; automation for regression/API; manual exploratory for UX. |

## 2. Objectives

| ID | Objective | Source |
|---|---|---|
| O1 | 100% coverage of the 11-step business flow (BRD §II) | §II |
| O2 | Verify all query categories: System related, Application, Insider Trading Compliance, FAQ/self-help, call tagging in Felicity portal | §1.4.1 |
| O3 | Verify end-to-end ticket raising: SAP authentication → parameters → Felicity portal → ticket number returned | §II Steps 9–11, §3.3 |
| O4 | Verify Insider Trading Compliance queries are visible only to authorized users | §1.4.1 |
| O5 | Verify 24/7 availability and simultaneous multi-user usage | §1.3 |
| O6 | Release to production with no high-priority open defects | §1.6 |

## 3. Scope

**In Scope**
- Chatbot UI: welcome message, category selection, query list, solution display, "Was it helpful?" feedback, thank-you message, ticket-raise prompt.
- SAP code/password authentication for ticket raising.
- Ticket parameters capture and handoff to Felicity portal; call tagging.
- Insider Trading Compliance authorization (role-based visibility).
- Integration points: Felicity portal, SAP.
- Non-functional: availability (24/7), concurrency, security (authorization).

**Out of Scope**
- No items are explicitly listed as out of scope in the BRD (§1.4.2 is empty). Scope is limited to what the documentation supports.
- External / non-Mahindra users are excluded (chatbot is for internal Mahindra users only — §1.4.1).

## 4. Application / Feature Analysis

| Module / Feature | Requirement Reference | Description | Risk | Priority |
|---|---|---|---|---|
| Chatbot launch & welcome message | §II Step 1, §3.3 | MFBOT opens with a welcome message and category prompt | Low | High |
| Query category selection | §1.4.1, §II Step 2 | Categories: System related, Application, Insider Trading Compliance, FAQs | Medium | High |
| Insider Trading Compliance authorization | §1.4.1 | Content visible only to authorized users | High (security) | High |
| Query list & selection | §II Step 3 | Specific queries displayed under each category | Low | High |
| Solution display | §II Steps 4–5 | Correct solution for selected query (e.g., Outlook proxy configuration — §3.3) | Medium | High |
| Feedback "Was it helpful?" | §II Step 6 | Yes/No options alongside solution | Low | High |
| Thank-you message | §II Step 7 | Displayed on "Yes" | Low | Medium |
| Ticket-raise initiation | §II Step 8 | Offered when user is not satisfied | Medium | High |
| SAP authentication | §II Step 9 | SAP code + password required to raise a ticket | High (security/integration) | High |
| Ticket parameters form | §II Step 10 | Parameter list captured for the ticket | Medium | High |
| Felicity portal integration & call tagging | §1.4.1, §II Step 10, §3.3 | Ticket details passed to Felicity portal | High (integration) | High |
| Ticket number display | §II Step 11, §3.3 | Generated ticket number reverted to user on MFBOT screen | Medium | High |
| 24/7 availability & concurrency | §1.3 | Solution to multiple users at the same time, round-the-clock | High (NFR) | High |

## 5. Test Strategy

| Test Type | Objective | Scope | Approach | Applicability |
|---|---|---|---|---|
| Functional testing | Verify business rules and each step of the §II flow | All modules | Requirement-based test cases; manual + automated execution | Yes — all |
| UI testing | Verify web UI layout, navigation, prompts, readability | All chatbot screens | Visual/inspector checks; layout walkthroughs | Yes |
| API testing | Verify Felicity portal handoff: payload, field mapping, response, error handling | Ticket-raise integration | Contract validation; request/response testing (API spec to be obtained — OQ-01) | Yes |
| Integration testing | Chatbot ↔ SAP ↔ Felicity portal; call tagging | Cross-system journey | End-to-end data flow with test stubs | Yes |
| End-to-end testing | Full journey: launch → solution → feedback → ticket → ticket number | Complete flow | Scripted E2E scenarios | Yes |
| Regression testing | Ensure fixes/new builds do not break existing flow | All modules | Automated regression suite per sprint | Yes |
| Smoke testing | Build acceptance of core flow after deploy | Launch, category, solution, feedback | Minimal critical-path checks on each build | Yes |
| Sanity testing | Verify targeted fixes | Fixed modules | Focused re-checks after minor changes | Yes |
| Negative testing | Invalid SAP credentials, unauthorized access to Insider Trading Compliance, no selection, empty inputs | SAP auth, authorization, flow | Invalid-data test cases | Yes |
| Boundary testing | Field lengths, empty/max-length parameters, long query lists | Parameters form, solution content | Boundary value analysis | Yes |
| Data validation | Mandatory vs. optional parameters, special characters, duplicates | Parameters form | Data-driven cases | Yes |
| Compatibility testing | Browsers, OS, devices | UI across environments | Cross-browser/device matrix (matrix unspecified — OQ-05) | Yes (pending matrix) |
| Security testing | Insider Trading Compliance authorization, SAP credential handling, session management | Authorization, auth | Role-based access tests, credential handling review (BRD §7.2 empty — OQ-04) | Yes |
| Performance testing | 24/7 availability, concurrent users, response times | NFR | Load/concurrency testing (targets unspecified — OQ-06) | Yes (pending targets) |
| Usability testing | Self-help intuitiveness, clarity of prompts and solutions | Chatbot flows | Exploratory testing with internal users | Yes |
| Accessibility testing | WCAG compliance | UI | Accessibility scan + manual keyboard/screen-reader checks | Conditional (not specified — assumption) |

## 6. Test Scenarios

| Scenario ID | Requirement ID | Module | Test Scenario | Priority | Test Type |
|---|---|---|---|---|---|
| TS-01 | FR-01 | Launch | Verify MFBOT opens and displays welcome message with category prompt | High | Functional |
| TS-02 | FR-02 | Categories | Verify all categories displayed (System related, Application, Insider Trading Compliance, FAQ/self-help) | High | Functional |
| TS-03 | FR-03 | Authorization | Verify Insider Trading Compliance visible only to authorized users | High | Security |
| TS-04 | FR-04 | Query list | Verify specific queries listed under a selected category | High | Functional |
| TS-05 | FR-05 | Solution | Verify correct solution displayed for selected query (e.g., Outlook proxy configuration) | High | Functional |
| TS-06 | FR-06 | Feedback | Verify "Was it helpful?" Yes/No shown with solution | High | Functional |
| TS-07 | FR-07 | Thank-you | Verify thank-you message on "Yes" | Medium | Functional |
| TS-08 | FR-08 | Ticket raise | Verify ticket-raise prompt on "No" | High | Functional |
| TS-09 | FR-09 | SAP auth | Verify SAP code + password required; invalid credentials rejected with error | High | Negative |
| TS-10 | FR-10 | Parameters | Verify parameter form displayed and mandatory-field validation | High | Data validation |
| TS-11 | FR-11 | Felicity integration | Verify ticket data passed to Felicity portal with correct field mapping and call tagging | High | Integration |
| TS-12 | FR-12 | Ticket number | Verify generated ticket number returned and displayed to user | High | Integration |
| TS-13 | NFR-01 | Availability | Verify chatbot accessible 24/7 | High | Performance |
| TS-14 | NFR-02 | Concurrency | Verify multiple users simultaneously without degradation | High | Performance |
| TS-15 | FR-05 | Solution content | Verify solution content accuracy against signed-off bot flow document | Medium | Functional |
| TS-16 | FR-02 | FAQs | Verify FAQ/self-help queries resolve correctly | Medium | Functional |

## 7. Test Case Strategy

- **Preconditions**: user on corporate network; test environment up; bot flow document signed off; SAP/Felicity test endpoints available; test accounts provisioned.
- **Test data**: per Section 9; externalized per module (categories, queries, solutions, credentials, parameters).
- **Test steps**: numbered, Given–When–Then style, one action per step, explicit expected results per step.
- **Positive scenarios**: happy-path flow (TS-01 → TS-07), complete ticket-raise flow (TS-08 → TS-12).
- **Negative scenarios**: invalid SAP code/password, unauthorized Insider Trading Compliance access, empty/malformed parameter inputs.
- **Boundary conditions**: min/max field lengths, single vs. large query lists, rapid successive interactions.
- **Error handling**: Felicity/SAP downtime, connection failure, invalid inputs — verify graceful, user-friendly errors and no data loss.
- **Alternate flows**: "No" on helpful → ticket raise; "Yes" on helpful → thank-you; retry after failed submission.

## 8. Requirement Traceability (RTM)

| Requirement ID | Requirement | Test Scenario IDs | Test Case IDs | Coverage | Status |
|---|---|---|---|---|---|
| FR-01 | Welcome message on launch | TS-01 | TC-001 – TC-003 | 100% | To be designed / executed |
| FR-02 | Category display (incl. FAQ) | TS-02, TS-16 | TC-004 – TC-008 | 100% | To be designed / executed |
| FR-03 | Insider Trading Compliance authorization | TS-03 | TC-009 – TC-012 | 100% | To be designed / executed |
| FR-04 | Query list under category | TS-04 | TC-013 – TC-015 | 100% | To be designed / executed |
| FR-05 | Solution display & content accuracy | TS-05, TS-15 | TC-016 – TC-020 | 100% | To be designed / executed |
| FR-06 | "Was it helpful?" feedback | TS-06 | TC-021 – TC-023 | 100% | To be designed / executed |
| FR-07 | Thank-you message | TS-07 | TC-024 – TC-025 | 100% | To be designed / executed |
| FR-08 | Ticket-raise prompt on "No" | TS-08 | TC-026 – TC-027 | 100% | To be designed / executed |
| FR-09 | SAP authentication | TS-09 | TC-028 – TC-032 | 100% | To be designed / executed |
| FR-10 | Ticket parameters capture & validation | TS-10 | TC-033 – TC-038 | 100% | To be designed / executed |
| FR-11 | Felicity portal handoff & call tagging | TS-11 | TC-039 – TC-043 | 100%* | Blocked — API spec required (OQ-01) |
| FR-12 | Ticket number display | TS-12 | TC-044 – TC-046 | 100% | To be designed / executed |
| NFR-01 | 24/7 availability | TS-13 | TC-047 | Not testable — targets not specified | Info missing (OQ-06) |
| NFR-02 | Concurrency / multi-user | TS-14 | TC-048 | Not testable — user counts not specified (§11.3 blank) | Info missing (OQ-06) |
| NFR-03 | Response time | — | — | Not testable — no targets (§3.9 blank) | Info missing (OQ-06) |

\* Coverage planned; execution blocked until Felicity portal API specification is provided.

## 9. Test Data Strategy

- **Valid data**: valid SAP code/password; authorized user credentials; valid category/query selections (to be provided).
- **Invalid data**: invalid SAP credentials; unauthorized user; empty fields; malformed values.
- **Boundary data**: min/max length parameter values (limits to be confirmed — OQ-02).
- **Mandatory/optional data**: ticket parameter list with mandatory flags (to be provided — OQ-02).
- **Duplicate data**: repeated ticket submissions, duplicate SAP code entries.
- **Special characters**: field inputs with `!@#$%^&*()<>/"'\` characters.
- **Large-volume data**: high concurrent user load; large query lists/solution text.
- **Role-specific data**: authorized vs. non-authorized users for Insider Trading Compliance.
- **API request/response data**: Felicity portal payloads and response codes (to be obtained — OQ-01).
- No actual values are invented; all are flagged "to be provided" where the BRD does not specify them.

## 10. Environment Requirements

| Item | Requirement | Status |
|---|---|---|
| Application environments | Dev, SIT, UAT, Production | Not specified — to be confirmed |
| Browsers | Not specified | To be confirmed (OQ-05) |
| Devices / OS | Not specified (§4.2.1 blank) | To be confirmed (OQ-05) |
| Database | RDBMS not specified (§4.2.1 blank) | To be confirmed |
| API environment | Felicity portal test endpoint; SAP test instance | To be provided |
| Third-party integrations | Felicity portal, SAP | To be confirmed |
| Test accounts | Internal Mahindra user; authorized Insider Trading Compliance user; SAP credentials | To be provided |
| Configuration | Hosting, bandwidth, localization (§4.3 blank) | To be confirmed |

## 11. Automation Strategy

| Candidate | Reason for Automation Suitability | Tooling Direction |
|---|---|---|
| UI automation (core chatbot flow) | Stable, high-frequency, deterministic flow | Selenium / Cypress with Page Object Model |
| API automation (Felicity handoff) | Contract-stable, fast execution | REST Assured / Postman + Newman |
| Regression automation | Repeated per sprint; must not break existing flow | Integrated with UI/API suites |
| Data-driven testing | Multiple categories/queries/solutions share the same flow | CSV/Excel external test data |
| CI/CD integration | Smoke on every deploy; regression on demand | Jenkins / Azure DevOps pipeline |

## 12. Entry Criteria

- Requirements collection from internal Mahindra users and call reports complete (§1.5).
- Requirements analysis and documentation complete (§1.5).
- Structural bot flow document designed (§1.5).
- Coding complete and build deployed to test environment (§1.5).
- Test environment set up (§1.5).
- Test cases/scripts ready (§1.5).
- Felicity portal and SAP test endpoints available (not specified in BRD — flagged).
- Test data provisioned (not specified in BRD — flagged).

## 13. Exit Criteria

- Circle Head – IT signs off the Functional Requirement document / bot flow document (§1.6).
- All high-priority test cases executed (§1.6).
- High-risk identified areas taken up and tested (§1.6).
- Build successfully deployed to production with no high-priority defects (§1.6).
- Deadlines reached (§1.6).
- Regression cycle completed; defect backlog within agreed limits (thresholds not specified in BRD — flagged).

## 14. Defect Management

- **Identification**: defects found in functional, integration, security, and performance testing.
- **Logging**: single defect tracking tool (JIRA/ALM); mandatory fields: summary, steps, expected/actual, severity, priority, environment, attachments.
- **Severity**: Blocker / Critical / Major / Minor / Trivial.
- **Priority**: P1 – P4 (P1 = must fix before release per §1.6 no-high-priority-defects rule).
- **Lifecycle**: New → Assigned → Open → Fixed → Retest → Verified → Closed (Reopen on failure).
- **Retesting**: executed on latest build after fix; verified by reporter.
- **Regression**: full/impacted-area regression after each fix cycle.
- **Closure criteria**: no open P1/P2 defects; all fixes verified; duplicates/rejected resolved with rationale.

## 15. Risks and Mitigation

| Risk ID | Risk | Impact | Probability | Mitigation | Contingency |
|---|---|---|---|---|---|
| R-01 | Insider Trading Compliance data exposed to unauthorized users | High | Medium | Role-based access test cases (TS-03), security review | Revoke access, patch, full retest |
| R-02 | Felicity portal integration failure / ticket data loss | High | Medium | Early integration testing, contract validation, test stubs | Manual fallback ticket logging process |
| R-03 | SAP authentication unavailable / rejects valid users | High | Medium | Test against SAP test instance; mock-based testing | Graceful error message; alternate auth path |
| R-04 | Performance under concurrent usage unknown (no targets) | Medium | High | Capacity profiling with realistic estimates; early load testing | Infrastructure tuning; revised NFR targets |
| R-05 | Solution content inaccuracy causing user distrust | Medium | Medium | Content validation against signed-off bot flow doc (TS-15) | Content fix cycle with business sign-off |
| R-06 | 24/7 availability downtime | Medium | Medium | Availability monitoring; failover verification | Ops runbook; RCA per incident |

## 16. Dependencies

- **Development**: bot flow implementation, build deployment.
- **APIs**: Felicity portal API specification, endpoint and test credentials; SAP authentication service.
- **Database**: chatbot content store, ticket store (specs to be confirmed).
- **Third-party systems**: Felicity portal, SAP.
- **Test environments**: environment setup, configuration.
- **Test data**: user accounts, SAP credentials, authorized-user accounts, content corpus.
- **External services**: corporate network access, 24/7 hosting.
- **Business stakeholders**: Circle Head – IT sign-off (§1.6), content owners for solution accuracy.

## 17. Assumptions

- ASSUMPTION-01: Scope is derived solely from the supplied BRD (MFBOT chatbot). The login-page context in the task template is not part of this BRD and is excluded.
- ASSUMPTION-02: Internal users access MFBOT via the corporate network; session authentication method (SSO/LDAP) is not specified in the BRD.
- ASSUMPTION-03: Felicity portal and SAP provide test endpoints/stubs for SIT.
- ASSUMPTION-04: Solution content is finalized and available in the signed-off bot flow document.
- ASSUMPTION-05: 24/7 availability permits only approved maintenance windows (BRD §11.5 blank).
- ASSUMPTION-06: Reports described in §3.6 (PR device report links) appear to be template remnants unrelated to the chatbot; applicability requires confirmation (OQ-08).

## 18. Open Questions

| ID | Priority | Question | Owner |
|---|---|---|---|
| OQ-01 | Critical | Where is the Felicity portal API specification (endpoints, payloads, authentication, error codes)? | Developer / Architect |
| OQ-02 | Critical | What are the exact ticket parameters and which are mandatory? | Business Analyst |
| OQ-03 | Critical | How is the SAP code/password authenticated? What are the credential validation rules and error messages? | Developer / Architect |
| OQ-04 | High | How is an "authorized user" for Insider Trading Compliance defined and enforced (roles, groups, SSO claims)? | Product Owner / Architect |
| OQ-05 | High | What browsers, OS, and devices must be supported? | Product Owner |
| OQ-06 | High | Expected concurrent user count, total user count, and response time targets (§11.3, §3.9 blank)? | Product Owner / Architect |
| OQ-07 | Medium | Test environment details: URLs, database, hosting, bandwidth, localization (§4.2, §4.3 blank)? | Test Manager / DevOps |
| OQ-08 | Medium | Is §3.6 (report links for PR devices) applicable to the chatbot, or a template remnant? | Business Analyst |
| OQ-09 | Medium | Session timeout, chatbot language(s), and multilingual support? | Product Owner |
| OQ-10 | Low | Does §7.2 "Security and Privacy" imply additional compliance requirements (access logging, PII)? | Architect / Compliance |

## 19. Deliverables

- Test Plan (this document)
- Test Scenarios
- Test Cases (with preconditions, data, steps, expected results)
- Requirement Traceability Matrix (RTM)
- Test Data (with externalized credentials/content corpus)
- Automation Scripts (UI + API)
- Defect Reports
- Test Execution Reports (per cycle/sprint)
- Test Summary Report (per release)

## 20. Overall Test Coverage Assessment

- **Requirements identified**: 16 (FR-01 – FR-12 functional, NFR-01 – NFR-03 non-functional, plus business rules from §1.3/§1.4.1/§II).
- **Requirements covered by designed scenarios**: 15 of 16 (all FRs + NFR-01/NFR-02 at scenario level).
- **Requirements with insufficient information**: NFR-01/NFR-02/NFR-03 (no performance targets, no user counts — §3.9, §11.3 blank); FR-11 execution blocked pending API spec (OQ-01); FR-10 details pending parameter list (OQ-02).
- **High-risk areas**: Insider Trading Compliance authorization (security), Felicity portal integration, SAP authentication, 24/7 concurrency.
- **Critical gaps**: no Felicity API specification; no SAP authentication specification; no environment/hardware specs (§4.2 blank); no NFR targets; browser/device matrix unspecified.
- **Recommended next actions**:
  1. Obtain Felicity portal API specification and SAP authentication details (OQ-01, OQ-03) — unblocks TS-09/TS-11/TC-028–043.
  2. Confirm authorization model for Insider Trading Compliance (OQ-04).
  3. Define NFR targets (concurrency, response time, availability) (OQ-06).
  4. Confirm supported browsers/devices and environment details (OQ-05, OQ-07).
  5. Confirm applicability of §3.6 reports and §7.2 security requirements (OQ-08, OQ-10).
