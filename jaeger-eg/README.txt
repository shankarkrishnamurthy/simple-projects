References:
    main:
		https://github.com/jaegertracing/jaeger/tree/master/examples/hotrod
    	hands on: https://www.digitalocean.com/community/tutorials/how-to-implement-distributed-tracing-with-jaeger-on-kubernetes
    others:
		official: https://www.jaegertracing.io/download/, https://github.com/jaegertracing
		https://medium.com/opentracing/take-opentracing-for-a-hotrod-ride-f6e3141f7941
		tutorial: https://www.udemy.com/course/jaeger-distributed-tracing-for-cloud-native-applications/

official hotrod app:
  jaeger:
  git clone git@github.com:jaegertracing/jaeger.git jaeger
  cd jaeger
  go run ./examples/hotrod/main.go all
  go app:
  docker run --rm --name jaeger -p6831:6831/udp -p16686:16686 jaegertracing/all-in-one:latest
    
python app:
  frontend:
  cd frontend
  docker build --network host -t shankarkrishna/do-visit-counter-frontend:v1 .
  backend:
  cd backend
  docker build --network host -t shankarkrishna/do-visit-counter-backend:v1 .
  run locally (no jaeger yet):
  docker run --name backend --rm -p 5000:5000 shankarkrishna/do-visit-counter-backend:v1
  docker run --rm -p 8000:8000 -e COUNTER_ENDPOINT=http://$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' backend):5000 shankarkrishna/do-visit-counter-frontend:v1

  run in k8s cluster & test (no jaeger yet):
        kubectl apply -f ./deploy_frontend.yaml
        kubectl apply -f ./deploy_backend.yaml
        kubectl port-forward $(kubectl get pods -l=app="do-visit-counter-frontend" -o name) 8000:8000
        for i in 1 2 3; do curl localhost:8000; done

  deploy jaeger:
    crd:
    kubectl apply -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/crds/jaegertracing.io_jaegers_crd.yaml
    role,binding,sa:
    kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/service_account.yaml
    kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role.yaml
    kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role_binding.yaml
    jaeger operator:
    kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/operator.yaml
    kubectl apply -f jaeger.yaml

    kubectl port-forward --address 0.0.0.0 $(kubectl get pods -l=app="jaeger" -o name) 8080:16686

  instrumented app (with jaeger):
    kubectl apply -f deploy_frontend_instrumented.yaml
    kubectl apply -f deploy_backend_instrumented.yaml
    kubectl port-forward $(kubectl get pods -l=app="do-visit-counter-frontend" -o name) 8000:8000 &
    kubectl port-forward --address 0.0.0.0 $(kubectl get pods -l=app="jaeger" -o name) 8080:16686 &

  test from laptop/local dev m/c (with jaeger):
    http://54.183.251.219:8080/ # *http://<master node ip>:8080*
    
