# Resources

This folder contains additional helpful materials and resources for "Automating Serverless Workflows".

## 🎯 Main Demo Repository

**[mms-basic-functions-and-containers](https://github.com/donnietaylor/mms-basic-functions-and-containers)** - Complete demo series with working code, infrastructure, and CI/CD pipelines

## 📚 Official Azure Documentation

### Azure Functions
- **[Azure Functions Overview](https://docs.microsoft.com/en-us/azure/azure-functions/functions-overview)** - Core concepts and capabilities
- **[PowerShell in Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-powershell)** - PowerShell developer reference
- **[Azure Functions Triggers and Bindings](https://docs.microsoft.com/en-us/azure/azure-functions/functions-triggers-bindings)** - Complete binding reference
- **[Azure Functions Best Practices](https://docs.microsoft.com/en-us/azure/azure-functions/functions-best-practices)** - Performance and reliability patterns
- **[Durable Functions](https://docs.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview)** - Stateful workflows in serverless

### Azure Container Apps
- **[Azure Container Apps Overview](https://docs.microsoft.com/en-us/azure/container-apps/overview)** - Introduction and capabilities
- **[Container Apps Environments](https://docs.microsoft.com/en-us/azure/container-apps/environment)** - Environment configuration
- **[Scaling in Container Apps](https://docs.microsoft.com/en-us/azure/container-apps/scale-app)** - KEDA-based autoscaling
- **[Container Apps Networking](https://docs.microsoft.com/en-us/azure/container-apps/networking)** - Ingress, egress, and service-to-service
- **[Microservices with Container Apps](https://docs.microsoft.com/en-us/azure/container-apps/microservices)** - Architecture patterns

### Azure Logic Apps
- **[Logic Apps Overview](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-overview)** - Visual workflow designer
- **[Logic Apps Connectors](https://docs.microsoft.com/en-us/connectors/connector-reference/)** - 400+ pre-built connectors
- **[Logic Apps Standard vs Consumption](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-overview#resource-environment-differences)** - Pricing tier comparison
- **[Enterprise Integration](https://docs.microsoft.com/en-us/azure/logic-apps/logic-apps-enterprise-integration-overview)** - B2B and EDI workflows

### Azure Storage
- **[Azure Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-overview)** - Object storage for serverless
- **[Storage Bindings for Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-blob)** - Blob trigger and bindings
- **[Azure Queue Storage](https://docs.microsoft.com/en-us/azure/storage/queues/storage-queues-introduction)** - Message queuing service
- **[Azure Table Storage](https://docs.microsoft.com/en-us/azure/storage/tables/table-storage-overview)** - NoSQL key-value store

### Event-Driven Architecture
- **[Azure Event Grid](https://docs.microsoft.com/en-us/azure/event-grid/overview)** - Event routing service
- **[Azure Service Bus](https://docs.microsoft.com/en-us/azure/service-bus-messaging/service-bus-messaging-overview)** - Enterprise messaging
- **[Azure Event Hubs](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-about)** - Big data streaming platform

## 🛠️ Development Tools

### Essential Tools
- **[Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)** - Command-line interface for Azure
- **[Azure Functions Core Tools](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)** - Local development and testing
- **[Visual Studio Code](https://code.visualstudio.com/)** - Primary development IDE
- **[Docker Desktop](https://www.docker.com/products/docker-desktop)** - Container development and testing

### VS Code Extensions
- **[Azure Functions Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)** - Functions development in VS Code
- **[Azure Container Apps Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurecontainerapps)** - Container Apps management
- **[PowerShell Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.PowerShell)** - PowerShell development
- **[Docker Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker)** - Docker development
- **[Terraform Extension](https://marketplace.visualstudio.com/items?itemName=HashiCorp.terraform)** - Infrastructure as Code

### PowerShell Modules
```powershell
# Install Azure PowerShell modules
Install-Module -Name Az -Repository PSGallery -Force
Install-Module -Name Az.Functions -Repository PSGallery -Force
Install-Module -Name Az.Storage -Repository PSGallery -Force
Install-Module -Name Az.ContainerInstance -Repository PSGallery -Force
```

## 🏗️ Infrastructure as Code

### Terraform
- **[Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)** - Azure resource management
- **[Azure Functions Terraform Examples](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/linux_function_app)** - Function App resources
- **[Container Apps Terraform Examples](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/container_app)** - Container Apps resources
- **[Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)** - HashiCorp recommendations

### Azure Bicep
- **[Bicep Overview](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/overview)** - ARM template alternative
- **[Bicep Functions Templates](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/scenarios-functions)** - Functions deployment
- **[Bicep Container Apps Templates](https://docs.microsoft.com/en-us/azure/azure-resource-manager/bicep/scenarios-container-apps)** - Container Apps deployment

## 🚀 CI/CD and DevOps

### GitHub Actions
- **[GitHub Actions for Azure](https://github.com/Azure/actions)** - Azure-specific actions
- **[Deploy to Azure Functions](https://github.com/Azure/functions-action)** - Functions deployment action
- **[Deploy to Container Apps](https://github.com/Azure/container-apps-deploy-action)** - Container Apps action
- **[Azure Login Action](https://github.com/Azure/login)** - Authenticate to Azure

### Azure DevOps
- **[Azure Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/)** - CI/CD with Azure DevOps
- **[Azure Functions Task](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/deploy/azure-function-app)** - Deploy Functions
- **[Container Apps Task](https://docs.microsoft.com/en-us/azure/devops/pipelines/tasks/deploy/azure-container-apps)** - Deploy containers

## 📊 Monitoring and Observability

### Application Insights
- **[Application Insights Overview](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)** - APM for Azure
- **[Monitor Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/functions-monitoring)** - Functions telemetry
- **[Monitor Container Apps](https://docs.microsoft.com/en-us/azure/container-apps/observability)** - Container Apps monitoring
- **[Application Map](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-map)** - Service dependency visualization

### Log Analytics
- **[Azure Monitor Logs](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/data-platform-logs)** - Log querying and analysis
- **[Kusto Query Language (KQL)](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/)** - Query language for logs
- **[Log Analytics Workspace](https://docs.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-workspace-overview)** - Centralized logging

## 🔒 Security Best Practices

### Identity and Access
- **[Managed Identities](https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview)** - Credential-free authentication
- **[Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/general/overview)** - Secrets management
- **[Azure AD Integration](https://docs.microsoft.com/en-us/azure/active-directory/develop/)** - Authentication and authorization
- **[RBAC for Azure Functions](https://docs.microsoft.com/en-us/azure/azure-functions/security-concepts)** - Role-based access control

### Network Security
- **[Virtual Network Integration](https://docs.microsoft.com/en-us/azure/azure-functions/functions-networking-options)** - Private networking
- **[Private Endpoints](https://docs.microsoft.com/en-us/azure/private-link/private-endpoint-overview)** - Secure connectivity
- **[API Management](https://docs.microsoft.com/en-us/azure/api-management/api-management-key-concepts)** - API gateway and security

## 💰 Cost Optimization

### Pricing Resources
- **[Azure Functions Pricing](https://azure.microsoft.com/en-us/pricing/details/functions/)** - Consumption vs Premium plans
- **[Container Apps Pricing](https://azure.microsoft.com/en-us/pricing/details/container-apps/)** - Resource-based pricing
- **[Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)** - Estimate costs
- **[Cost Management](https://docs.microsoft.com/en-us/azure/cost-management-billing/)** - Monitor and optimize spending

### Optimization Tips
- Use Consumption plans for variable workloads
- Implement scale-to-zero for Container Apps
- Right-size Function App service plans
- Use storage lifecycle policies
- Implement efficient code patterns
- Monitor cold starts and optimize

## 📖 Learning Resources

### Microsoft Learn Paths
- **[Create Serverless Applications](https://docs.microsoft.com/en-us/learn/paths/create-serverless-applications/)** - Functions learning path
- **[Deploy Container Apps](https://docs.microsoft.com/en-us/learn/paths/deploy-container-apps/)** - Container Apps learning path
- **[Implement Azure Logic Apps](https://docs.microsoft.com/en-us/learn/paths/build-workflows-with-logic-apps/)** - Logic Apps learning path

### Community Resources
- **[Azure Functions Reddit](https://reddit.com/r/azurefunctions)** - Community discussions
- **[Azure Updates](https://azure.microsoft.com/en-us/updates/)** - Latest feature announcements
- **[Azure Blog](https://azure.microsoft.com/en-us/blog/)** - Technical articles and updates
- **[GitHub Azure Samples](https://github.com/Azure-Samples)** - Official code samples

### Books and Guides
- **[Azure Functions in Action](https://www.manning.com/books/azure-functions-in-action)** - Comprehensive Functions guide
- **[Serverless Architectures on Azure](https://azure.microsoft.com/en-us/resources/serverless-architectures-on-azure/)** - Architecture patterns
- **[Cloud Design Patterns](https://docs.microsoft.com/en-us/azure/architecture/patterns/)** - Architectural guidance

## 🎓 Certification Paths

- **[AZ-204: Developing Solutions for Microsoft Azure](https://docs.microsoft.com/en-us/learn/certifications/exams/az-204)** - Includes Functions and Container Apps
- **[AZ-400: DevOps Engineer Expert](https://docs.microsoft.com/en-us/learn/certifications/exams/az-400)** - CI/CD and automation
- **[AZ-305: Designing Microsoft Azure Infrastructure Solutions](https://docs.microsoft.com/en-us/learn/certifications/exams/az-305)** - Architecture design

## 🤝 Community and Support

### Getting Help
- **[Azure Functions GitHub](https://github.com/Azure/azure-functions)** - Issues and discussions
- **[Stack Overflow](https://stackoverflow.com/questions/tagged/azure-functions)** - Community Q&A
- **[Microsoft Q&A](https://docs.microsoft.com/en-us/answers/topics/azure-functions.html)** - Official Microsoft Q&A
- **[Azure Support](https://azure.microsoft.com/en-us/support/options/)** - Professional support options

### Stay Updated
- **[Azure Friday](https://azure.microsoft.com/en-us/resources/videos/azure-friday/)** - Weekly video series
- **[Azure DevOps Blog](https://devblogs.microsoft.com/devops/)** - DevOps updates
- **[Azure Twitter](https://twitter.com/azure)** - Latest announcements

---

These resources will help you advance your serverless automation skills and stay current with Azure best practices. Start with the [main demo repository](https://github.com/donnietaylor/mms-basic-functions-and-containers) for hands-on learning!