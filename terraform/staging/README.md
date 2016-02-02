# Staging Infrastructure

- This infrastructure will be used for play testing, integration, and development.
- It will allow a full end to end test that should match the publicly deployed environment.
- It will be internet accessible but is intended to be access controlled to prevent any compromise of the competition.

## Workflow
1. Make edits to the appropriate configuration file
2. Check what changes it will have
    - `terraform plan -var-file="secret.tfvars"`
    - look for things like improperly templated/applied variables
3. If everything looks good commit code explaining the changes
4. Apply the changes
    - `terraform apply -var-file="secret.tfvars"` 
5. Commit the newly modified `terraform.tfstate`

Note:  This will create the necessary server instances and configures networking but does not further provision or configure the servers.

## Common Tasks

### Rebuild a single server

1. Find resource name
    - `terraform show`
    - ex: `aws_instance.web`
2. Taint the resource
    - `terraform taint aws_instance.web`
    - this will only mark the server for recreation
3. Capture the plan
    - `terraform plan -var-file="secret.tfvars"`
    - this should show only the deletion of the instance and perhaps the modification of attached resources (eg: Elastic IP (eip), Elastic Block Storage (ebs)) that rely on the instance id
4. Commit the plan
    - `git add terraform.tfstate*`
    - `git commit -m "[PLAN ] - rebuild server aws_instance.web"`
    - this ensures that changes to infrastructure are tracked
5. Apply the plan
    - `terraform apply -var-file="secret.tfvars"`
    - this is the step that actually destroys the server and creates a new instance
6. Commit the results 
    - `git add terraform.tfstate*`
    - `git commit -m "[APPLY] - sucess rebuilding server aws_instance.web"`
    - this ensures that changes to infrastructure are tracked
7. Re-provision/Configure
    - run the relevant ansible playbooks
