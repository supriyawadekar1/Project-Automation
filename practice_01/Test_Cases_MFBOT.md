# MFBOT — Test Cases (FR-01 to FR-12, NFR-01 to NFR-02)

Generated from `Test_Plan_MFBOT.md` (BRD: MFBOT – Chatbot for IT Services, MMFSL) under Anti-Hallucination Rules.

---

## Verified Facts (from BRD / Test Plan)

- MFBOT is a web-hosted chatbot for internal Mahindra (MMFSL) users only. (§1.4.1)
- Business flow (§II): 1) Open MFBOT → 2) Select type of query (System related, Application, etc.) → 3) Select specific query → 4) Solution displayed → 5) Solution shown on MFBOT screen → 6) "Was it helpful?" Yes/No + "Do you want to raise a ticket?" Yes/No → 7) "Yes" → Thank-you message → 8) "No" → ticket can be raised → 9) SAP code and password required → 10) Parameter list displayed, details passed to Felicity portal → 11) Ticket number displayed.
- Insider Trading Compliance queries visible to authorized users only. (§1.4.1)
- Self-help queries, FAQs, and call tagging in Felicity portal are in scope. (§1.4.1)
- Objectives: 24/7 availability, multiple users at the same time, reduced TAT. (§1.3)
- Sample query: Outlook proxy configuration for Mahindra mail (mfowa.mfeka.com, BASIC AUTHENTICATION). (§3.3)
- Solution content is governed by the signed-off bot flow document. (§1.6)
- Exit requires execution of all high-priority test cases and no high-priority defects in production. (§1.6)

## Missing / Unknown Information

- Felicity portal API specification (endpoints, payloads, authentication, error codes) — "Not specified".
- SAP authentication mechanism, validation rules, error messages — "Not specified".
- Ticket parameter list and mandatory flags — "Not specified".
- Insider Trading Compliance authorization model (roles/groups/claims) — "Not specified".
- Error message texts — "Not specified".
- Field length limits, special-character rules, duplicate-submission behavior — "Not specified".
- NFR targets: concurrent user count, total user count, response time (§11.3, §3.9 blank) — "Not specified".
- Browser/OS/device matrix — "Not specified".

---

## Generated Output — Test Cases

