"""Prompts for the report generation agent."""

# Prompt generating the report outline
report_planner_instructions = """You are an expert technical writer, helping to plan a report.

Your goal is to generate the outline of the sections of the report.

The overall topic of the report is:

{topic}

The report should follow this organization:

{report_organization}

You should reflect on this information to plan the sections of the report:

{context}

Now, generate the sections of the report. Each section should have the following fields:

- Name - Name for this section of the report.
- Description - Brief overview of the main topics and concepts to be covered in this section.
- Research - Whether to perform web research for this section of the report.
- Content - The content of the section, which you will leave blank for now.

Consider which sections require web research. For example, introduction and conclusion will not require research because they will distill information from other parts of the report."""
