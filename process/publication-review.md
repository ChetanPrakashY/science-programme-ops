# Publication review: how a paper, poster or talk gets cleared

Version 0.1 (draft for discussion). Owner: science programme.

## Why this exists

Researchers and engineers should be able to publish, and the company needs three things checked
before anything leaves the building: no customer or confidential information goes out by accident,
the science holds up, and someone accountable said yes. This process does those three checks in a
fixed order with fixed times, so authors know when to start and nobody is surprised a week before a
deadline.

## What needs review

Anything public that uses company data, results or hardware details: journal and conference papers,
abstracts, posters, talks (including recorded webinars), preprints, datasets, and technical blog posts.
Internal seminars do not need it. If unsure, submit it; a quick "no review needed" costs a day.

## Roles

| Role | Who | Does |
|---|---|---|
| Author | whoever leads the work | fills the submission form, makes the changes asked for |
| Programme lead | science programme | runs the process, keeps the tracker, chases delays |
| Confidentiality reviewer | legal / business, rotating | the confidentiality checklist below |
| Technical reviewer | a scientist or engineer not on the author list | reads it like a referee would |
| Approver | head of science (or delegate) | final yes / no |

## Stages and times

Times are working days and are a starting proposal; adjust them after a quarter of real data.

| Stage | Max time | Leaves the stage when |
|---|---:|---|
| 1. Submitted | - | the form is complete (tracker `check` passes) |
| 2. Confidentiality | 5 | checklist signed off, or changes requested |
| 3. Technical review | 10 | reviewer's comments answered |
| 4. Approval | 3 | approver signs |
| 5. Approved / submitted | - | author submits to the venue and records the date |

So an author should submit **at least 18 working days before the venue deadline**. The tracker
(`tracker/pubtrack.py status`) marks items LATE when the remaining stages no longer fit, and "stuck"
when an item has sat in one stage longer than its maximum.

## Confidentiality checklist

- Does it use customer data or show a customer's area of interest? Then written customer consent is on
  file before approval. The tracker refuses to move such an item to approval without it.
- Does it state unreleased product specifications, pricing, roadmap, or partner names under NDA?
- Does it describe technology that may fall under export controls (in India, the SCOMET list)? If
  possible, ask legal.
- Are images and data used within their licence (company data licence, third-party data terms)?
- Do author affiliations and the acknowledgement follow the standard wording?

## Technical review

The reviewer answers four questions in writing: is the claim supported by what is shown, are the
methods described well enough to repeat, are uncertainties stated, and would a referee at this venue
accept it. The author replies point by point. Disagreements go to the approver.

## Records

Every item keeps: the submission form, the checklist, review comments and replies, the approval, and
the final submitted version, all linked from its tracker row. That makes it possible to answer, later,
who approved what and on which version.

## Measuring the process

Once a quarter: median days per stage, the number of items that arrived late (submitted with less than
18 working days), and items withdrawn. If one stage is the bottleneck, change that stage, not the others.
