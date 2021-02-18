import requests
import os
import logging
import json
import kopf
from kube import wait_for_deployment_complete


class Deployments:
    def __init__(self):
        self.headers = {
            "Authorization": f"token {os.environ.get('GITHUB_TOKEN')}",
            "accept": "application/vnd.github.ant-man-preview+json",
        }
        self.uri = "https://api.github.com"
        self.status_params = ["environment_url", "log_url", "description"]

    def update(self, body, deployment_id, state):
        spec = body["spec"]
        meta = body["metadata"]

        data = {"state": state}

        # Process Optional Paramters
        for param in self.status_params:
            if spec.get(param):
                data[param] = spec.get(param)

        resp = requests.post(
            f"{self.uri}/repos/{spec['repo']}/deployments/{deployment_id}/statuses",
            headers=self.headers,
            data=json.dumps(data),
        )
        if resp.status_code > 299:
            raise kopf.PermanentError(f"{resp.text}")

    def create(self, body):
        spec = body["spec"]
        meta = body["metadata"]

        data = {
            "ref": spec.get("ref"),
            "transient_environment": spec.get("transient_environment", True),
            "environment": spec.get("environment"),
            "auto_merge": spec.get("auto_merge", False),
            "required_contexts": spec.get("required_contexts", []),
        }
        resp = requests.post(
            f"{self.uri}/repos/{spec['repo']}/deployments",
            headers=self.headers,
            data=json.dumps(data),
        )
        if resp.status_code > 299:
            raise kopf.PermanentError(f"{resp.text}")

        deployment_id = resp.json().get("id")

        if spec.get("deployment"):
            timeout = spec.get("deploymentTimout", 120)
            logging.info(
                f"waiting {timeout} seconds for deployment {spec['deployment']} in the {meta['namespace']} namespace"
            )

            if wait_for_deployment_complete(spec["deployment"], meta["namespace"], timeout=timeout):
                state = "success"
            else:
                state = "failure"
        else:
            logging.info("no deployment given, setting state to success")
            state = "success"

        self.update(body, deployment_id, state)

        return deployment_id

    def delete(self, body):
        env = body["spec"]["environment"]
        repo = body["spec"]["repo"]
        deployments = self.get_deployments_from_environment(repo, env)
        for dep in deployments:
            resp = self.delete_deployment(repo, dep["id"])
            if resp == 422:
                self.update(body, dep["id"], "inactive")
                self.delete_deployment(repo, dep["id"])

    def delete_deployment(self, gh_path, gh_deploy_id):
        resp = requests.delete(
            f"{self.uri}/repos/{gh_path}/deployments/{gh_deploy_id}",
            headers=self.headers,
        )
        return resp.status_code

    def get_deployments_from_environment(self, gh_path, environment):
        deployments = []
        params = {"environment": environment}
        deployments = requests.get(
            f"{self.uri}/repos/{gh_path}/deployments",
            headers=self.headers,
            params=params,
        )
        if deployments.status_code == 200:
            deployments = deployments.json()

        return deployments
