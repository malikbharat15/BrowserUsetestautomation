#!/usr/bin/env python3
"""
GitHub Actions Webhook Simulator
Generates realistic webhook events for workflow runs, jobs, and steps
"""

import json
import time
import random
import requests
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import threading
import uuid
from dataclasses import dataclass
from typing import List, Dict, Any

app = Flask(__name__)


@dataclass
class WorkflowStep:
    name: str
    duration_seconds: int
    failure_rate: float = 0.05


@dataclass
class WorkflowJob:
    name: str
    steps: List[WorkflowStep]
    failure_rate: float = 0.1


# Define realistic CI/CD workflow structure
WORKFLOW_JOBS = [
    WorkflowJob("initialization", [
        WorkflowStep("Setup Runner", 30, 0.02),
        WorkflowStep("Checkout Code", 15, 0.01),
        WorkflowStep("Setup Dependencies", 45, 0.08)
    ]),
    WorkflowJob("build", [
        WorkflowStep("Setup Node.js", 20, 0.03),
        WorkflowStep("Install Dependencies", 60, 0.10),
        WorkflowStep("Build Application", 120, 0.15),
        WorkflowStep("Build Docker Image", 90, 0.08)
    ]),
    WorkflowJob("test", [
        WorkflowStep("Unit Tests", 180, 0.12),
        WorkflowStep("Integration Tests", 300, 0.20),
        WorkflowStep("Security Scan", 240, 0.05),
        WorkflowStep("Upload Test Results", 30, 0.02)
    ]),
    WorkflowJob("deploy_dev", [
        WorkflowStep("Deploy to Dev", 120, 0.15),
        WorkflowStep("Run Smoke Tests", 90, 0.10),
        WorkflowStep("Update Status", 10, 0.01)
    ]),
    WorkflowJob("deploy_qat", [
        WorkflowStep("Deploy to QAT", 150, 0.12),
        WorkflowStep("Run E2E Tests", 600, 0.25),
        WorkflowStep("Performance Tests", 300, 0.15),
        WorkflowStep("Update QAT Status", 10, 0.01)
    ]),
    WorkflowJob("deploy_prod", [
        WorkflowStep("Deploy to Production", 180, 0.08),
        WorkflowStep("Health Check", 60, 0.05),
        WorkflowStep("Notify Teams", 15, 0.01)
    ])
]


