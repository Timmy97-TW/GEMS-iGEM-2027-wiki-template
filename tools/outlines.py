# -*- coding: utf-8 -*-
"""Seed outline of every page: section headings, what judges look for, and which
placeholders the section starts with. tools/build.py reads this only to scaffold
a page that does not exist yet. Once a team member owns a page, the page file is
the truth and this file is no longer used for it.

Sources for the guidance, all read 2026-11-05 and all 2026 rules (2027 rules are
not published): iGEM Medals and Special Awards pages (ballot questions), and the
2026 Judge Handbook. Guidance is paraphrased. Everything is in English, because
judges read the wiki in English.

Each section: (heading, guide, options)
  options: figs = list of figure hints, facts = list of fact hints,
           block = name of a component block in tools/build.py, attr = True for
           an attribution line
"""

SHARED_ABSTRACT = ("In 3 to 5 sentences: what this page must convince the judges of, and the strongest evidence "
                   "for it. Judges arrive here straight from the ballot and will not have read any other page first.")

OUTLINES = {
"home": {
  "lede": "[One sentence: the problem the project solves, and how.]",
  "kicker": "GEMS Taiwan · iGEM 2027",
  "sections": [
    ("The problem", "The first Best Wiki question is whether the site makes the project and its goals clear. The first screen must tell a stranger what the problem is and who it affects. Every number about the problem needs a V.", {"facts": ["Number showing the scale of the problem"], "figs": ["Diagram of the problem"]}),
    ("Our approach", "Explain the approach with one system diagram, not a pile of jargon. Judges want to finish reading and know what you did.", {"figs": ["System overview diagram"]}),
    ("What we achieved", "Only verified results, each linked to the page that proves it. Do not write up what you did not achieve as if you had.", {"facts": ["The single most important result number"]}),
    ("Explore the wiki", "Helping judges find content is a Best Wiki criterion. Keep these entry points or replace them with better navigation, but they must link to the standard pages.", {"block": "doors"}),
  ]},
"description": {
  "lede": "[Why the project is worth doing: the problem, the gap in current approaches, and our answer.]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("The problem", "Describe the problem and the people it affects, with references. Background is there so judges understand your choices; it is not a textbook.", {"facts": ["Number showing the scale of the problem"], "figs": ["Diagram of the problem"]}),
    ("Why existing approaches fall short", "Judges ask whether you studied earlier work seriously. List existing solutions and their gaps, including past iGEM teams, with sources.", {}),
    ("Our solution", "Explain how the system works and what each module does. Figures and text must match the lab pages and never claim more than they do.", {"figs": ["How the system works"]}),
    ("How the work evolved", "Link to Human Practices and Engineering, and show how the idea changed because of evidence or stakeholders.", {}),
  ]},
"engineering": {
  "lede": "[How we solved the problem step by step with Design, Build, Test, Learn.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Engineering goals", "Silver requires at least one complete design cycle. The Handbook values failure as much as success; what matters is that a hypothesis was confirmed or refuted. Start with each goal's hypothesis and success criterion.", {"facts": ["Success criterion value"]}),
    ("Cycles", "Every cycle needs Design, Build, Test and Learn, and Learn must actually change the next Design. If a Part is used to meet the criterion, its documentation must be on the Part's Registry page. Put every cycle here; every result figure has an F, and every number has a V linked back to an R.", {"block": "dbtl", "attr": True}),
    ("What we would do next", "Judges want to see that you know what the next cycle would change, and why.", {}),
  ]},
"contribution": {
  "lede": "[What we leave for future iGEM teams, and how they can use it.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Contributions at a glance", "Required for Bronze. State explicitly why this is useful to other teams. Any form works: data, a tool, Part documentation or a troubleshooting record.", {}),
    ("Contribution details", "One subsection each: what it is, how to reproduce it, how far it was validated, and its limits. If an existing Part is used to meet the criterion, add the documentation to that Part on the Registry and link it here.", {"figs": ["The contribution or how it is used"], "facts": ["Reusable specification or data"]}),
    ("How future teams can use this", "Write for next year's students: where to start, what to prepare and where they will get stuck.", {}),
  ]},
