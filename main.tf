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

resource "google_project_service" "firestore" {
  service            = "firestore.googleapis.com"
  disable_on_destroy = false
}

resource "google_firestore_database" "default" {
  # firestoreリソースはGCPプロジェクトに1個だけにする
  # 複数作成できるがFirebaseSDKで参照できるのは1個だけ
  # firestoreデータベース名が"(default)"でなければならない
  # FirebaseSDKでデータベース名は指定できない
  name        = "(default)"
  provider    = google
  project     = var.project_id
  location_id = "asia-northeast1"
  type        = "FIRESTORE_NATIVE"
}

