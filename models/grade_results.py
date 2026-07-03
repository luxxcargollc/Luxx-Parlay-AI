@"
from models.manual_grader import manual_grade_latest_run
from models.performance_tracker import show_performance_tracker

manual_grade_latest_run()
show_performance_tracker()
"@ | Set-Content -Path .\grade_results.py