"results": {
  "lede": "[What we actually achieved, the evidence for it, and what we did not achieve.]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Key results", "Best Wiki asks whether the results are backed by convincing experimental evidence. Every claim gets one figure and one set of numbers; captions state n, the statistical method and the controls.", {"figs": ["Main result figure"], "facts": ["Main result value (with units and n)"], "attr": True}),
    ("Proof of concept", "Judges compare goals with results. State clearly how far the system was validated, and which parts are model estimates and which are experiments.", {"figs": ["Proof of concept"]}),
    ("What did not work", "The Handbook says failure has value too. Honestly describing what did not work, and your judgement about it, scores better than hiding it.", {}),
    ("Future work", "What comes next, and what it would take.", {}),
  ]},
"alternative-platform": {
  "lede": "[Why we chose this non-standard platform, and how we engineered on it.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Why this platform", "This award covers platforms other than the common model organisms. Judges ask whether the platform really suits the problem, and how closely the results depend on it. If the team is not competing for it this year, say so on the page (\"Not selected this year\"); do not delete the URL.", {}),
    ("Engineering evidence", "Judges ask how strong the evidence of successful engineering is. Show data, not vision.", {"figs": ["Engineering evidence"], "facts": ["Key result value"]}),
    ("What did not work", "Judges explicitly want to see what did not work, why, and what others should watch out for.", {}),
    ("Safety on this platform", "Link to Safety and Security. High-school teams must stay within the iGEM White List; if unsure, ask safety@igem.org first.", {}),
  ]},
"experiments": {
  "lede": "[How we ran our experiments, so others can repeat them.]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Experimental overview", "Organise by goal, not by date. Link each goal to its results and to its Engineering cycle.", {"figs": ["Overview of the experimental workflow"]}),
    ("Protocols", "Write so another team can repeat it: materials, conditions, controls. Content comes from the current version in Hub SOPs; give the S number and version instead of writing a second copy.", {"facts": ["Key experimental conditions"], "attr": True}),
    ("Controls and validation", "Explain how you know the experiment itself can be trusted.", {}),
  ]},
"measurement": {
  "lede": "[What we measured, how we calibrated, and whether other teams can reproduce it.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("What we measured and why", "Handbook: choosing the right thing to measure matters more than measuring a lot. For qualitative results, explain the path to quantitative ones; admitting a result is only qualitative is better than reporting flawed quantitative numbers.", {"facts": ["Measurement target and units"]}),
    ("Methods and protocols", "Judges ask whether the methods are described well enough for other teams to reproduce.", {"figs": ["Measurement method"]}),
    ("Calibration and validation", "Judges ask whether measurements were properly calibrated and validated. Show calibration curves, standards and sources of error.", {"figs": ["Calibration curve"], "facts": ["Calibration result"]}),
    ("Usefulness to other projects", "Judges ask whether the measurement is useful to other projects. Say who can use it and how.", {}),
  ]},
"safety-and-security": {
  "lede": "[How we identified and managed risks, and what we contributed to safety in the field.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Lab safety and risk assessment", "The Handbook requires every team to manage risks to themselves, their colleagues, the community and the environment. Quote the Safety Register directly; do not write a separate version for the wiki. High-school teams must stay within the White List.", {"attr": True}),
    ("Safety forms", "State which forms were submitted and when. The forms themselves are public on the team page.", {}),
    ("Project-specific risks", "Judges ask whether this project's risks were properly managed. Explain how biosafety and biosecurity were each handled.", {}),
    ("Contribution to safety", "Only needed when competing for the award. Judges ask what you contributed to biosafety or biosecurity, how far it was validated, whether it builds on existing knowledge, and whether real-world use was considered.", {"figs": ["Safety measure or its validation"]}),
  ]},
"notebook": {
  "lede": "[The daily wet-lab record: what we did each day, what happened, and which Run it belongs to.]",
  "sections": [
    ("How to read this notebook", "Judges use this page to confirm the work was really done. Each entry matches one R in Hub Runs, and its content comes from the Run Record rather than being retyped.", {}),
    ("Entries", "In date order, one entry per Run, filterable by month or keyword. Do not paste unprocessed raw files.", {"block": "notebook"}),
  ]},
"parts": {
  "lede": "[Our Parts, and where their Registry documentation is.]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Parts table", "Part awards have no standard page; judges look only at the Registry. This page is just an index: every row links to the Registry and gives the C number. Write the content in the Registry first, not here.", {"block": "parts"}),
    ("Collections", "Keep only if you have a Part Collection. Judges ask whether it is a set of Parts designed to work together, or just a list of every Part you made.", {}),
    ("Characterization", "Summarise the most important characterization data and link to Results and Measurement instead of repeating figures.", {"figs": ["Part characterization data"], "facts": ["Key characterization value"]}),
  ]},
