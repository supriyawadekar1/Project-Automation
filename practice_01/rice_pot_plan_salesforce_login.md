# Plan: Salesforce Login Selenium Framework (RICE POT)

## Goal

Build an **enterprise-grade Selenium + Java + Maven + TestNG** framework that automates and verifies the Salesforce login page (`https://login.salesforce.com/?locale=in`) with valid and invalid test cases.

## Decoded Requirements (RICE POT)

| Component | Requirement |
|---|---|
| **R**ole | QA automation tester, 15 yrs, CRM/Salesforce domain expert |
| **I**nstructions | TestNG annotations (`@Test`, `@BeforeTest`, setup/teardown); robust try-catch exception handling in Page Object + test scripts; PageFactory + `@FindBy` + constructor init + reusable action methods; xpath-only selectors |
| **C**ontext | Salesforce login page with email, password, submit button, remember-me checkbox |
| **E**xample | `LoginPage` pattern with `@FindBy(xpath=...)`, `PageFactory.initElements(driver, this)`, `doLogin(user, pass)` action method |
| **P**arameters | External URLs (incl. staging), external username/password supplied separately; production precision |
| **O**utput | 1 Page Object + 2 TestNG test scripts + Maven project. No explanations/comments |
| **T**one | Technical, precise, enterprise-grade |

## Hard Constraints

- **xpath-only** selectors — no CSS, no `By.id()`, `By.name()`, `By.className()`, etc. (`@id` inside xpath like `//input[@id='username']` is allowed — that's the provided example pattern)
- **No comments** in generated code
- **No `Thread.sleep()`** — use `WebDriverWait` / explicit waits only
- **No bad practices** — no hardcoded credentials; external via config
- **Structured try-catch** exception handling everywhere

## Deliverables

```
practice_01/RICE_POT_SeleniumFramework/
├── pom.xml                          # Selenium 4.x, TestNG 7.x, WebDriverManager 5.x, Surefire
├── testng.xml                       # Suite referencing both test classes
└── src/
    ├── main/java/
    │   └── com/salesforce/
    │       ├── config/
    │       │   └── ConfigReader.java        # Reads config.properties
    │       ├── pages/
    │       │   └── LoginPage.java           # PageFactory + @FindBy (xpath only)
    │       └── utils/
    │           └── WaitUtils.java           # WebDriverWait helpers
    ├── test/java/
    │   └── com/salesforce/
    │       ├── base/
    │       │   └── BaseTest.java            # @BeforeTest / @AfterTest setup & teardown
    │       ├── tests/
    │       │   ├── ValidLoginTest.java      # valid login + remember-me + UI elements
    │       │   └── InvalidLoginTest.java    # wrong pass, empty fields, bad email format
    └── test/resources/
        └── config.properties                # base.url, browser, placeholder credentials
```

## Test Matrix

| Class | Test Cases |
|---|---|
| `ValidLoginTest` | 1. Valid credentials → login success |
| | 2. Remember-me checkbox checked |
| | 3. UI elements rendered (email, password, submit, remember-me visible) |
| `InvalidLoginTest` | 1. Wrong password → error message |
| | 2. Empty username → error message |
| | 3. Empty password → error message |
| | 4. Both empty → error message |
| | 5. Invalid email format → error message |

## Execution Steps

1. **Fetch live DOM** of `https://login.salesforce.com/?locale=in` — extract real xpaths (Salesforce serves locale-specific HTML; fetched DOM is authoritative, prevents hallucinations).
2. **Scaffold Maven project** directory structure.
3. **Write `pom.xml`** — Selenium 4.x, TestNG 7.x, WebDriverManager, Maven Surefire plugin.
4. **Write `config.properties`** — `base.url`, `browser=chrome`, `valid.username=PLACEHOLDER`, `valid.password=PLACEHOLDER`, wait timeouts.
5. **Write `ConfigReader.java`** — loads properties from classpath (no hardcoded credentials).
6. **Write `WaitUtils.java`** — `WebDriverWait` wrappers; zero `Thread.sleep`.
7. **Write `BaseTest.java`** — `@BeforeTest`: WebDriverManager init, maximize, navigate to URL; `@AfterTest`: quit driver. Protected `driver` + `loginPage` fields.
8. **Write `LoginPage.java`** — xpath-only `@FindBy`, `PageFactory.initElements()`, action methods (`doLogin`, `enterUsername`, `enterPassword`, `clickLogin`, `checkRememberMe`, `getErrorMessageText`, `isErrorMessageDisplayed`), all wrapped in try-catch.
9. **Write `ValidLoginTest.java`** — 3 valid test cases (extends BaseTest).
10. **Write `InvalidLoginTest.java`** — 5 invalid test cases (extends BaseTest).
11. **Write `testng.xml`** — suite referencing both test classes.
12. **Verify**:
    - `mvn compile` — zero errors
    - `mvn test` — run with placeholders (may fail at login step if credentials invalid — expected; framework correctness is the goal)
    - Grep checks: no `By.id`, `By.name`, `By.cssSelector`, `By.className`, no `Thread.sleep`, no `//` comments in Java files

## Key Decisions

- **xpath with `@id` allowed** — "don't use ID" = no `By.id()` strategy, not no `@id` in xpath.
- **Config placeholders** — credentials filled in externally; nothing hardcoded.
- **Live DOM first** — step 1 before any xpath is written.
- **8 total test cases** — 3 valid + 5 invalid.

## Known Risks / Limitations

1. **CAPTCHA/SSO**: Real Salesforce org may show CAPTCHA or SSO redirect — automated login could fail. Known limitation.
2. **Credentials**: Login tests need real creds; without them, `mvn test` can't fully pass — use placeholders + document.
3. **Headless mode**: Add `headless=true/false` config flag for CI readiness (easy future add).
4. **Cross-browser**: Structure supports Firefox/Edge branches in BaseTest when needed.

## Open Questions (to confirm before implementation)

1. Where exactly should the project live — `practice_01/RICE_POT_SeleniumFramework/`?
2. Java version target (8 or 11+)? Selenium 4 requires Java 8+.
3. Do you have real Salesforce test credentials to plug in, or keep placeholders?
4. Should the valid-login success assertion target the Salesforce home page (`/one/one.app` or `/lightning/page/home`)?
