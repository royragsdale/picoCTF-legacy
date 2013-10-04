print("Setting Indexes");
print("-------------------");

db.submissions.ensureIndex({"pid": 1, "tid": 1, "correct": 1, "key": 1}, {unique: true});
db.submissions.ensureIndex({"tid": 1});
db.submissions.ensureIndex({"pid": 1});

db.problems.ensureIndex({"displayname": 1}, {unique: true});
db.problems.ensureIndex({"pid": 1}, {unique: true});

db.teams.ensureIndex({"tid": 1}, {unique: true});
db.teams.ensureIndex({"teamname": 1}, {unique: true});

db.groups.ensureIndex({"gid":1}, {unique: true});
db.groups.ensureIndex({"name":1}, {unique: true});

print("");

