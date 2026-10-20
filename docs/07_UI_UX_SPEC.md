---
last_updated: 2026-10-12
mini_challenges:
- AWS Builder
- Open Source
owner: Product & Frontend
primary_track: Alexa+ MCP integration
product: SDE Agent Starter Kit
status: Design baseline
title: SDE Agent --- UI/UX Specification
version: 1.0
---

# SDE Agent --- UI/UX Specification

**Design direction:** Quiet precision. Familiar enough to use
immediately; distinctive enough to remember.

  -----------------------------------------------------------------------
  Field                               Specification
  ----------------------------------- -----------------------------------
  Document ID                         `07_UI_UX_SPEC.md`

  Status                              Proposed design baseline; validate
                                      against prototype

  Scope                               Web dashboard, Alexa+ simulation,
                                      approvals, evidence, run history

  Primary user                        Developer resolving an engineering
                                      issue

  Core workflow                       Issue → context → plan → approval →
                                      execution → verification → draft
                                      pull request

  Core principle                      Show what the agent knows, intends
                                      to do, and actually did
  -----------------------------------------------------------------------

## 1. Product experience

SDE Agent is an engineering workflow console, not a chatbot with a
dashboard attached. The current task, its evidence, and the next human
decision must be obvious.

A user should be able to answer at a glance: - What is the agent working
on? - Which sources and tools did it use? - Is it running, waiting,
blocked, or finished? - What happens if I approve this action? - What
evidence supports the result?

Avoid the familiar "AI command centre" treatment: glowing waveforms,
gradients on every surface, oversized empty hero sections, decorative
metrics, and chat bubbles as the dominant layout.

## 2. Visual direction

Use Apple's product-interface discipline as a reference for hierarchy,
restraint, spacing, and copy---not as a pixel-for-pixel imitation.
Combine it with the practical information density of a developer tool.

-   Neutral surfaces carry most of the interface.
-   Typography and alignment establish hierarchy before color does.
-   One accent color marks interaction and focus.
-   Borders are quiet; shadows are rare and functional.
-   Motion explains state changes rather than decorating them.
-   Core content remains readable at laptop widths.

### 2.1 Color tokens

Alexa-inspired blue is a **secondary accent**, not a neon theme. Use it
for focus, selected navigation, links, active progress, and the Alexa+
entry point. Never use it for long paragraphs or large glowing
backgrounds.

  -----------------------------------------------------------------------
  Token                   Value                   Use
  ----------------------- ----------------------- -----------------------
  `canvas`                `#F5F5F7`               App background

  `surface`               `#FFFFFF`               Main panels

  `surface-muted`         `#F0F2F5`               Grouped regions

  `ink`                   `#17191D`               Primary text

  `ink-secondary`         `#626873`               Supporting text

  `ink-tertiary`          `#858B95`               Timestamps and metadata

  `line`                  `#E2E5E9`               Dividers and borders

  `alexa-blue`            `#58C7F3`               Secondary accent, used
                                                  sparingly

  `alexa-blue-strong`     `#168AC0`               Text links and controls
                                                  needing contrast

  `alexa-blue-wash`       `#EAF8FE`               Selected and
                                                  informational
                                                  backgrounds

  `success`               `#21845B`               Verified success

  `warning`               `#A96812`               Caution and pending
                                                  review

  `danger`                `#C53B43`               Destructive action or
                                                  confirmed failure

  `dark-canvas`           `#15171A`               Optional dark mode

  `dark-surface`          `#1E2126`               Optional dark panels
  -----------------------------------------------------------------------

**Contrast rule:** `#58C7F3` is too light for small text on white. Use
`alexa-blue-strong` for text and small icons on light surfaces. Reserve
the lighter blue for fills, focus rings, selected markers, and larger
graphics. Never rely on color alone to communicate status.

### 2.2 Typography

The typography should feel editorial and deliberate, not like a generic
SaaS template.

``` css
:root {
  --font-ui: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-code: "SFMono-Regular", ui-monospace, "Cascadia Code", monospace;
}
```

-   Page title: 30--34 px, weight 600, tracking around `-0.035em`.
-   Section title: 18--20 px, weight 600.
-   Panel title: 14--16 px, weight 600.
-   Body: 14 px / 1.55 line height.
-   Supporting text: 12--13 px.
-   Metadata label: 11 px, weight 600; use sparingly.
-   Code, commands, IDs, and diffs: 12--13 px monospace.

