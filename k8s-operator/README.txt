Author: Shankar, K
Date: Dec 2020

Description:
    This elustrates custom controller (or) operator for custom resource
    this operator monitors configMap and does take action

Steps:
    1. Build and Run App which uses configmap:
        docker build -f Dockerfile-app -t shankarkrishna/my-flask-app:test .
        docker push shankarkrishna/my-flask-app:test
        kubectl apply -f my-cm.yaml 
        kubectl apply -f my-app-deploy.yaml

    2. Build Operator, apply CRD & Customer Resource:
        docker build --network=host -t shankarkrishna/operator-k8s-app:test .
        docker push shankarkrishna/operator-k8s-app:test
        kubectl apply -f my-crd.yaml
        kubectl apply -f my-custom-defn.yaml

    3. Create ServiceAccount, ClusterRoleBinding and Run Operator:
        kubectl apply -f my-serviceaccount.yaml 
        kubectl apply -f my-clusterrolebinding.yaml 
        kubectl apply -f my-operator-deploy.yaml
        
    4. Monitor and Test:
        kubectl logs -f $(kubectl get pod -l"app=operator"  -o jsonpath="{.items[0].metadata.name}") app    
        modify my-cm.yaml "MSG"
        kubectl apply -f my-cm.yaml
        verify pod restarted
        
       
