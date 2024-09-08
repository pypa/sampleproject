resource "google_storage_bucket_iam_member" "test" {
  bucket = "test"
  role   = "roles/viewer"

  # This is bad
  member = "allUsers"
}

# testtttt

# test
# test
