from hacksport.deploy import deploy_problem

class TestProblems:
    """
    Regression tests for compiled problems.
    """

    def test_compiled_sources(self):
        deploy_problem("./tests/problems/compiled_sources")

    def test_remote_compiled_makefile_template(self):
        deploy_problem("./tests/problems/remote_compiled_makefile_template")
