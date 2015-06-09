from hacksport.problem_templates import LocalCompiledBinary

Problem = LocalCompiledBinary(sources=["mybinary.c"], share_source=True, static_flag="this_is_the_flag")
