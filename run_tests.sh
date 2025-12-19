#!/bin/bash
# Test Runner for HUE Customization Odoo 12 Migration
# Usage: ./run_tests.sh [unit|integration|all]

set -e

DB_NAME="odoo12_test_db"
MODULE_NAME="hue_customization"
ODOO_BIN="odoo-bin"

log_info() {
    echo -e "\033[0;32m[INFO]\033[0m $1"
}

log_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

# Check if Odoo is installed
if ! command -v $ODOO_BIN &> /dev/null; then
    log_error "odoo-bin not found. Ensure Odoo 12 is installed."
    exit 1
fi

# Create test database
setup_test_db() {
    log_info "Setting up test database..."
    createdb "$DB_NAME" 2>/dev/null || log_info "Test database already exists"
}

# Run unit tests
run_unit_tests() {
    log_info "Running unit tests (TEST-01 to TEST-10)..."
    
    $ODOO_BIN -d "$DB_NAME" -u "$MODULE_NAME" \
        --test-enable \
        --test-file="tests/test_migration.py" \
        --no-http \
        --stop-after-init 2>&1 | tee test_results.log
    
    if grep -q "passed" test_results.log; then
        log_info "✓ Unit tests passed"
        return 0
    else
        log_error "✗ Unit tests failed"
        return 1
    fi
}

# Run integration tests
run_integration_tests() {
    log_info "Running integration tests (placeholder)..."
    log_info "Note: Integration tests should include:"
    log_info "  - Invoice generation workflow"
    log_info "  - Discount application workflow"
    log_info "  - Student fee calculation"
}

# Run all tests
run_all_tests() {
    setup_test_db
    run_unit_tests
    run_integration_tests
}

# Cleanup
cleanup_test_db() {
    log_info "Cleaning up test database..."
    dropdb "$DB_NAME" 2>/dev/null || true
}

# Main
case "${1:-all}" in
    unit)
        setup_test_db
        run_unit_tests
        ;;
    integration)
        run_integration_tests
        ;;
    all)
        run_all_tests
        ;;
    cleanup)
        cleanup_test_db
        ;;
    *)
        echo "Usage: $0 {unit|integration|all|cleanup}"
        exit 1
        ;;
esac

log_info "✓ Test execution complete"