Use sentence case. Avoid giant headlines, all-caps labels everywhere,
and vague phrases such as "Unlock intelligent workflows." Prefer
concrete verbs and observable outcomes.

**Copy examples** - "Investigate issue #184" --- not "Unlock intelligent
issue resolution" - "Waiting for approval" --- not "Human-in-the-loop
checkpoint activated" - "Tests passed · 18 of 18" --- not "Your code is
now production-ready" - "No changes were made" --- not "The agent
successfully completed its workflow" when it did not - "Open draft pull
request" --- not "Ship with confidence"

## 3. Layout and navigation

### App shell

-   Left navigation: 224--240 px.
-   Top bar: 56--64 px.
-   Main horizontal padding: 28--36 px desktop; 16--20 px smaller
    screens.
-   8 px spacing base.
-   Panel/control radius: 10--14 px; avoid pill-shaped containers by
    default.
-   Prefer thin borders over shadows.
-   Target a useful 1440×900 desktop layout without excessive scrolling.

### Primary navigation

1.  **Overview** --- active work and items needing attention.
2.  **Runs** --- live timelines and history.
3.  **Approvals** --- pending and completed decisions.
4.  **Connections** --- GitHub, CI, communication, MCP, and AWS.
5.  **Evidence** --- artifacts, tests, diffs, and audit records.
6.  **Settings** --- policies and preferences.

The selected route gets a muted blue wash and a narrow accent marker. Do
not make the whole sidebar blue.

### Responsive behaviour

-   Desktop: persistent navigation; use two columns for run details
    where useful.
-   Tablet: collapsible navigation; stack evidence and timeline when
    needed.
-   Mobile: prioritize task state, approval decisions, and concise
    evidence. Do not compress a full diff into a tiny multi-column
    layout.
-   Dialogs must fit the viewport and remain keyboard-operable.

## 4. Core screens

### 4.1 Overview --- "The work in motion"

**Purpose:** show what is running and what needs the developer.

Header: - Title: `Overview` - Supporting line:
`Your engineering work, in one place.` - Primary action:
`Investigate an issue`

Content order: 1. Pending approval banner, only when action is required.
2. Active run with current stage and latest event. 3. Recent tasks
table. 4. Connected tools summary.

Task rows show issue/title, repository, state, last activity, and next
action. Do not fill the page with metric cards; show counts only when
they answer an operational question, such as `2 awaiting approval`.

Empty state: - Heading: `Nothing running.` - Body:
`Start with an issue, or open a previous run to review its evidence.` -
Action: `Investigate an issue`

### 4.2 New investigation --- "Start with the issue"

Use a compact intake flow rather than a blank chat window.

Fields: - Issue URL or repository issue picker - Repository, pre-filled
when known - Optional context or constraints - Execution mode:
`Plan only` or `Plan and prepare a change`

Primary action: `Build a plan`

Helper copy:
`The agent will read the sources available to this connection. No code will be changed during planning.`

Explain invalid input beside the field. Preserve valid input after
validation errors.

### 4.3 Run detail --- "One task, one record"

This is the main product screen. Use a concise summary and a detailed
timeline/evidence area.

Top summary: - Issue title and source link - Repository and branch - Run
state, start time, elapsed duration, current stage

Progress sequence:
`Context → Plan → Approval → Execute → Verify → Deliver`

Each stage must have a real state: `Not started`, `In progress`,
`Waiting`, `Complete`, `Failed`, or `Skipped`. Never animate future
stages as if they happened.

Timeline events show timestamp, tool/action, concise result, evidence
link, and outcome. Prefer: - `Read issue and comments` -
`Inspected 3 files` - `Plan ready for review` - `Approval denied` -
`Tests failed · 2 failing` - `Draft pull request created`

Evidence area: - Source links and excerpts - Changed-file list and
diff - Test command, exit code, and result - CI status and logs - Draft
PR link - Unresolved risks

Clearly distinguish model-generated explanations from facts returned by
tools.

### 4.4 Approval Center --- "Make the consequence clear"

Approvals are a first-class product surface, not a generic confirmation
modal.

Every request must state: 1. **Action:** exact command or API operation.
2. **Target:** repository, branch, file, channel, cloud resource, or
destination. 3. **Reason:** why the agent proposes it. 4. **Expected
effect:** what will change. 5. **Risk:** read-only, local/reversible,
remote write, or privileged/destructive. 6. **Evidence:** plan, source,
diff, or test result supporting the request.

