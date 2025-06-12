import yaml
import os
import subprocess
import argparse
from robot import rebot_cli


def load_config(yaml_file):  # Function to load the YAML config
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)


def run_task(task, test_data_file, iteration_suffix, temp_yaml_file):
    # Extract task details
    root_path = task['root_path']
    test_path = task['test_path']
    test_cases = task['test_cases']
    framework = task['framework']
    tags = task['Tags']
    variable_string = []

    if task.get("Variables", None):
        for key, value in task['Variables'].items():
            variable_string.append("-v")
            variable_string.append(f"{key}:{value}")

    iteration_no = task.get("iteration_no", 1)
    argument = task.get("argument", None)

    for i in range(iteration_no):
        iteration_report_path = f"{task['report_path']}_task{iteration_suffix}"
        os.makedirs(iteration_report_path, exist_ok=True)

        if framework == "Robot Framework":
            for test_case in test_cases:
                command = [
                    "robot",
                    "-d", iteration_report_path,
                    "-x", "outputxunit.xml",
                    *variable_string,
                    "-v", f"TEST_DATA_FILE:{test_data_file}",
                    test_path
                ]
                if argument:
                    command.append(argument)

                print(f"Running: {test_path}, Iteration: {i + 1}, Test Data File: {test_data_file}")
                try:
                    subprocess.run(command, check=True, text=True)
                except subprocess.CalledProcessError as e:
                    print(f"Test case {test_path} failed: {e}")
                    return False  # Stop this test_data_file processing
        elif framework == "UFT":
            for test_case in test_cases:
                command = [
                    "uft_batch_runner",
                    "-test", os.path.join(root_path, test_path),
                    "-report", iteration_report_path,
                    "-v", f"TEST_DATA_FILE:{test_data_file}"
                ]
                if argument:
                    command.append(argument)

                print(f"Running UFT test case: {test_case}, Iteration: {i + 1}")
                try:
                    subprocess.run(command, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"UFT test case {test_path} failed: {e}")
                    return False
        else:
            print(f"Unknown framework: {framework}")

        check_and_set_environment_variables(temp_yaml_file)

    return True


def check_and_set_environment_variables(temp_yaml_file):
    if os.path.exists(temp_yaml_file):
        with open(temp_yaml_file, 'r') as file:
            data = yaml.safe_load(file) or {}
            if data:
                for key, value in data.items():
                    os.environ[key] = str(value)
                    print(f"Set environment variable: {key}={value}")
            else:
                print(f"No data found in {temp_yaml_file} to set as environment variables.")
    else:
        print(f"{temp_yaml_file} does not exist.")


def report_export(report_path, export_path):
    if not os.path.exists(export_path):
        os.makedirs(export_path)

    xml_files = []
    for root, dirs, files in os.walk(report_path):
        for file in files:
            if file == "output.xml":
                xml_files.append(os.path.join(root, file))

    if xml_files:
        rebot_cli(['-x', 'outputxunit.xml', '-d', export_path] + xml_files, exit=False)

    screenshot_files = []
    for root, dirs, files in os.walk(report_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                screenshot_files.append(os.path.join(root, file))

    for screenshot_file in screenshot_files:
        destination = os.path.join(export_path, os.path.basename(screenshot_file))
        with open(screenshot_file, 'rb') as src, open(destination, 'wb') as dest:
            dest.write(src.read())


def main():
    parser = argparse.ArgumentParser(description="Run automated tests based on the YAML configuration.")
    parser.add_argument("yaml_file", help="Path to the YAML configuration file")
    args = parser.parse_args()
    config = load_config(args.yaml_file)

    temp_yaml_file = config["output_temp_file"]
    os.environ["temp_yaml_file"] = temp_yaml_file

    test_data_files = config["test_data_file"].split(", ")

    for idx, test_data_file in enumerate(test_data_files):
        task_iteration_suffix = idx + 1
        task_iteration = config.get("task_iteration", 1)

        print(f"\n========= Running for Test Data File: {test_data_file} =========")

        for iteration in range(1, task_iteration + 1):
            for task_key, task in config['tasks'].items():
                print(f"\nExecuting {task_key}: {task['name']}")
                success = run_task(task, test_data_file, task_iteration_suffix, temp_yaml_file)
                if not success:
                    print(f"Stopping further tasks for: {test_data_file}")
                    break

        # Always export report
        report_path = f"./E2E_Adbreak_Automation/reports/{task_iteration_suffix}"
        export_path = f"./E2E_Adbreak_Automation/exported_reports/{task_iteration_suffix}"
        report_export(report_path, export_path)


if __name__ == "__main__":
    main()
