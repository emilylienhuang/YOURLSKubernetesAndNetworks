# YOURLS, Kubernetes, and Docker Networks
This repository walks you through a step-by-step guide into experimenting with container orchestration and microservice architecture.
For the purposes of this application, we will be using Docker Desktop, K3d, and Docker Hub. 
Docker Desktop is required to provide the underlying containerruntime for k3d and the Docker Network. K3d is a local version of Kubernetes used to simulate a producstion-level environment.
Further, Python should be installed on your machine and accessible through the command line. 
**Note:** This guide is strictly for Windows users.

### Please follow the following tutorials for downloading and installing K3d and Docker Desktop:
👉 [Download Docker Desktop here](https://www.docker.com/products/docker-desktop/)
👉 [View k3d Installation Requirements and Instructions](https://k3d.io/stable/#requirements)

## Steps for Set Up
1. Start with the Docker Networks Guide
   * This will walk you through creating a YOURLS username and password and setting up the network configurations. Remember to tailor the scripts in this repository to your specific credentials
2. Follow the Kubernetes guide
3. Generate plots from the Jupyter notebook combining the results of each deployment type trial run

## About the Tests
**Performance Test**: This performance test uses Python to test the average URL shortening and redirection time in seconds, percent CPU usage, percent Memory usage, and throughput per second. The data is generated from fetching random Wikipedia articles with 30% repeated calls from previously seen websites.    



**Locust Test:** The locust test puts in simple requests at a high rate to see how many requests per second the system can tolerate.

## Watch out for
This project requires intensive CPU and memory usage. Without sufficient hardware, running this experiment can cause hardware failures, computer crashes, and memory loss.

## GLAF and Happy Coding!
