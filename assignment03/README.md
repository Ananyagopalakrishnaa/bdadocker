Installing Docker Desktop on Windows
Installation Steps:

1. Download Docker Desktop:
   - Visit https://www.docker.com/products/docker-desktop
   - Download the Docker Desktop installer and run it.

2. Install Docker Desktop:
   - Follow the on-screen instructions to install Docker Desktop.
   - You might be prompted to enable the WSL 2 backend during the installation. Allow it, as it provides better performance and compatibility.

3. Start Docker Desktop:
   - Once installed, start Docker Desktop. You should see the Docker icon in your system tray when Docker is running.
------------------------------------------------------------------------------------------------------------------------------------------
Installing Docker Desktop on macOS
Installation Steps:

Download Docker Desktop:

Visit https://www.docker.com/products/docker-desktop
Download the Docker Desktop installer for macOS and open it.
Install Docker Desktop:

Follow the on-screen instructions to install Docker Desktop.
When prompted, drag and drop Docker.app to your Applications folder.
Start Docker Desktop:

Open Docker from your Applications folder.
You should see the Docker icon in your menu bar when Docker is running.
------------------------------------------------------------------------------------------------------------------------------------------
Running Docker Project:

1. Navigate to Project Directory:
   - Open a terminal or command prompt and navigate to the directory where your friend's unzipped folder is located.
    cd /path to the folder

2. Build and Run Docker Containers as a daemon process:
   docker-compose up - d --build 

3. To check the working of the containers:
    docker ps
    docker images

4. to check functionality of any 1 container:
    docker-compose logs <container_name>

------------------------------------------------------------------------------------------------------------------------------------------

Running kibana:
    Kibana is setup in the localhost with the port number 5061 to see the bar graph, 
1. open a browser and find
    http://localhost:5601/app/home#/

2. Navigate to the dashboard and visualize the NER panel present

------------------------------------------------------------------------------------------------------------------------------------------

To stop the container
docker-compose down
