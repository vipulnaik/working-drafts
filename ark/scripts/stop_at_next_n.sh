#!/usr/bin/env bash
# stop_at_next_n.sh — schedule a graceful stop for mu_enumerate.py (or any
# script with the same "[idx/total] ..." per-item log format) that lands
# exactly after the CURRENT in-flight item finishes, instead of you trying
# to time Ctrl-C by hand and risking cutting off a half-done n.
#
# Usage:
#   1. Run the job with output going to a log file you can tail, e.g.:
#        cpulimit -l 1 -- python3 scripts/mu_enumerate.py --nmax 10000 \
#            --out mu_table_safe_v2.csv | tee run.log
#   2. In a second terminal:
#        ./stop_at_next_n.sh run.log <job_pid>
#      (find the pid with: pgrep -f mu_enumerate.py)
#   3. Press Enter whenever you've decided you want to stop. The script
#      waits for the NEXT completed-n line to appear in the log, then sends
#      a single SIGINT to the job — the same signal a real Ctrl-C sends,
#      so mu_enumerate.py's own graceful-stop handling runs normally.
#
# This only ever sends one plain SIGINT, once, on a line-match — nothing
# fancier than that, deliberately, given how much grief a more elaborate
# wrapper caused for this same job in the past.

set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <logfile> <job_pid>" >&2
    exit 1
fi

LOGFILE="$1"
JOB_PID="$2"

if ! kill -0 "$JOB_PID" 2>/dev/null; then
    echo "error: PID $JOB_PID doesn't look alive (or isn't yours)." >&2
    exit 1
fi

if [[ ! -f "$LOGFILE" ]]; then
    echo "error: $LOGFILE doesn't exist. Is the job actually writing to it (via tee)?" >&2
    exit 1
fi

echo "Watching PID $JOB_PID via $LOGFILE."
echo "Press Enter to schedule a stop after the CURRENT n finishes (Ctrl-C to cancel)..."
read -r

echo "Armed. Waiting for the next completed-n line..."

TAIL_PID=""
cleanup() {
    [[ -n "$TAIL_PID" ]] && kill "$TAIL_PID" 2>/dev/null || true
}
trap cleanup EXIT

# Capture the process substitution's PID (via exec+$!) so we can clean it
# up afterward instead of leaving an orphaned `tail -F` running forever.
exec {TAIL_FD}< <(tail -n0 -F "$LOGFILE")
TAIL_PID=$!

while IFS= read -r line <&"$TAIL_FD"; do
    if [[ "$line" =~ ^\[[0-9]+/[0-9]+\] ]]; then
        echo "Boundary reached: $line"
        echo "Sending SIGINT to PID $JOB_PID"
        kill -INT "$JOB_PID"
        break
    fi
done

echo "Done — job should be stopping gracefully now (watch its own terminal for the ^C summary)."
