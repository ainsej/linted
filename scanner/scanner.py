from linted.models import ScanViolation

import os



class Scanner:
    def __init__(self, repository_scan, linter, path):
        self.repository_scan = repository_scan
        self.linter = linter
        self.path = path

    def get_relative_path(self, abs_path):
        return os.path.relpath(abs_path, self.path)

    def save_violation(self, error_group, file_path, start_line, end_line):
        scan_violation = ScanViolation()

        scan_violation.linter = self.linter
        scan_violation.scan = self.repository_scan
        scan_violation.snippet = ""

        scan_violation.error_group = error_group
        scan_violation.file = file_path
        scan_violation.start_line = start_line
        scan_violation.end_line = end_line

        scan_violation.save()