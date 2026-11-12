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

## Created Search 
az search service create \
  --name raglearningsearch866 \
  --resource-group rg-rag-learning \
  --location centralindia \
  --sku free \
  --partition-count 1 \
  --replica-count 1

## Gives Search API 
az search admin-key show --service-name raglearningsearch866 --resource-group rg-rag-learning
{
  "primaryKey": "###",
  "secondaryKey": "###"
}
Take the primaryKey for the as search key