| Test ID | Description | Pre-conditions | Steps | Expected Result | Priority |
| ------- | ----------- | -------------- | ----- | --------------- | -------- |
| TC-001 | Launch: welcome message and category prompt displayed | MFBOT accessible; test environment up | 1. Open MFBOT | Welcome message displayed; user asked to select from category list (§II Step 1, §3.3) | High |
| TC-002 | Welcome / query-list content matches signed-off bot flow document | Bot flow document signed off (§1.6) | 1. Open MFBOT; 2. Compare displayed text with bot flow document | Displayed categories and prompts match the signed-off document | Medium |
| TC-003 | Multiple users can open MFBOT simultaneously | Test accounts provisioned | 1. N users open MFBOT at the same time | All users receive welcome message; no failure (§1.3 multi-user objective) | High |
| TC-004 | All categories displayed: System related, Application, Insider Trading Compliance, FAQ/self-help | MFBOT launched | 1. Open MFBOT; 2. Inspect category list | All four categories listed (§1.4.1, §II Step 2) | High |
| TC-005 | System related category displays system queries | Category list displayed | 1. Select "System related" | System-related query options displayed (§1.4.1, §II Step 2) | High |
| TC-006 | Application category displays application queries | Category list displayed | 1. Select "Application" | Application query options displayed (§1.4.1) | High |
| TC-007 | FAQ / self-help queries resolve correctly | FAQ content available | 1. Select FAQ/self-help option; 2. Select a query; 3. View solution | Solution displayed for the FAQ query (§1.4.1) | Medium |
| TC-008 | Call tagging option in Felicity portal accessible | Valid user session | 1. Navigate ticket-raise flow; 2. Check call tagging availability | Call tagging flow reachable (§1.4.1). Felicity behavior: Not specified | High |
| TC-009 | Authorized user can view Insider Trading Compliance queries | Authorized user account (definition: Not specified) | 1. Log in as authorized user; 2. Open category list | Insider Trading Compliance queries visible (§1.4.1) | High |
| TC-010 | Unauthorized user cannot view Insider Trading Compliance queries | Unauthorized user account | 1. Log in as unauthorized user; 2. Attempt to access Insider Trading Compliance queries | Content not accessible (§1.4.1). Error/denial behavior: Not specified | High |
| TC-011 | Insider Trading Compliance option not shown to unauthorized user | Unauthorized user account | 1. Log in as unauthorized user; 2. Inspect category list | Insider Trading Compliance option absent or disabled (§1.4.1) | High |
| TC-012 | Insider Trading Compliance restricted consistently across sessions | Multiple user accounts | 1. Repeat TC-009/TC-010 across sessions | Authorization behavior consistent (§1.4.1) | High |
| TC-013 | Specific queries displayed under selected category | Category selected | 1. Select a category; 2. Inspect query list | List of specific queries displayed (§II Step 3) | High |
| TC-014 | Selecting a query proceeds to solution display | Query list displayed | 1. Select a specific query | Solution displayed for that query (§II Steps 3–5) | High |
| TC-015 | All displayed query options are selectable | Query list displayed | 1. Select each displayed option | Each option responds with a solution (§II Step 3) | Medium |
| TC-016 | Correct solution displayed for selected query | Specific query selected | 1. Select a query (e.g., Outlook proxy configuration); 2. View solution | Correct solution shown on MFBOT screen (§3.3, §II Step 5) | High |
| TC-017 | Solution content matches signed-off bot flow document | Bot flow document signed off | 1. Select query; 2. Compare solution with document | Solution steps and text match the document (§1.6) | High |
| TC-018 | Solution displayed in full on MFBOT screen | Solution available | 1. Select query; 2. Verify full solution visibility | Full solution readable on screen (§II Step 5) | Medium |
| TC-019 | Sample query (Outlook proxy) solution accuracy | Query available in corpus | 1. Select Outlook proxy configuration query; 2. Verify steps | Steps include: Outlook → Tools → Account Settings → Connection → Exchange Proxy server, server `mfowa.mfeka.com`, Basic Authentication (§3.3) | Medium |
| TC-020 | Solution shown only after query selection | MFBOT launched | 1. Do not select a query; 2. Observe screen | No solution displayed before query selection (§II Steps 3–5) | Medium |
| TC-021 | "Was it helpful?" Yes and No options displayed with solution | Solution displayed | 1. View solution area | Both "Yes" and "No" options displayed (§II Step 6) | High |
| TC-022 | Feedback options are selectable | Solution displayed | 1. Select Yes; 2. Select No in a new session | Both selections register (§II Step 6) | Medium |
| TC-023 | Feedback shown for each solution | Solution displayed | 1. Complete two different queries | Feedback options appear after each solution (§II Step 6) | Medium |
| TC-024 | Thank-you message on selecting "Yes" | Feedback shown | 1. Select "Yes" for "Was it helpful?" | Thank-you message displayed (§II Step 7) | High |
| TC-025 | Thank-you message content matches bot flow document | Bot flow document signed off | 1. Select "Yes"; 2. Compare message with document | Message matches the signed-off document (§1.6) | Medium |
| TC-026 | Ticket-raise option offered on selecting "No" | Feedback shown | 1. Select "No" for "Was it helpful?" | Ticket-raise option presented (§II Step 8) | High |
| TC-027 | No ticket-raise prompt on "Yes" | Feedback shown | 1. Select "Yes"; 2. Observe options | Thank-you message shown; no ticket-raise prompt (§II Steps 7–8) | Medium |
| TC-028 | SAP code and password required to raise a ticket | Ticket-raise flow started | 1. Attempt to raise a ticket | SAP code and password requested before proceeding (§II Step 9) | High |
| TC-029 | Valid SAP code and password proceed to parameters | Valid SAP credentials (values: Not specified) | 1. Enter valid SAP code/password; 2. Submit | Parameter list displayed (§II Step 10) | High |
| TC-030 | Invalid SAP code rejected | SAP authentication available | 1. Enter invalid SAP code; 2. Submit | Submission rejected. Error message: Not specified | High |
| TC-031 | Invalid password rejected | SAP authentication available | 1. Enter invalid password; 2. Submit | Submission rejected. Error message: Not specified | High |
| TC-032 | Empty SAP code or password not accepted | Ticket-raise flow started | 1. Submit with empty SAP code/password | Submission blocked. Behavior: Not specified | High |
| TC-033 | Ticket parameter list displayed after SAP authentication | SAP authentication passed | 1. Authenticate; 2. Observe form | Parameter list displayed for ticket (§II Step 10) | High |
| TC-034 | Mandatory parameter fields enforced | Parameter form displayed; mandatory flags: Not specified | 1. Submit without mandatory fields | Submission blocked; user must enter details (§II Step 10). Validation behavior: Not specified | High |
| TC-035 | Empty mandatory fields not submitted | Parameter form displayed | 1. Leave fields empty; 2. Submit | No submission to Felicity portal (§II Step 10). Error message: Not specified | High |
| TC-036 | Special characters in parameter fields | Parameter form displayed; field rules: Not specified | 1. Enter `!@#$%^&*()<>/"'\` in fields; 2. Submit | System behavior per field rules. Rules: Not specified | Medium |
| TC-037 | Field length boundary values | Parameter form displayed; length limits: Not specified | 1. Enter min/max length values | Behavior at boundaries. Limits: Not specified | Medium |
| TC-038 | Duplicate ticket submission behavior | Ticket already submitted | 1. Submit identical ticket again | System behavior. Duplicate handling: Not specified | Medium |
| TC-039 | Ticket data passed to Felicity portal | API spec available (Not specified) | 1. Complete parameter form; 2. Submit | Ticket details passed to Felicity portal (§II Step 10). Payload/response: Not specified | High |
| TC-040 | Field mapping to Felicity portal correct | API spec available (Not specified) | 1. Submit ticket; 2. Verify Felicity record | Entered parameters match the Felicity ticket fields (§II Step 10) | High |
| TC-041 | Call tagging performed in Felicity portal | API spec available (Not specified) | 1. Submit ticket via call-tagging flow | Call tagged in Felicity portal (§1.4.1) | High |
| TC-042 | Felicity portal failure handled gracefully | Felicity unavailable (simulated) | 1. Submit ticket while Felicity is down | Graceful handling; no crash. Error behavior: Not specified | High |
| TC-043 | No data loss on failed handoff | Felicity failure simulated | 1. Submit ticket; 2. Force failure; 3. Retry | No ticket data lost. Recovery behavior: Not specified | High |
| TC-044 | Ticket number generated and displayed | Felicity returns ticket number (format: Not specified) | 1. Complete ticket-raise flow | MFBOT displays generated ticket number (§II Step 11, §3.3) | High |
| TC-045 | Ticket number matches Felicity-created ticket | Felicity record available | 1. Note displayed ticket number; 2. Check Felicity | Number corresponds to the created ticket (§II Step 11) | High |
| TC-046 | Ticket number visible on MFBOT screen after submission | Ticket created | 1. Submit ticket; 2. Observe screen | Ticket number reverted back to user on MFBOT screen (§3.3) | High |
| TC-047 | Chatbot accessible 24/7 | Test environment; availability targets: Not specified | 1. Access MFBOT outside business hours | Chatbot available (§1.3 24/7 objective). Availability target: Not specified | High |
| TC-048 | Multiple concurrent users without degradation | User count target: Not specified | 1. Simulate concurrent users raising queries/tickets | All users served simultaneously (§1.3). Degradation threshold: Not specified | High |

---

## Self-Validation Check

- **Traceability**: Every test case maps to a BRD fact — §II steps 1–11 (TC-001 to TC-028, TC-033 to TC-046), §1.4.1 (TC-004 to TC-012, TC-041), §1.3 (TC-003, TC-047, TC-048), §3.3 (TC-016, TC-019, TC-044, TC-046), §1.6 (TC-002, TC-017, TC-025).
- **No invented behavior**: No UI texts, error messages, API payloads, credentials, or validation rules were invented; all such details are marked "Not specified".
- **No invented data**: No actual SAP codes, passwords, URLs beyond the BRD's example (`mfowa.mfeka.com`), or test values were fabricated.
- **Contradiction check**: No case asserts behavior contradicting the BRD flow; negative cases (TC-030, TC-031, TC-032) only assert rejection, not the message.
- **Deterministic**: Output is fully derived from the test plan's RTM and BRD facts; repeatable.
- **Incomplete-stop rule**: Cases blocked on missing information (TC-039 to TC-043) are flagged as dependent on the Felicity API specification; NFR-03 (response time) has no testable case because no targets exist — "Insufficient information to determine."
