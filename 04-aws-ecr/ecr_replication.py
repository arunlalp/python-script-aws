import boto3
import subprocess

# Define source and destination regions
source_region = 'us-west-2'
destination_region = 'us-east-1'

# Define boto3 clients
ecr_source_client = boto3.client('ecr', region_name=source_region)
ecr_destination_client = boto3.client('ecr', region_name=destination_region)

# Authenticate Docker to ECR in both regions
def docker_login(region):
    password = subprocess.run(
        f"aws ecr get-login-password --region {region}",
        shell=True,
        check=True,
        capture_output=True,
        text=True
    ).stdout.strip()

    account_id = boto3.client('sts').get_caller_identity().get('Account')
    ecr_url = f"{account_id}.dkr.ecr.{region}.amazonaws.com"

    subprocess.run(
        f"docker login --username AWS --password {password} {ecr_url}",
        shell=True,
        check=True
    )

docker_login(source_region)
docker_login(destination_region)

# Get the list of repositories in the source region
repositories = ecr_source_client.describe_repositories()['repositories']

for repo in repositories:
    repo_name = repo['repositoryName']
    
    # Ensure the repository exists in the destination region
    try:
        ecr_destination_client.create_repository(repositoryName=repo_name)
    except ecr_destination_client.exceptions.RepositoryAlreadyExistsException:
        pass  # Repository already exists, continue

    # List images in the source repository
    images = ecr_source_client.list_images(repositoryName=repo_name)['imageIds']

    for image in images:
        image_tag = image.get('imageTag')
        image_digest = image.get('imageDigest')

        if image_tag:
            # Pull image from source region
            source_image_uri = f"{repo['registryId']}.dkr.ecr.{source_region}.amazonaws.com/{repo_name}:{image_tag}"
            subprocess.run(f"docker pull {source_image_uri}", shell=True, check=True)

            # Tag image for destination region
            destination_image_uri = f"{repo['registryId']}.dkr.ecr.{destination_region}.amazonaws.com/{repo_name}:{image_tag}"
            subprocess.run(f"docker tag {source_image_uri} {destination_image_uri}", shell=True, check=True)

            # Push image to destination region
            subprocess.run(f"docker push {destination_image_uri}", shell=True, check=True)

        elif image_digest:
            # Pull image by digest from source region
            source_image_uri = f"{repo['registryId']}.dkr.ecr.{source_region}.amazonaws.com/{repo_name}@{image_digest}"
            subprocess.run(f"docker pull {source_image_uri}", shell=True, check=True)

            # Tag image for destination region
            destination_image_uri = f"{repo['registryId']}.dkr.ecr.{destination_region}.amazonaws.com/{repo_name}@{image_digest}"
            subprocess.run(f"docker tag {source_image_uri} {destination_image_uri}", shell=True, check=True)

            # Push image to destination region
            subprocess.run(f"docker push {destination_image_uri}", shell=True, check=True)

print("Replication complete")