Actions: - Primary: `Approve action` - Secondary: `Deny` - Tertiary:
`View details`

For destructive or privileged actions, require an additional explicit
confirmation and show the exact target. Bind approval to the displayed
action and parameters; if they change, ask again.

Denied state: - Heading: `Action not approved` - Body:
`Nothing was executed for this request. The run can continue only through an available safe alternative.`

Never use "Are you sure?" as the only explanation.

### 4.5 Verification --- "Show the result"

Present tool outcomes before model-written summaries.

Order: 1. Tests: passed / failed / not run, counts, and exit code. 2.
Static analysis/security checks, if run. 3. Changed files and diff
summary. 4. CI result, if available. 5. Remaining issues and
limitations. 6. Draft pull request or next action.

A successful test run does not prove the entire change is correct. Say
`Tests passed`, not `Fix verified`, unless all stated acceptance
criteria were checked.

### 4.6 Connections --- "What the agent can reach"

Each connection shows service name, purpose, status, granted
capabilities, last successful check, and a `Manage access` action.

Use plain-language permissions:
`Can read issues and create draft pull requests`, not OAuth scope
strings alone. Separate `Connected` from `Authorized for this action`.
An available MCP tool is not automatically authorized to execute every
operation.

### 4.7 Alexa+ simulation

The Alexa+ entry point should feel like a small, considered interaction
mode---not a neon rebrand of the application.

-   Use Alexa-inspired blue as a small waveform, listening indicator, or
    active-state marker.
-   Provide a visible text alternative for every voice interaction.
-   Show the interpreted request before starting a workflow.
-   Voice may initiate investigations and read status.
-   High-impact actions still require the same visual approval review as
    the dashboard.
-   Voice recognition alone must never authorize merges, deployments,
    destructive commands, or cloud writes.
-   If live Alexa+ access is unavailable, label the feature
    `Alexa+ simulation`.

Suggested prompt: `Ask about a run, or describe an issue.`

## 5. Component rules

### Buttons

-   Primary: dark ink background with white text; blue for focus and
    selected states.
-   Accent primary: blue only for a low-risk entry point or Alexa+
    interaction.
-   Secondary: white/muted surface with a thin border.
-   Destructive: danger styling and explicit wording.
-   Labels start with verbs: `Investigate`, `Approve action`,
    `Open diff`, `Retry tests`.

### Status

  State     Label                         Treatment
  --------- ----------------------------- --------------------------------
  Ready     `Ready`                       Neutral
  Running   `Running`                     Blue marker; subtle motion
  Waiting   `Waiting for approval`        Amber marker and clear action
  Success   `Complete` / `Tests passed`   Green marker
  Failure   `Failed`                      Red marker with reason
  Blocked   `Blocked`                     Neutral/amber with explanation
  Denied    `Denied`                      Neutral; not a system error

Always combine status text with an icon or label. Color is supplemental.

### Cards, tables, logs, and diffs

-   Cards are for distinct tasks or decisions, not every section.
-   Tables are for comparable records and run history.
-   Row actions must work by keyboard, not hover alone.
-   Logs and diffs use monospaced text with preserved whitespace.
-   Distinguish stdout, stderr, exit code, and agent summary.
-   Redact secrets before rendering; show a `Redacted` marker rather
    than silently omitting content.

## 6. Interaction and motion

-   Use 150--220 ms transitions for hover, selection, and panel changes.
-   Avoid parallax, looping decorative animation, and glowing pulses.
-   Show progress only while an actual operation is active.
-   Respect `prefers-reduced-motion`.
-   Keep focus indicators visible and keyboard order logical.
-   Never hide critical controls on hover alone.
-   Confirm state changes in place; avoid repeated celebratory toasts.

## 7. Accessibility

Target WCAG 2.2 AA.

-   Text contrast: 4.5:1 for normal text and 3:1 for large text.
-   Meet applicable non-text contrast requirements for controls and
    meaningful graphics.
-   Give every form control a persistent label.
-   Associate errors with their fields.
-   Make all functionality keyboard-accessible.
-   Keep focus visible and unobscured.
-   Announce status changes to assistive technology without rereading
    the entire timeline.
