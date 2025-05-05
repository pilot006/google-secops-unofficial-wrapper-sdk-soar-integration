# Unofficial SecOps Wrapper SDK Integration for Google SecOps/Chronicle SOAR
Unofficial integration for Chronicle SOAR/Google SecOps to integrate with the new [SecOps Wrapper SDK](https://github.com/google/secops-wrapper). The version of this integration (releases in this repo) will match the version of SDK we're using.

## Service Account Requirement
You'll need to create a service account in your Google SecOps project (sometimes called Bring-your-own-project). It will require the permissions required for each action, with `Chronicle API Admin` given the most level of access. Once created, generate a JSON key for that service account and that's what you'll use for the integration.

## Available Actions
| SOAR Action | Description |
| ------------- | ------------- |
| Entity Summary | Returns a JSON object with enrichment details for any entity |
| Query SecOps Gemini | Ask a quesiton of the Gemini embedded in your SecOps instance |
| Query with Statistics | Run a stats/aggregation search and return results to case wall |