class GitHubWebhookSimulator:
    def __init__(self, webhook_url: str, otel_url: str):
        self.webhook_url = webhook_url
        self.otel_url = otel_url
        self.running = False

    def generate_workflow_run_event(self, action: str, conclusion: str = None) -> Dict[str, Any]:
        """Generate a realistic workflow_run webhook event"""
        run_id = random.randint(1000000, 9999999)

        return {
            "action": action,
            "workflow_run": {
                "id": run_id,
                "name": "CI/CD Pipeline",
                "node_id": f"WFR_{run_id}",
                "head_branch": random.choice(["main", "develop", "feature/auth", "bugfix/login"]),
                "head_sha": f"{random.randint(10 ** 39, 10 ** 40 - 1):040x}"[:40],
                "path": ".github/workflows/cicd.yml",
                "display_title": "CI/CD Pipeline",
                "run_number": random.randint(1, 1000),
                "event": random.choice(["push", "pull_request", "workflow_dispatch"]),
                "status": "completed" if conclusion else "in_progress",
                "conclusion": conclusion,
                "workflow_id": 12345,
                "url": f"https://api.github.com/repos/myorg/myapp/actions/runs/{run_id}",
                "html_url": f"https://github.com/myorg/myapp/actions/runs/{run_id}",
                "created_at": datetime.utcnow().isoformat() + "Z",
                "updated_at": datetime.utcnow().isoformat() + "Z",
                "actor": {
                    "login": random.choice(["dev1", "dev2", "devops", "qa-engineer"]),
                    "id": random.randint(1000, 9999)
                },
                "triggering_actor": {
                    "login": random.choice(["dev1", "dev2", "devops"]),
                    "id": random.randint(1000, 9999)
                }
            },
            "repository": {
                "id": 123456789,
                "name": "myapp",
                "full_name": "myorg/myapp",
                "private": True,
                "html_url": "https://github.com/myorg/myapp"
            },
            "organization": {
                "login": "myorg",
                "id": 12345
            }
        }

    def generate_job_event(self, action: str, job: WorkflowJob, run_id: int, conclusion: str = None) -> Dict[str, Any]:
        """Generate a workflow_job webhook event"""
        job_id = random.randint(1000000, 9999999)

        return {
            "action": action,
            "workflow_job": {
                "id": job_id,
                "run_id": run_id,
                "workflow_name": "CI/CD Pipeline",
                "head_branch": "main",
                "run_url": f"https://api.github.com/repos/myorg/myapp/actions/runs/{run_id}",
                "run_attempt": 1,
                "node_id": f"CR_{job_id}",
                "head_sha": f"{random.randint(10 ** 39, 10 ** 40 - 1):040x}"[:40],
                "url": f"https://api.github.com/repos/myorg/myapp/actions/jobs/{job_id}",
                "html_url": f"https://github.com/myorg/myapp/actions/runs/{run_id}/jobs/{job_id}",
                "status": "completed" if conclusion else "in_progress",
                "conclusion": conclusion,
                "created_at": datetime.utcnow().isoformat() + "Z",
                "started_at": datetime.utcnow().isoformat() + "Z",
                "completed_at": (datetime.utcnow() + timedelta(seconds=300)).isoformat() + "Z" if conclusion else None,
                "name": job.name,
                "steps": [],
                "check_run_url": f"https://api.github.com/repos/myorg/myapp/check-runs/{job_id}",
                "labels": ["ubuntu-latest"],
                "runner_id": random.randint(1, 100),
                "runner_name": f"runner-{random.randint(1, 10)}",
                "runner_group_id": 1,
                "runner_group_name": "Default"
            },
            "repository": {
                "id": 123456789,
                "name": "myapp",
                "full_name": "myorg/myapp"
            }
        }

    def send_otel_trace(self, span_data: Dict[str, Any]):
        """Send trace data to OTEL collector"""
        try:
            trace_payload = {
                "resourceSpans": [{
                    "resource": {
                        "attributes": [
                            {"key": "service.name", "value": {"stringValue": "github-actions"}},
                            {"key": "service.version", "value": {"stringValue": "1.0.0"}}
                        ]
                    },
                    "scopeSpans": [{
                        "scope": {"name": "github-webhook-simulator"},
                        "spans": [span_data]
                    }]
                }]
            }

            response = requests.post(
                f"{self.otel_url}/v1/traces",
                json=trace_payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"OTEL trace sent: {response.status_code}")
        except Exception as e:
            print(f"Failed to send OTEL trace: {e}")

    def send_otel_metrics(self, metric_data: Dict[str, Any]):
        """Send metrics to OTEL collector"""
        try:
            metrics_payload = {
                "resourceMetrics": [{
                    "resource": {
                        "attributes": [
                            {"key": "service.name", "value": {"stringValue": "github-actions"}}
                        ]
                    },
                    "scopeMetrics": [{
                        "scope": {"name": "github-webhook-simulator"},
                        "metrics": [metric_data]
                    }]
                }]
            }

            response = requests.post(
                f"{self.otel_url}/v1/metrics",
                json=metrics_payload,
                headers={"Content-Type": "application/json"}
            )
            print(f"OTEL metrics sent: {response.status_code}")
        except Exception as e:
            print(f"Failed to send OTEL metrics: {e}")

    def simulate_workflow_run(self):
        """Simulate a complete workflow run with all jobs and steps"""
        run_id = random.randint(1000000, 9999999)
        workflow_start_time = datetime.utcnow()

        print(f"Starting workflow run {run_id}")

        # Send workflow started event
        workflow_event = self.generate_workflow_run_event("requested")
        try:
            requests.post(self.webhook_url, json=workflow_event)
        except Exception as e:
            print(f"Failed to send webhook: {e}")

        # Create workflow span
        workflow_trace_id = f"{random.randint(10 ** 31, 10 ** 32 - 1):032x}"
        workflow_span_id = f"{random.randint(10 ** 15, 10 ** 16 - 1):016x}"

        workflow_failed = False
        current_time = workflow_start_time

        # Process each job
        for job_idx, job in enumerate(WORKFLOW_JOBS):
            job_start_time = current_time
            job_span_id = f"{random.randint(10 ** 15, 10 ** 16 - 1):016x}"

            print(f"  Starting job: {job.name}")

            # Send job started event
            job_event = self.generate_job_event("queued", job, run_id)
            try:
                requests.post(self.webhook_url, json=job_event)
                time.sleep(1)
                job_event = self.generate_job_event("in_progress", job, run_id)
                requests.post(self.webhook_url, json=job_event)
            except Exception as e:
                print(f"Failed to send job webhook: {e}")

            # Determine job outcome
            job_failed = random.random() < job.failure_rate
            if job_failed:
                workflow_failed = True

            # Process each step
            step_duration_total = 0
            for step_idx, step in enumerate(job.steps):
                step_span_id = f"{random.randint(10 ** 15, 10 ** 16 - 1):016x}"
                step_start_time = current_time

                # Add some variance to step duration
                actual_duration = max(5, int(step.duration_seconds * random.uniform(0.7, 1.5)))
                step_end_time = step_start_time + timedelta(seconds=actual_duration)
                step_duration_total += actual_duration

                step_failed = random.random() < step.failure_rate
                if step_failed:
                    job_failed = True
                    workflow_failed = True

                # Send step trace
                step_span = {
                    "traceId": workflow_trace_id,
                    "spanId": step_span_id,
                    "parentSpanId": job_span_id,
                    "name": f"step:{step.name}",
                    "startTimeUnixNano": int(step_start_time.timestamp() * 1e9),
                    "endTimeUnixNano": int(step_end_time.timestamp() * 1e9),
                    "attributes": [
                        {"key": "github.workflow.name", "value": {"stringValue": "CI/CD Pipeline"}},
                        {"key": "github.job.name", "value": {"stringValue": job.name}},
                        {"key": "github.step.name", "value": {"stringValue": step.name}},
                        {"key": "github.step.number", "value": {"intValue": str(step_idx + 1)}},
                        {"key": "github.run.id", "value": {"stringValue": str(run_id)}},
                        {"key": "github.repository", "value": {"stringValue": "myorg/myapp"}},
                        {"key": "step.outcome", "value": {"stringValue": "failure" if step_failed else "success"}}
                    ],
                    "status": {
                        "code": 2 if step_failed else 1  # ERROR or OK
                    }
                }
                self.send_otel_trace(step_span)

                print(f"    Step: {step.name} ({'FAILED' if step_failed else 'SUCCESS'}) - {actual_duration}s")

                current_time = step_end_time
                time.sleep(0.5)  # Small delay between steps

                if step_failed:
                    break  # Stop processing steps if one fails

            # Send job completion
            job_end_time = current_time
            job_conclusion = "failure" if job_failed else "success"

            job_event = self.generate_job_event("completed", job, run_id, job_conclusion)
            try:
                requests.post(self.webhook_url, json=job_event)
            except Exception as e:
                print(f"Failed to send job completion webhook: {e}")

            # Send job trace
            job_span = {
                "traceId": workflow_trace_id,
                "spanId": job_span_id,
                "parentSpanId": workflow_span_id,
                "name": f"job:{job.name}",
                "startTimeUnixNano": int(job_start_time.timestamp() * 1e9),
                "endTimeUnixNano": int(job_end_time.timestamp() * 1e9),
                "attributes": [
                    {"key": "github.workflow.name", "value": {"stringValue": "CI/CD Pipeline"}},
                    {"key": "github.job.name", "value": {"stringValue": job.name}},
                    {"key": "github.job.number", "value": {"intValue": str(job_idx + 1)}},
                    {"key": "github.run.id", "value": {"stringValue": str(run_id)}},
                    {"key": "github.repository", "value": {"stringValue": "myorg/myapp"}},
                    {"key": "job.outcome", "value": {"stringValue": job_conclusion}},
                    {"key": "job.duration_seconds", "value": {"intValue": str(step_duration_total)}}
                ],
                "status": {
                    "code": 2 if job_failed else 1
                }
            }
            self.send_otel_trace(job_span)

            print(f"  Job {job.name}: {'FAILED' if job_failed else 'SUCCESS'}")

            if job_failed and job.name not in ["deploy_dev", "deploy_qat", "deploy_prod"]:
                # Stop workflow if non-deployment job fails
                break

        # Send workflow completion
        workflow_end_time = current_time
        workflow_conclusion = "failure" if workflow_failed else "success"

        workflow_event = self.generate_workflow_run_event("completed", workflow_conclusion)
        try:
            requests.post(self.webhook_url, json=workflow_event)
        except Exception as e:
            print(f"Failed to send workflow completion webhook: {e}")

        # Send workflow trace
        workflow_span = {
            "traceId": workflow_trace_id,
            "spanId": workflow_span_id,
            "name": "workflow:CI/CD Pipeline",
            "startTimeUnixNano": int(workflow_start_time.timestamp() * 1e9),
            "endTimeUnixNano": int(workflow_end_time.timestamp() * 1e9),
            "attributes": [
                {"key": "github.workflow.name", "value": {"stringValue": "CI/CD Pipeline"}},
                {"key": "github.run.id", "value": {"stringValue": str(run_id)}},
                {"key": "github.repository", "value": {"stringValue": "myorg/myapp"}},
                {"key": "workflow.outcome", "value": {"stringValue": workflow_conclusion}},
                {"key": "workflow.duration_seconds",
                 "value": {"intValue": str(int((workflow_end_time - workflow_start_time).total_seconds()))}}
            ],
            "status": {
                "code": 2 if workflow_failed else 1
            }
        }
        self.send_otel_trace(workflow_span)

        # Send metrics
        workflow_duration_metric = {
            "name": "github_workflow_duration_seconds",
            "description": "Duration of GitHub workflow execution",
            "gauge": {
                "dataPoints": [{
                    "attributes": [
                        {"key": "workflow_name", "value": {"stringValue": "CI/CD Pipeline"}},
                        {"key": "repository", "value": {"stringValue": "myorg/myapp"}},
                        {"key": "outcome", "value": {"stringValue": workflow_conclusion}}
                    ],
                    "timeUnixNano": int(workflow_end_time.timestamp() * 1e9),
                    "asDouble": (workflow_end_time - workflow_start_time).total_seconds()
                }]
            }
        }
        self.send_otel_metrics(workflow_duration_metric)

        print(
            f"Workflow {run_id}: {'FAILED' if workflow_failed else 'SUCCESS'} - Total duration: {(workflow_end_time - workflow_start_time).total_seconds():.0f}s")
        return workflow_conclusion == "success"

    def run_continuous_simulation(self, interval_minutes: int = 5):
        """Run continuous workflow simulations"""
        self.running = True
        success_count = 0
        total_count = 0

        while self.running:
            try:
                success = self.simulate_workflow_run()
                total_count += 1
                if success:
                    success_count += 1

                success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
                print(f"\nRunning stats: {success_count}/{total_count} successful ({success_rate:.1f}%)")
                print(f"Waiting {interval_minutes} minutes until next run...\n")

                time.sleep(interval_minutes * 60)
            except KeyboardInterrupt:
                print("Stopping simulation...")
                self.running = False
                break
            except Exception as e:
                print(f"Error in simulation: {e}")
                time.sleep(30)


