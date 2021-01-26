import kopf
import os
import requests
import logging
from deployments import Deployments


@kopf.on.create("jetpack.io", "v1alpha1", "githubdeployments")
@kopf.on.update("jetpack.io", "v1alpha1", "githubdeployments")
def create_fn(body, **kwargs):
    d = Deployments()
    # deployment_id = body.get("status", {}).get("create_fn", {}).get("deployment_id")
    # if deployment_id:
    #     logging.info(f"found existing deployment, inactivating it before proceeding")
    #     d.update(body, deployment_id, "inactive")

    deployment_id = d.create(body)

    return {"deployment_id": deployment_id}


@kopf.on.delete("jetpack.io", "v1alpha1", "githubdeployments")
def delete_fn(body, **kwargs):
    d = Deployments()
    d.delete(body)
