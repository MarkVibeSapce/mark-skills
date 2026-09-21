---
name: ux-ui-review
description: UX/UI review for all user types across every screen and flow.
license: MIT
---

# UX/UI Review

Goal: every user can accomplish their task without confusion. The product looks professional.

Invoke when: user asks to review a project, audit the UI, check usability, or when running alongside code review.

## How to run

**1. Scan first** — find all page/screen files and list them before reviewing anything. If screenshots or a live URL are provided, use those as primary evidence.

**2. Identify user types** — who uses this system? (end user, admin, guest, etc.) For each: what is their goal?

**3. Review each screen per user type** — ask three questions:
- Can this user complete their goal without getting stuck?
- Does anything look broken, inconsistent, or amateur?
- What is the single most confusing or frustrating moment in their flow?

Apply standard UX/UI judgment: usability, visual hierarchy, accessibility, responsiveness, feedback states, empty states, forms, navigation. Skip criteria that clearly don't apply to this project — state why.

**4. Write the report**

```
## UX/UI Review — [Project Name]

Screens found: [list]
User types: [list]

### [User Type]

#### Top friction point
- [The single worst moment in this user's flow]

#### Critical (blocks task completion)
- [Screen]: [issue] → [fix]

#### Major (degrades experience)
- [Screen]: [issue] → [fix]

#### Minor (polish)
- [Screen]: [issue] → [fix]

#### What's working well
- [keep these — don't remove in next iteration]
```

Severity guide: Critical = user cannot finish their task. Major = user finishes but frustrated. Minor = looks unprofessional but functional.

