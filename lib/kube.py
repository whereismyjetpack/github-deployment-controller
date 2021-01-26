from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.config.config_exception import ConfigException
import time
import logging


def wait_for_deployment_complete(deployment_name, namespace, timeout=60):

    try:
        config.load_incluster_config()
    except ConfigException:
        config.load_kube_config()

    api = client.AppsV1Api()
    start = time.time()
    while time.time() - start < timeout:
        logging.info(f"{time.time() - start}")
        time.sleep(2)
        try:
            response = api.read_namespaced_deployment_status(deployment_name, namespace)
        except ApiException as exc:
            if isinstance(exc, ApiException) and exc.status == 404:
                logging.info(f"Deployment Not found. Continuing")
                continue
            else:
                raise kopf.PermanentError(exc)

        s = response.status
        if (
            s.updated_replicas == response.spec.replicas
            and s.replicas == response.spec.replicas
            and s.available_replicas == response.spec.replicas
            and s.observed_generation >= response.metadata.generation
        ):
            return True
        else:
            print(
                f"[updated_replicas:{s.updated_replicas},replicas:{s.replicas}"
                ",available_replicas:{s.available_replicas},observed_generation:{s.observed_generation}] waiting..."
            )

    return False
