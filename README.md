# Personal Homelab & Portfolio Platform

## Overview

This project began as a personal initiative to host my own portfolio website and gain hands-on experience with modern cloud and DevOps practices.

Rather than relying on third-party hosting platforms, I wanted to understand how applications are deployed, monitored, and maintained in a real environment. Throughout my cloud and DevOps bootcamp, I used this homelab as a practical learning platform to reinforce concepts such as containerisation, CI/CD automation, infrastructure monitoring, and cloud-native deployment workflows.

This project is not intended to be a production enterprise platform. It serves as a personal learning environment where I can experiment, test new technologies, and continuously improve my understanding of cloud computing and modern application delivery.

---

## Objectives

* Host and maintain my own portfolio website
* Learn containerisation using Docker
* Implement automated deployment pipelines
* Gain exposure to Kubernetes concepts
* Build monitoring and observability capabilities
* Practise Git-based development workflows
* Apply cloud and DevOps concepts learned during training

---

## Technology Stack

### Application Layer

* Flask
* HTML
* CSS
* MySQL

### Containerisation

* Docker
* Docker Compose

### CI/CD

* GitHub Actions
* Azure DevOps Pipelines
* Self Hosted Runners
* Self Hosted Azure DevOps Agent

### Kubernetes

* k3s

### Monitoring & Observability

* Prometheus
* Grafana
* Node Exporter
* cAdvisor
* Alertmanager
* Dozzle

### Networking

* Cloudflare Tunnel

---

## Solution Architecture

GitHub / Azure DevOps Repository

↓

Automated CI/CD Pipeline

↓

Docker Image Build

↓

Deployment to Homelab Environment

↓

Application Services

↓

Monitoring & Alerting Stack

---

## Features

### Portfolio Website

A lightweight personal portfolio application developed using Flask and MySQL.

### Automated Deployment

Code changes pushed to the repository automatically trigger deployment workflows through CI/CD pipelines.

### Containerised Applications

Applications are packaged using Docker for portability and consistency across environments.

### Monitoring & Dashboards

Prometheus collects infrastructure and container metrics while Grafana provides visualisation and monitoring dashboards.

### Alerting

Alertmanager provides notification capabilities when predefined monitoring thresholds are exceeded.

### Secure Remote Access

Cloudflare Tunnel provides secure access without exposing inbound ports to the internet.

---

## Key Learning Outcomes

Through this project I gained practical exposure to:

* Git workflows
* Source control management
* CI/CD automation
* Docker containerisation
* Kubernetes fundamentals
* Infrastructure monitoring
* Application observability
* Cloud-native deployment concepts
* Troubleshooting and operational workflows

---

## Future Enhancements

Planned areas for future exploration include:

* Loki and Promtail log aggregation
* Uptime monitoring
* Container image security scanning
* Azure cloud-native deployments
* AI-powered portfolio enhancements
* Infrastructure as Code using Terraform

---

## Disclaimer

This homelab is a personal learning environment and portfolio project. It was created to support continuous learning and experimentation while reinforcing concepts from cloud and DevOps training programmes. The platform continues to evolve as new technologies and ideas are explored.
