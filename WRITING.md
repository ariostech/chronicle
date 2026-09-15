# Chronicle Writing Guide

Chronicle documentation should sound like maintainers explaining a system they understand.

## Core rules

### Be concrete

Name the component, action, condition, and consequence.

Prefer “The gateway checks the actor's project scope before querying Hindsight” to “Authorization enforcement occurs before memory retrieval.”

### Separate fact, decision, and uncertainty

State whether a claim is:

- required by an accepted specification;
- a current architecture decision;
- a proposal;
- an implementation detail;
- an assumption that still needs a benchmark.

“We have not benchmarked this yet” is useful project information.

### Explain trade-offs

Record why Chronicle chose an option, what it gives up, and what evidence could change the decision. Do not make every alternative sound equally suitable.

### Use the right voice for the artifact

- A README is approachable and brief.
- A specification uses defined terms and normative language consistently.
- An ADR records context, decision, consequences, and alternatives.
- An RFC invites challenge and identifies unresolved questions.
- A security policy is direct and careful.
- Release notes tell users what changed and what to do.

One polished “brand voice” is not appropriate for every file.

## Style

- Prefer active voice when the actor matters.
- Prefer verbs to abstract nouns.
- Use short sentences for important rules.
- Let technical explanations use longer sentences when the relationships require it.
- Use headings to help navigation, not to give every paragraph a label.
- Use tables for exact mappings and comparisons.
- Use diagrams when topology or sequence is harder to understand in prose.
- Define an acronym on first use in each standalone document.
- Use examples with synthetic names and data.
- Link to the normative source instead of restating a changing external standard in full.

## Normative language

Formal specifications may use `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY`. State near the beginning of the specification that these terms are normative. Ordinary guides should use plain language instead.

## AI-assisted contributions

AI tools may help draft or review project material. The contributor remains responsible for every claim, citation, license obligation, example, and security implication.

Before submitting AI-assisted prose:

- remove claims the source does not support;
- replace generic claims with component-specific explanations;
- verify names, versions, links, and code;
- disclose meaningful uncertainty;
- check that the document does not invent features or commitments;
- ensure examples contain no real secrets or personal data;
- read the result as a maintainer, not as a prompt evaluator.

Do not write for detector scores. Write so a contributor can make a correct decision from the document.

## Patterns to avoid

Avoid habitual filler such as:

- “in today's rapidly evolving landscape”;
- “seamlessly leverage”;
- “delve into”;
- “it is important to note” when the sentence can simply state the point;
- repeated “not just X, but Y” framing;
- claims that Chronicle is comprehensive, enterprise-ready, secure, or production-ready without evidence.

These words are not banned. Repetition and unsupported polish are the problem.

## Links and citations

- Prefer primary specifications, official documentation, research papers, and source repositories.
- Put a citation next to the claim it supports.
- Include access or version dates when upstream behavior is likely to change.
- Do not use a search-results page as a source.
- Do not copy large passages when a short quote and a clear paraphrase will do.

## Repository conventions

- Use sentence case for headings.
- Wrap code, paths, fields, and literal values in backticks.
- Keep filenames stable after publication unless the move includes link updates.
- Use relative links for files inside this repository.
- End text files with one newline.
- Use UTF-8 and LF line endings.

## Final review

Before merging documentation, ask:

1. What should the reader know or do after reading this?
2. Which statements are contracts, decisions, proposals, or guesses?
3. Could a new contributor interpret any sentence in a materially unsafe way?
4. Are links and examples correct?
5. Can anything be shorter without losing necessary context?
