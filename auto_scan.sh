#!/bin/bash

# Define where to save the logs
LOG_DIR="$HOME/scan_results"
mkdir -p "$LOG_DIR"

echo "=== STARTING AUTOMATED SECURITY SCAN ==="
echo "Results will be saved to: $LOG_DIR"

# 1. Update malware definitions quietly
echo "[1/4] Updating ClamAV definitions..."
sudo systemctl stop clamav-freshclam 2>/dev/null
sudo freshclam --quiet

# 2. Run ClamAV Malware Scan (Only logs infected files to save noise)
echo "[2/4] Running Malware Scan (this may take a while)..."
#!/bin/bash

# Define where to save the logs
LOG_DIR="$HOME/scan_results"
mkdir -p "$LOG_DIR"

echo "=== STARTING AUTOMATED SECURITY SCAN ==="
echo "Results will be saved to: $LOG_DIR"

# 1. Update malware definitions quietly
echo "[1/4] Updating ClamAV definitions..."
sudo systemctl stop clamav-freshclam 2>/dev/null
sudo freshclam --quiet

# 2. Run ClamAV Malware Scan (Only logs infected files to save noise)
echo "[2/4] Running Malware Scan (this may take a while)..."
sudo clamscan -r --infected --nocerts --exclude-dir="^/sys" --exclude-dir="^/proc" --exclude-dir"^/dev" --exclude-dir="^/mnt" / > "$LOG_DIR/clamav_infected.log" 2>&1

# 3. Update and Run Rootkit Hunter (Runs in non-interactive/cron mode)
echo "[3/4] Running Rootkit Scans..."
sudo rkhunter --propupd --quiet
sudo rkhunter --check --sk --nocolor > "$LOG_DIR/rkhunter.log" 2>&1
sudo chkrootkit > "$LOG_DIR/chkrootkit.log" 2>&1

# 4. Run Lynis System Audit (Runs completely non-interactive)
echo "[4/4] Running Lynis System Audit..."
sudo lynis audit system --quick --no-colors > "$LOG_DIR/lynis_audit.log" 2>&1

echo "=== SCAN COMPLETE ==="
echo "Check your results using: ls $LOG_DIR"
sudo lynis audit system --quick --no-colors > "$LOG_DIR/lynis_audit.log" 2>&1

echo "=== SCAN COMPLETE ==="
echo "Check your results using: ls $LOG_DIR"
