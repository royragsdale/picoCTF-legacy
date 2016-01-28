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
