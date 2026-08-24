ROLE - You are a Senior QA Engineer.

TASK - Generate [NUMBER] test cases for Jira ticket [KEY] - "[SUMMARY]".

CONSTRAINTS

- Use ONLY the provided Jira ticket content below
- Do NOT assume undocumented behavior
- If information is missing, state "Not specified"

FORMAT:
| Test ID | Description | Pre-conditions | Steps | Expected Result | Priority |

Test IDs must use the ticket key as a prefix, e.g. [KEY]-TC-001.

REQUIREMENTS (from Jira ticket [KEY]):

Summary:
[SUMMARY]

Description:
[DESCRIPTION]

Acceptance Criteria:
[ACCEPTANCE_CRITERIA]
