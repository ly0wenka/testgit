# Step 1: Build (if you haven't)
docker tag hello-c aitoly0w/hello-c:latest


# Step 2: Tag it with Docker Hub repo
docker tag my-image-name aitoly0w/my-app:latest

# Step 3: Login to Docker Hub (if not already)
docker login

# Step 4: Push
docker push aitoly0w/hello-c:latest