"model": {
  "lede": "[The questions our model answered, and how it changed our design.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Questions the model answers", "Judges ask whether the model helped the team understand, predict or design. State the questions first, then the equations.", {}),
    ("Model design and assumptions", "List assumptions and where each parameter comes from; every parameter gets a V linked back to an R or a reference. Code lives in the team repository; cite the commit.", {"figs": ["Model structure diagram"], "facts": ["Model parameter and its source"], "attr": True}),
    ("Validation", "Judges ask whether experimental or other relevant data was used to develop, train or validate the model. Say plainly what was not validated.", {"figs": ["Model versus experiment"]}),
    ("How the model changed the project", "Name the specific decision the model changed, and link to the Engineering cycle. Judges ask whether this could serve as an example for others.", {}),
  ]},
"hardware": {
  "lede": "[The synthetic biology need this hardware meets, and whether others can build it.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("The need", "Judges ask whether the hardware addresses a need or problem in synthetic biology.", {}),
    ("Design and build", "Each device maps to an H project number. CAD and firmware live in the team repository; images go on static.igem.wiki. If files are too large, link only to downloads on iGEM platforms.", {"figs": ["Device design drawing"], "facts": ["Key specification"], "attr": True}),
    ("Proof of concept", "Judges ask whether usefulness and functionality were demonstrated.", {"figs": ["Functional test result"]}),
    ("User testing", "Judges ask whether user testing was done and whether you learned from the feedback. Names and photos of testers need a K.", {}),
    ("Reproducibility", "Judges ask whether the documentation is enough for another team to rebuild it. List the bill of materials, assembly steps and cost.", {"facts": ["Cost and part count"]}),
  ]},
"software": {
  "lede": "[What the tool does, who can use it, and how to install it.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("What the tool does", "Judges ask whether the tool could be useful to other projects. It need not be big or complex, but it must solve a real problem.", {"figs": ["Tool screen or workflow"]}),
    ("Install and use", "Judges ask whether it is easy to use. It must have an OSI-approved licence, with source code in a dedicated repository on iGEM GitLab, linked here; since 2026 up to 5 repositories may be submitted.", {}),
    ("Validation", "Judges ask how far it was validated by experiments, test data or benchmarks.", {"facts": ["Validation result"], "attr": True}),
    ("Standards and integration", "Judges ask whether it is compatible with synthetic biology standards (for example SBOL) and can integrate with outside tools (APIs, packages).", {}),
    ("Documentation for developers", "Judges ask whether the code and documentation make it easy for future teams to extend.", {}),
  ]},
"drylab-notebook": {
  "lede": "[The daily record of computational and hardware work: what we ran, what happened, and which Run it belongs to.]",
  "sections": [
    ("How to read this notebook", "Judges use this page to confirm the work was really done. Hub Runs is the source: one computation or test is one R, and this page is only its published copy.", {}),
    ("Entries", "In date order, one entry per Run, with the commit and where the output files are.", {"block": "notebook"}),
  ]},
"human-practices": {
  "lede": "[How we judged that the project is responsible and good for the world, and how the outside world changed it.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Values and framework", "Silver asks which values went into the design, who you consulted, and what evidence shows the project is responsible and good for the world. State your framework and the reasons for it.", {}),
    ("Project evolution", "Judges ask whether the HP work is woven into the whole project. Map each change: the interaction I, the decision D, and how the project changed.", {"figs": ["How the project evolved"]}),
    ("Stakeholder engagement", "Judges ask whether stakeholders with different viewpoints were included, with context and reasons. One card per person; without a consent record K, no names, photos, quotes or logos. Minors also need school or parental permission.", {"block": "ihp"}),
    ("Implementation and end users", "Silver asks who would use it, how, how it would be put into practice in the real world, and with what impact.", {}),
    ("What others can build on", "Judges ask whether the documentation lets others build on it and inspires them.", {}),
  ]},
