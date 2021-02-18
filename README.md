# Github Deployment Operator
An Operator that updates the Github Deployment API on successful deployments. 


# Deploy 
create a github-deployment-controller namespace
```
kubectl create ns github-deployment-controller
```
create a secret and give it a GITHUB_TOKEN value 
```
kubectl -n github-deployment-controller create secret generic github-deployment-controller --from-literal=GITHUB_TOKEN=asdfjlasdfjalf
```

Review, and then apply manifests

```
kubectl -n github-deployment-controller apply -f deploy/
```

# Creating your first GithubDeployment 

```
---
apiVersion: jetpack.io/v1alpha1
kind: GithubDeployment
metadata:
  name: banker
spec:
  environment: 'qa'
  repo: 'whereismyjetpack/banker'
  environment_url: "https://github.com/whereismyjetpack"
  ref: "main"
```

This spec will create a Github Deployment, with the environment name of 'qa' in the 'whereismyjetpack/banker' repository

## Spec Reference
| Parameter         | Default | Description                                                                    | Required? |
|-------------------|---------|--------------------------------------------------------------------------------|-----------|
| environment       | n/a     | Github Environment                                                             | Yes       |
| repo              | n/a     | Github Repository in the org/repo format                                       | Yes       |
| ref               | n/a     | Github commit, branch, tag ref                                                 | Yes       |
| environment_url    | None    | URL where the Deployment can be reached                                        | No        |
| log_url            | None    | URL where the Deployment logs can be found (i.e CI build)                      | No        |
| description       | None    | A description for the deployment                                               | No        |
| deployment        | None    | The deployment name in the same namespace as GithubDeployment to watch         | No        |
| deploymentTimeout | 120     | Time in seconds to wait for rollout. Timeout will send failure state to Github | No        |

