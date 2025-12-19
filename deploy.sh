#!/bin/bash
# DEPLOYMENT SCRIPT - Odoo 11 → Odoo 12 Migration
# Usage: ./deploy.sh [backup|deploy|migrate|verify|rollback]

set -e

# Configuration
ODOO_USER="odoo"
ODOO_GROUP="odoo"
ODOO_SERVICE="odoo12"
ODOO_ADDONS="/opt/odoo/addons"
DB_NAME="odoo12_db"
BACKUP_DIR="/backups/odoo"
MODULE_NAME="hue_customization"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

backup_database() {
    log_info "Backing up database..."
    mkdir -p "$BACKUP_DIR"
    pg_dump -U "$ODOO_USER" "$DB_NAME" > "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql"
    log_info "✓ Database backed up: $BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql"
}

backup_module() {
    log_info "Backing up module..."
    if [ -d "$ODOO_ADDONS/$MODULE_NAME" ]; then
        cp -r "$ODOO_ADDONS/$MODULE_NAME" "$BACKUP_DIR/${MODULE_NAME}_${TIMESTAMP}/"
        log_info "✓ Module backed up: $BACKUP_DIR/${MODULE_NAME}_${TIMESTAMP}/"
    fi
}

stop_service() {
    log_info "Stopping Odoo service..."
    sudo systemctl stop "$ODOO_SERVICE" || log_warn "Service already stopped"
    sleep 3
}

start_service() {
    log_info "Starting Odoo service..."
    sudo systemctl start "$ODOO_SERVICE"
    sleep 5
    log_info "✓ Odoo service started"
}

deploy_module() {
    log_info "Deploying updated module..."
    
    if [ ! -d "." ] || [ ! -f "__manifest__.py" ]; then
        log_error "Must run from module directory"
        exit 1
    fi
    
    sudo cp -r . "$ODOO_ADDONS/$MODULE_NAME/"
    sudo chown -R "$ODOO_USER:$ODOO_GROUP" "$ODOO_ADDONS/$MODULE_NAME"
    
    log_info "✓ Module deployed to: $ODOO_ADDONS/$MODULE_NAME"
}

migrate_module() {
    log_info "Running module migration..."
    
    sudo -u "$ODOO_USER" odoo-bin \
        -d "$DB_NAME" \
        -u "$MODULE_NAME" \
        --dev=xml \
        --logfile=/var/log/odoo/migration.log \
        --stop-after-init \
        2>&1 | tee migration_output.log
    
    if grep -q "Successfully installed" migration_output.log; then
        log_info "✓ Migration completed successfully"
        return 0
    else
        log_warn "Check migration_output.log for details"
        return 1
    fi
}

verify_installation() {
    log_info "Verifying installation..."
    
    sudo -u "$ODOO_USER" odoo-bin shell -d "$DB_NAME" << 'EOF'
try:
    count = env['hue.alumni.fees'].search_count([])
    print("✓ hue.alumni.fees accessible")
    count = env['hue.discounts'].search_count([])
    print("✓ hue.discounts accessible")
    count = env['account.invoice'].search_count([])
    print("✓ account.invoice accessible")
    print("✓ All models verified - Migration successful!")
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)
EOF
}

rollback() {
    log_warn "Rolling back migration..."
    stop_service
    
    if [ -f "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql" ]; then
        log_info "Restoring database..."
        dropdb "$DB_NAME" 2>/dev/null || true
        createdb "$DB_NAME"
        psql "$DB_NAME" < "$BACKUP_DIR/${DB_NAME}_${TIMESTAMP}.sql"
        log_info "✓ Database restored"
    fi
    
    if [ -d "$BACKUP_DIR/${MODULE_NAME}_${TIMESTAMP}" ]; then
        log_info "Restoring module..."
        sudo rm -rf "$ODOO_ADDONS/$MODULE_NAME"
        sudo cp -r "$BACKUP_DIR/${MODULE_NAME}_${TIMESTAMP}" "$ODOO_ADDONS/$MODULE_NAME"
        log_info "✓ Module restored"
    fi
    
    start_service
    log_info "✓ Rollback completed"
}

# Main execution
case "${1:-migrate}" in
    backup)
        backup_database
        backup_module
        ;;
    deploy)
        stop_service
        deploy_module
        ;;
    migrate)
        log_info "Starting full migration..."
        backup_database
        backup_module
        stop_service
        deploy_module
        start_service
        migrate_module
        verify_installation
        log_info "✓✓✓ MIGRATION COMPLETE ✓✓✓"
        ;;
    verify)
        start_service
        verify_installation
        ;;
    rollback)
        rollback
        ;;
    *)
        echo "Usage: $0 {backup|deploy|migrate|verify|rollback}"
        exit 1
        ;;
esac
