Allow to validate work entries.

This module allows to:

*   Validate work entries: setting their state to "Validated" on the work entry form
*   Regenerate work entries for dates containing validated work entries

When regenerating work entries, if a conflict is created, the validated work entries will stay validated: only the new conflicting ones will have their state set to "Conflict".
