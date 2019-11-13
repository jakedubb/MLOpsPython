from azureml.core import Workspace
from azureml.core.model import InferenceConfig, Model
from azureml.core.webservice import LocalWebservice
from azureml.core.authentication import AzureCliAuthentication

cli_auth = AzureCliAuthentication()

subscription_id = '7fd76d0f-84f2-498b-a997-e0d059af5ce1'
resource_group  = 'sdbolts-AML-RG'
workspace_name  = 'sdbolts-AML-WS'

try:
    ws = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)
    ws.write_config()
    print('Library configuration succeeded')
except:
    print('Workspace not found')
# Get workspace
#ws = Workspace.from_config(auth=cli_auth, path='./')

# Create inference configuration. This creates a docker image that contains the model.
inference_config = InferenceConfig(runtime="python",
                                   entry_script="score.py",
                                   conda_file="conda_dependencies.yml")
model = Model(ws, name='sklearn_regression_model.pkl')

# Create a local deployment, using port 8890 for the web service endpoint
deployment_config = LocalWebservice.deploy_configuration(port=8890)
# Deploy the service
service = Model.deploy(
    ws, "mymodel", [model], inference_config, deployment_config)
# Wait for the deployment to complete
service.wait_for_deployment(True)
# Display the port that the web service is available on
print(service.port)