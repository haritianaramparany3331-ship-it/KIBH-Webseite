# Deep Reading Engine — Draft Content (new website section)

> Consolidated from 3 overlapping drafts on the KIBH dashboard. Repeated
> bullets are merged; distinct phrasing/examples from each draft are kept
> and labeled so Willy can pick or merge. Treat as draft copy — confirm
> final wording and any numbers/claims before publishing.

## Core pitch
No surface-level summarizing. When standard AI fails on 1,000-page tenders,
nested Excel spreadsheets, or complex objection/appeal processes, the Deep
Reading Engine delivers robust, auditable results.

**Alternate framing (more casual/pitch tone, draft 3):** Standard AI
workflows fail at complex tasks because both the reading and the prompt
context get overwhelmed. Anyone who really understands the space knows AI
has no real understanding, and so can't handle tasks that need real
combinatorial reasoning — that's exactly where KIBH's know-how comes in.

## Three pillars
- **100% source referencing ("Footnoted AI"):** every extraction,
  evaluation, and number references the exact page, paragraph, or table
  cell in the original document
- **Multi-LLM cross-validation:** specialized models break workflows into
  deterministic sub-tasks and cross-check each other for consistency,
  hallucinations, logic breaks, calculation errors
- **Confidence scoring & human-in-the-loop:** every result gets a
  confidence score; clear cases pass through automatically, edge cases are
  transparently flagged for human sign-off

## How it works
1. **Task decomposition (micro-pipelines):** documents aren't dumped into a
   context window — complex rule sets are broken into deterministic
   sub-tasks (e.g. clause review, deadline extraction, number reconciliation)
2. **Multi-stage prompt engineering:** specialized prompts for each
   sub-step so the model returns exactly the structure needed
3. **Cross-checking:** multiple model runs validate intermediate results
   against each other for hallucinations, logic breaks, calculation errors
4. **Granular source referencing:** no black-box output — every decision
   has a deep-link back to the source doc (PDF, Excel, scan)
5. **Confidence & anomaly scoring:** automatic pass-through at high
   confidence; selective routing to human experts when thresholds or
   contradictions are hit

## Use cases

**1. Public/industrial tenders — Go/No-Go analysis**
- Challenge: hundreds of pages of service descriptions, exclusion criteria,
  deadlines tie up senior staff for days
- Solution: engine matches your portfolio/capacity against the requirements
  catalog automatically
- Output: structured Go/No-Go decision matrix with risk flagging and exact
  source locations for knockout criteria
- *Draft 3 variant, freight/logistics tenders specifically: questionnaire
  matching + Go/No-Go, "from several weeks to a few minutes"*

**2. Health insurers/insurance — objection & complaint review**
- Challenge: medical assessments, billing line items, legal justifications
  must be checked error-free under time pressure
- Solution: matches billing against guidelines, prior rulings, medical
  documentation
- Output: pre-structured, legally-referenced objection/response draft with
  a full evidence trail
- *Draft 3 phrasing: reviewing thousands of legal documents per case,
  producing an individual objection response*

**3. Construction/industry — bill-of-quantities & quote comparison**
- Challenge: dozens of subcontractor offers with different GAEB files,
  measurements, alternate offers, incomplete BoQs
- Solution: normalizes and deep-checks every line item, flags speculative
  pricing and hidden scope gaps
- Output: complete price/quantity comparison with warnings for missing or
  deviating items
- *(Draft 3 mentions a 3rd example, "Angebot" (quote), but the note cuts
  off there — check with Willy whether it's this one or something else)*