# Test Report: Socket-Based Port Availability Checker

**Student:**  
**Course:** Computer Networks  
**Date:**  

## Objective
Evaluate whether the program correctly reports TCP port connection outcomes for authorized localhost/private-network targets.

## Environment
- Operating system:
- Python version:
- CPU/device:
- Target:
- Timeout:

## Test results
Fill this table using your own observed results.

| Case | Target:Port | Expected | Actual | Latency (ms) | Pass/Fail |
|---|---|---|---|---:|---|
| Open port | 127.0.0.1:5001 | Open while app is running | | | |
| Closed port | 127.0.0.1:54321 | Usually Closed | | | |
| Invalid port | 127.0.0.1:70000 | Validation error | | N/A | |
| Range check | 127.0.0.1:5000-5010 | Per-port results | | | |
| Range too large | 127.0.0.1:1-101 | Rejected | | N/A | |

## Performance method
Run each valid test at least five times under the same conditions. Record each measured latency, then calculate average latency = sum of measurements / number of measurements. Include actual observations only.

## Discussion
Explain effects of timeout, firewall behavior, whether a service is listening, and why a timeout does not prove a port is closed.

## Conclusion
Summarize what passed, known limitations, and possible future improvements.
