# Cypress Test Project

End-to-end testing setup using [Cypress](https://www.cypress.io/).

## Prerequisites

- [Node.js](https://nodejs.org/) (version 18 or higher)
- npm (comes with Node.js)

## Installation

```bash
npm install
```

This installs Cypress and all project dependencies.

## Running Tests

### Open the Cypress Test Runner

```bash
npm run cypress:open
```

The interactive Test Runner lets you run specs individually, watch them live, and debug with the built-in time-travel snapshots.

### Run Tests Headlessly

```bash
npm run cypress:run
```

Runs all specs in the terminal without opening the browser UI. This is the mode used in CI.

### Run a Single Spec

```bash
npx cypress run --spec "cypress/e2e/example.cy.js"
```

## Project Structure

```
cypress/
├── e2e/            # End-to-end test specs (*.cy.js / *.cy.ts)
├── fixtures/       # Static test data (JSON files)
├── support/        # Shared commands, custom assertions, and setup
│   ├── commands.js
│   └── e2e.js
└── downloads/      # Files downloaded during tests (auto-generated)
```

## Configuration

Cypress settings live in `cypress.config.js` at the project root. Common options:

- `baseUrl` — the default URL tests visit
- `viewportWidth` / `viewportHeight` — default browser window size
- `e2e.supportFile` — path to the support file
- `retries` — number of times a failing test retries

## Writing Tests

Add spec files to `cypress/e2e/`. Example:

```js
describe('Example spec', () => {
  it('visits the app and checks the title', () => {
    cy.visit('https://example.cypress.io');
    cy.contains('type').should('exist');
  });
});
```

## CI

Run tests in a CI pipeline with the headless command:

```bash
npm run cypress:run
```

Cypress also provides a [GitHub Action](https://github.com/cypress-io/github-action) for easy integration.

## Documentation

- [Cypress Docs](https://docs.cypress.io/)
- [API Reference](https://docs.cypress.io/api/table-of-contents)
