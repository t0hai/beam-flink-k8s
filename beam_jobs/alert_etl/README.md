## Build Job Module
Set environment variables to connect Poetry to private repository (e.g. in AWS CodeArtifact):
```
export CODEARTIFACT_ENDPOINT=$(aws codeartifact get-repository-endpoint --domain <your_domain> --repository <your_repo> --format pypi --query repositoryEndpoint --output text)
export CODEARTIFACT_TOKEN=$(aws codeartifact get-authorization-token --domain <your_domain> --query authorizationToken --output text)
export CODEARTIFACT_USER=aws
```

Configure Poetry to use CodeArtifact
```
poetry config repositories.aws $CODEARTIFACT_REPOSITORY_URL
poetry config http-basic.aws $CODEARTIFACT_USER $CODEARTIFACT_AUTH_TOKEN
```