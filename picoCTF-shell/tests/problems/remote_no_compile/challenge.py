from hacksport.problem import Remote, Compiled, File, ExecutableFile, ProtectedFile

class Problem(Remote):
    program_name = "mybinary"
    files = [ProtectedFile("flag.txt")]
