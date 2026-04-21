# Continuous Delivery Pipeline

A pipeline encompassing the second half of a CI/CD lifecycle which delivers an application using a push based GitOps approach.



**Goal:** Implement a solid Continuous Delivery pipeline with a pre-provided web application image pulled from ACR.

**Pipeline Features:**
- Helm Chart for centralized deployment and enabling modularity between environments for future implementation
- KEDA for versatile pod autoscaling including:
    * A baseline of 2 pods to ensure availability at all times
    * Cron scheduling to 5 pods as a baseline for high traffic hours (08:00 AM - 12:00 AM)
    * Additional CPU scaling triggering at 70% to catch traffic spikes early and Memory scaling at 80% to avoid scaling up unnecessarily.
- Jenkins Kubernetes cloud agent for build freshness and resource efficiency.
- Continuous Delivery deploying only upon human intervention
- Linting, Validation and Security scanning of helm chart using external tools (kubeconform, kube-linter)
- Pipeline waits for Health check to respond before announcing success, fails after 3 minutes of waiting.

**Environment:** To implement this project I worked on the Azure infrastructure provided. 
- A single VM to be used as a jenkins controller bootstrapped with the necessary tools and permissions to access a cluster.
- An AKS cluster with a bootstrapped dedicated namespace, pre-configured ingress controller.

**Challenges:** 
- Due to the limited permissions (single namespace, no access to Role and RoleBinding creation) I had to implement the cloud agent in an alternative method.
for this I used the permissions of the VM to generate a token in real time as a step in the pipeline and injected it as an pipeline environment variable to be used by the agent to authorize resource deployment.
- Due to the provided container image having significant security flaws such as running as root and using port 80 internally (likely due to its age, image uses Python 2.7.14) implementing security best practices required allowing the container to run as root while minimizing its unnecessary capabilities by use of security context.

**Steps taken to complete the task:**
- I first researched about the tools I would need, Including KEDA az cli and kubelogin, the environment I would be working in (Azure) and its concepts.
- I then explored the environment provided to me to verify necessary access and understand its mechanics, including Azure managed identity, and on the fly token genaration.
- After this I created a plan which included the Jenkins and Kubernetes mechanisms I would need to utilize and the features I would like to implement.
- I then started implementing beginning with creating a helm chart with resources such as deployment, ClusterIP service, image pull secret, KEDA and ingress rules. I focused on making the helm charts modular to enable reusability using templating and helpers, proper labeling for versatile search and filter, and ensuring security best practices by injecting sensitive values in real time using an external secret (Jenkins). 