# Flask API endpoints
simulator = None


@app.route('/start', methods=['POST'])
def start_simulation():
    global simulator
    data = request.get_json() or {}
    interval = data.get('interval_minutes', 2)

    if simulator and simulator.running:
        return jsonify({"error": "Simulation already running"}), 400

    webhook_url = "http://otel-collector:8088/webhook/github"
    otel_url = "http://otel-collector:4318"

    simulator = GitHubWebhookSimulator(webhook_url, otel_url)

    thread = threading.Thread(target=simulator.run_continuous_simulation, args=(interval,))
    thread.daemon = True
    thread.start()

    return jsonify({"message": f"Simulation started with {interval} minute intervals"})


@app.route('/stop', methods=['POST'])
def stop_simulation():
    global simulator
    if simulator:
        simulator.running = False
    return jsonify({"message": "Simulation stopped"})


@app.route('/trigger', methods=['POST'])
def trigger_single_run():
    global simulator
    webhook_url = "http://otel-collector:8088/webhook/github"
    otel_url = "http://otel-collector:4318"

    if not simulator:
        simulator = GitHubWebhookSimulator(webhook_url, otel_url)

    success = simulator.simulate_workflow_run()
    return jsonify({"message": "Workflow run triggered", "success": success})


@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "running": simulator.running if simulator else False,
        "message": "GitHub Actions Webhook Simulator"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)