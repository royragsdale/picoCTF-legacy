Things to do:
* Add ui element for TLS vs SSL email
* Add ui element to require email verification
* Update sever error email logger
* Need token name sanitization
* Potential race condition in token generation **if** you are sending a ton of tokens to the same person at once
* Using MD5 for hashes in common.py
* It is technically possible to generate a duplicate token if uuid.uuid64 duplicates
* Add TTL for tokens
* Consider moving tokens out of user.py
* Come up with a better user verification body?
* Clear distinction between /api/user/status and /api/team/settings
* #team-builder explicit in user.py routes and front-page.coffee
* /api/user/verify doesn't have a great way of informing the user whether or not they succeeded.
  * Realistically we could just create a /verify and a verify.coffee but that is a lot of boilerplate.
* Code duplication like crazy for react components. classroom-management, react-utils, etc. We **need** to fix the js organization.
* Shouldn't show option to create/delete group to teachers.
* Group info in get_team_information is awkward
* is_owner vs is_teacher in groups
* It would be great to get teacher=Bool out of user, we could just aggregate it and it would be a lot smoother.
* Affiliation does not work for team builder.
* Clear confusion between is_n_of_group, using TIDs for everything is wrong.
* Group hierarchy is a mess ^
* /api/user/status is a mess
