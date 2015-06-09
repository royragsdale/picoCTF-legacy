from hacksport.deploy import deploy_problem

class TestCompiled:
    """
    Regression tests for compiled problems.
    """

    def test_compiled_sources(self):
        deploy_problem("./tests/problems/compiled_sources")
