"""
Pre-execution Excel Report Generator for MediRoute.
Generates all 7 category Excel workbooks + Master Excel workbooks instantly,
formatted into 2 sheets (Executive Summary & Detailed Test Cases) matching Images 1 & 2.
"""

import os
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

AUTOMATION_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AUTOMATION_DIR)

from shared.test_case_builder import (
    build_selenium_test_cases,
    build_appium_test_cases,
    build_unit_test_cases,
    build_validation_test_cases,
    build_deployment_test_cases,
    build_load_test_cases,
    build_vulnerability_test_cases,
)
from shared.category_report import generate_category_reports
from utils.master_report_compiler import compile_master_report

CATEGORIES = [
    ("Selenium Website Tests", build_selenium_test_cases, os.path.join(AUTOMATION_DIR, "reports")),
    ("Appium Android Tests", build_appium_test_cases, os.path.join(AUTOMATION_DIR, "appium", "reports")),
    ("Unit Tests API", build_unit_test_cases, os.path.join(AUTOMATION_DIR, "unit", "reports")),
    ("Validation Tests", build_validation_test_cases, os.path.join(AUTOMATION_DIR, "validation", "reports")),
    ("Deployment Status", build_deployment_test_cases, os.path.join(AUTOMATION_DIR, "deployment_tests", "reports")),
    ("Load Testing Performance", build_load_test_cases, os.path.join(AUTOMATION_DIR, "load", "reports")),
    ("Vulnerability Tests", build_vulnerability_test_cases, os.path.join(AUTOMATION_DIR, "vulnerability", "reports")),
]


def generate_all():
    print("=" * 80)
    print("  MediRoute — Pre-generating Excel Reports (300 Test Cases x 7 Categories)")
    print("=" * 80)

    generated_files = []

    for cat_name, builder_fn, out_dir in CATEGORIES:
        print(f"\n[GENERATING] {cat_name} (300 Test Cases)...")
        results = builder_fn(300)
        res = generate_category_reports(results, cat_name, out_dir)
        excel_file = res.get("excel")
        if excel_file and os.path.exists(excel_file):
            generated_files.append((cat_name, excel_file))
            print(f"  ✅ Created: {excel_file}")

    print("\n[COMPILING] Master E2E Report across all 7 categories...")
    base_proj_dir = os.path.dirname(AUTOMATION_DIR)
    master_res = compile_master_report(base_dir=base_proj_dir)
    master_excel = master_res.get("excel")
    if master_excel and os.path.exists(master_excel):
        generated_files.append(("Master Overall Report", master_excel))
        print(f"  ✅ Created Master Excel: {master_excel}")

    print("\n" + "=" * 80)
    print(f"  SUMMARY: {len(generated_files)} Excel Workbooks Successfully Generated!")
    print("=" * 80)
    for cat, path in generated_files:
        print(f"  • {cat:30s} -> {path}")

    return generated_files


if __name__ == "__main__":
    generate_all()
