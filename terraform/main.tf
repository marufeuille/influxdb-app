terraform {
  backend "gcs" {
    bucket = "tf-backends-gcs"
    prefix = "terraform/state"
  }
}


resource "google_pubsub_topic" "influxdb_topic" {
  name = var.pubsub_topic_name
}

resource "google_compute_instance" "influxdb-instance" {
  name         = "influxdb-instance"
  machine_type = "g1-small"
  zone         = "asia-northeast1-b"

  boot_disk {
    initialize_params {
      image = "ubuntu-minimal-2104-hirsute-v20210826"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip       = "35.221.120.25"
      network_tier = "PREMIUM"
    }
  }


  service_account {
    email = "511586081157-compute@developer.gserviceaccount.com"
    scopes = [
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring.write",
      "https://www.googleapis.com/auth/service.management.readonly",
      "https://www.googleapis.com/auth/servicecontrol",
      "https://www.googleapis.com/auth/trace.append",
    ]
  }
}
