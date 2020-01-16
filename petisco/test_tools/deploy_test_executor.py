import time
import traceback

from petisco.test_tools.deployment_test_inventory import deploy_test_inventory


class DeployTestsExecutor:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    @staticmethod
    def get_available_tests():
        return list(deploy_test_inventory.keys())

    def execute(self, selected_test=None):
        errors = {}
        start_time = time.time()
        is_success = False

        if selected_test and (selected_test in deploy_test_inventory):
            tests = {selected_test: deploy_test_inventory[selected_test]}
        else:
            tests = deploy_test_inventory

        total_tests = len(tests)

        for i, (test_name, deploy_test) in enumerate(tests.items()):

            status = "FAILED"
            try:
                result = deploy_test.execute(verbose=self.verbose)
                if result.is_success:
                    status = "PASSED"
                else:
                    errors[test_name] = result.value.__repr__

            except Exception:
                errors[test_name] = traceback.format_exc()

            print(
                "{test_name:<50} {status} {i:>10}/{total_tests}".format(
                    test_name=test_name, status=status, i=i + 1, total_tests=total_tests
                )
            )
        elapsed_time = time.time() - start_time
        num_errors = len(errors)
        num_passed = total_tests - num_errors

        skipped_tests = len(deploy_test_inventory) - total_tests

        if num_errors > 0:
            print(
                f"Failed {num_errors} of {total_tests} in {elapsed_time:02f} seconds. Skipped {skipped_tests}."
            )
            print("\nFailed Deploy Tests:")
            for test_name, error in errors.items():
                print(
                    "> {test_name}:\n {error}".format(test_name=test_name, error=error)
                )

        else:
            print(
                f"Passed {num_passed} of {total_tests} in {elapsed_time:02f} seconds. Skipped {skipped_tests}."
            )

        if len(errors) == 0:
            is_success = True
        return is_success