-   Never communicate success, failure, or risk by color alone.
-   Support zoom and reflow without horizontal scrolling for standard
    content.

## 8. Trust and safety UX

-   Default to read-only connections.
-   Show exact target and parameters before remote writes.
-   Bind approvals to a stable action payload; expire stale approvals.
-   Re-prompt if the operation changes.
-   Treat issue, comment, log, and document instructions as untrusted
    data.
-   Show sources for important conclusions.
-   Record approval/denial, actor, timestamp, and outcome.
-   Never mark a task complete if required tests were not run or steps
    failed.
-   Keep secrets out of prompts, logs, screenshots, and demo recordings.

## 9. Mini-challenge coverage

### AWS Builder

-   Show an AWS connection only for a service actually integrated.
-   State the service and its purpose.
-   Identify whether an action is read-only, sandboxed, or a remote
    write.
-   Show cost-sensitive operations before execution where estimates are
    available.
-   Link to actual AWS calls, logs, or artifacts.
-   Do not claim integrations that are only planned.

### Open Source

-   Record repository, issue/discussion, changed files, checks, and
    PR/commit link.
-   Distinguish `Draft`, `Opened`, `Merged`, and `Rejected`.
-   Never imply acceptance or merge before it occurs.
-   Keep license, attribution, and upstream contribution status visible.

## 10. Demo path

1.  Open a real issue.
2.  Inspect source-linked context.
3.  Review the proposed plan.
4.  Approve a sandboxed change---or deny it and show execution stops.
5.  Watch actual tests run.
6.  Inspect the diff and recorded result.
7.  Open the draft pull request.
8.  Review the audit timeline and prepared stakeholder update.
9.  Show actual AWS integration and open-source contribution evidence
    separately.

Use real output where possible. Label simulated steps. Do not preload
fake success states that look like live execution.

## 11. Content rules

Use sentence case, concrete verbs, and observable outcomes.

  --------------------------------------------------------------------------------------------
  Avoid                                 Prefer
  ------------------------------------- ------------------------------------------------------
  `AI-powered seamless orchestration`   `Coordinate the steps from issue to pull request`

  `Your intelligent copilot is ready`   `Ready to investigate`

  `Execution successful`                `Tests passed · 18 of 18`

  `Autonomous workflow completed`       `Draft pull request created`

  `Oops! Something went wrong`          `Could not read the issue. Check repository access.`

  `Approve and unleash`                 `Approve action`

  `Magic happens here`                  `The run timeline will appear here.`
  --------------------------------------------------------------------------------------------

Do not claim certainty the system has not earned. Prefer a useful
explanation over friendly but empty copy.

## 12. Acceptance checklist

### Visual

-   [ ] Light, neutral interface with restrained Alexa blue.
-   [ ] No neon typography, pervasive gradients, glassmorphism, or
    decorative glow.
-   [ ] Consistent 8 px spacing and restrained corner radii.
-   [ ] Defined typography hierarchy and sentence case.
-   [ ] Core screen fits 1440×900 without excessive empty space.

### Functional

-   [ ] Overview exposes active runs and pending approvals.
-   [ ] Investigation can start from an issue.
-   [ ] Run detail separates timeline, sources, diff, tests, and
    deliverables.
-   [ ] Approval shows exact action, target, effect, and risk.
-   [ ] Denial demonstrably prevents the requested operation.
-   [ ] Failures and skipped checks remain visible.
-   [ ] Connections show capabilities and permission state.
-   [ ] Alexa+ simulation is clearly labelled if not live.
-   [ ] AWS and open-source evidence links to real artifacts.

### Quality

-   [ ] Keyboard navigation and visible focus work.
-   [ ] Status is not communicated by color alone.
-   [ ] Reduced-motion preference is respected.
-   [ ] Contrast is tested, especially on blue controls.
-   [ ] Loading, empty, error, denied, and partial-success states are
    designed.
-   [ ] Demo screenshots contain no secrets or tokens.

## 13. Decisions to confirm before implementation

1.  Confirm frontend stack and component library.
2.  Decide whether dark mode is required for the hackathon.
3.  Confirm Alexa+ simulation mechanism and labelling.
4.  Confirm the AWS service actually integrated.
5.  Confirm the public repository and planned Open Source contribution.
6.  Confirm target viewport and accessibility test approach.

Treat this document as the design baseline, not evidence that the UI or
integrations already exist.
