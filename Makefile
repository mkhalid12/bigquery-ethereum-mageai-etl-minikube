.PHONY: bootstrap install create-namespace install uninstall destroy

NAMESPACE=mk-mageai
HELM_REPO_MAGE=mk-mageai
HELM_REPO_PG=bitnami
APP_NAME=mageai
PROJECT_DIRECTORY={full/path/to/your/project/directory}/mage-ai/projects/

check-docker:
	docker version --format '{{.Server.Version}}'

setup-k8: check-docker
	arch -arm64 brew install minikube
	arch -arm64 brew install kubectl
	arch -arm64 brew install helm
	minikube version
	kubectl version --client
	minikube start --mount=true --driver=docker  --mount-string=$(PROJECT_DIRECTORY):/home/projects/  --ports=5432:5432,6789:6789

bootstrap:
	helm repo add $(HELM_REPO_MAGE) https://mkhalid12.github.io/helm-charts/
	helm repo add $(HELM_REPO_PG) https://charts.bitnami.com/bitnami
	helm repo update

create-namespace:
	kubectl create namespace $(NAMESPACE)
	kubectl create secret -n $(NAMESPACE) generic gcp-key --from-file=key.json=secrets/gcp_bg_user.json

install:
	helm upgrade --install --values mageai/values.yaml  $(APP_NAME) $(HELM_REPO_MAGE)/$(APP_NAME) -n $(NAMESPACE)
	kubectl create configmap db-schema --from-file=postgresql/table_script.sql -n mk-mageai
	helm upgrade --install --values   postgresql/values.yaml --set volumePermissions.enabled=true   postgresql $(HELM_REPO_PG)/postgresql  -n $(NAMESPACE)

uninstall-pg:
	helm delete postgresql -n $(NAMESPACE)
	kubectl delete pvc data-postgresql-0 -n $(NAMESPACE)
	kubectl delete configmap db-schema -n $(NAMESPACE)

forward-port:
	kubectl port-forward svc/$(APP_NAME) 6789:6789 -n $(NAMESPACE) &
	kubectl port-forward  svc/postgresql 5432:5432 -n $(NAMESPACE) &

kick-start: bootstrap create-namespace install

uninstall:
	helm uninstall $(APP_NAME) -n $(NAMESPACE)

destroy:
	# Backup pipeline source code before deleting the infra
	#docker cp minikube:/home/projects/mage_project/ ./projects/mage_project/
	kubectl delete namespace $(NAMESPACE)
	minikube stop
	minikube delete