"education": {
  "lede": "[Who we talked with, and what we learned from each other.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Who we reached and why", "This award is about two-way dialogue. Judges ask how much it fostered mutual learning or dialogue. It is not about promoting iGEM or synthetic biology. Activities need not relate to the project.", {"facts": ["Number of sessions and participants"]}),
    ("Activities", "Judges ask whether the activities were thoughtfully carried out. One card per activity, matched to an I in Interactions. Do not name minors; their photos need school or parental permission (K).", {"block": "ihp", "figs": ["Activity record"]}),
    ("What participants and we learned", "Show real feedback and what changed. Judges ask whether more people can now take part in synthetic biology.", {"facts": ["Feedback data"]}),
    ("Materials others can reuse", "Judges ask whether the documentation lets others continue the work. Attach the materials and instructions for using them.", {}),
  ]},
"entrepreneurship": {
  "lede": "[How the project could become a real product or business.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Customers and unmet need", "Judges ask whether you identified your first potential customers and a need existing solutions do not meet. Back it with interview evidence; interviewees' names need a K.", {"facts": ["Market or need figure"]}),
    ("Solution and feasibility", "Judges ask whether the solution is feasible, scalable and innovative. This award also expects a minimum viable product.", {"figs": ["Product or prototype"]}),
    ("Development plan", "Judges ask whether there are reasonable milestones, timelines, resources and risks.", {"figs": ["Product development roadmap"]}),
    ("Team and partners", "Judges ask what skills and partners are needed to take it forward credibly.", {}),
    ("Long-term impact", "Judges ask whether the long-term positive and negative impacts of the full solution were considered.", {}),
  ]},
"sustainability": {
  "lede": "[Which SDGs we chose, how we evaluated them, and what actually changed.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Chosen goals and evaluation", "Judges ask whether the work addresses one or more SDGs measurably and significantly. Pick a few, and state why and how you evaluate them.", {"facts": ["SDG indicator"]}),
    ("Stakeholder feedback", "Judges ask whether feedback from relevant stakeholders was built into the work.", {}),
    ("Long-term impacts and interactions", "Judges ask about long-term social, environmental and economic impacts, and positive or negative effects on other SDGs.", {"figs": ["Impact assessment"]}),
    ("What others can build on", "Judges ask whether the SDG work is documented so other teams can continue it.", {}),
  ]},
"inclusivity": {
  "lede": "[The barriers to participation we identified, and how we lowered them.]",
    "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Barriers we investigated", "Judges ask how deeply barriers to participation in science were investigated. Activities need not relate to the project.", {"facts": ["Survey data on barriers"]}),
    ("What we did", "Judges ask how much access to synthetic biology or science was widened.", {"figs": ["Activity or outcome"]}),
    ("Dialogue with the group", "Judges ask whether you talked with the group you aimed to include and considered their needs, opinions and values.", {}),
    ("What others can build on", "Judges ask whether the documentation lets other teams or outside organisations continue the work.", {}),
  ]},
"laws-and-regulations": {
  "lede": "[The regulations the project would meet in practice, and how we adjusted because of them.]",
  "sections": [
    ("Abstract", SHARED_ABSTRACT, {}),
    ("Regulatory landscape", "Not a standard page, but it can be linked from Human Practices as supporting material. Link back to the original legal text and give the date you read it.", {"facts": ["Regulation and date read"]}),
    ("What this means for our project", "State the concrete design or plan changes the regulations caused, and link to Human Practices.", {}),
    ("Expert input", "Names, quotes and logos of the people consulted all need a K. No image without a K goes up.", {"block": "ihp"}),
  ]},
"team": {
  "lede": "[Who we are.]",
  "sections": [
    ("Members", "Since 2026, Attributions data is shown directly on the iGEM team page. Copy the public columns of Hub Roster into assets/data/roster.js; portraits need a K.", {"block": "team"}),
  ]},
"attributions": {
  "lede": "[Who did what, and who helped us. The official record is iGEM's Attributions Form.]",
    "sections": [
    ("Official Attributions Form", "Since 2026 the Attributions Form is submitted from the Deliverables Dashboard, no longer has to be embedded in the wiki, and is shown publicly on the team page. Bronze requires every field, including specific tasks. Judges check that it is plausible. AI use must be disclosed here too.", {"block": "attribution-link"}),
    ("Who did what", "This table summarises the Hub and the Attribution sheet, public content only. Outside helpers are named only with a K.", {"block": "attribution"}),
  ]},
"milestone": {
  "lede": "[How the year went.]",
  "sections": [
    ("Our year", "From Milestones Caption, each entry with its real date. Every photo links to an M; identifiable people need a K.", {"block": "timeline"}),
  ]},
}
