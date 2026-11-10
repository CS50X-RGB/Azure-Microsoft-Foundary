### Create Storage

az storage account create \
  --name raglearn2026x7 \
  --resource-group rg-rag-learning \
  --location centralindia \
  --sku Standard_LRS \
  --kind StorageV2 \
  --min-tls-version TLS1_2 \
  --allow-blob-public-access true

## Create Container
az storage container create \
  --name documents \
  --account-name raglearn2026x7 \
  --auth-mode login