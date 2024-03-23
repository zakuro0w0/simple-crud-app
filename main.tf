terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.21"
    }
  }
}

provider "google" {
  credentials = file("${var.GOOGLE_APPLICATION_CREDENTIALS}")
  project     = var.project_id
  region      = var.region
}

variable "GOOGLE_APPLICATION_CREDENTIALS" {}
variable "project_id" {}
variable "region" {
  default = "us-central1"
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network"
}

resource "google_project_service" "firestore" {
  service            = "firestore.googleapis.com"
  disable_on_destroy = false
}

resource "google_firestore_database" "default" {
  name        = "simple-crud-app-database"
  provider    = google
  project     = var.project_id
  location_id = "asia-northeast1"
  type        = "FIRESTORE_NATIVE"
}

# resource "google_cloud_run_service" "default" {
#   name     = "crud-service"
#   location = var.region

#   template {
#     spec {
#       containers {
#         image = "gcr.io/${var.project_id}/crud-service:latest"
#       }
#     }
#   }

#   traffic {
#     percent         = 100
#     latest_revision = true
#   }
# }
