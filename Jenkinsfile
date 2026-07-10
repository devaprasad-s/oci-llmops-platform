pipeline {
    agent any
    stages {
        stage('Deploy') {
           steps {
			   withCredentials([string(credentialsId:'ai-private-ip', variable:'AI_PRIVATE_IP')]){
				    sshagent(credentials: ['ai-node-ssh-key']) {
				      sh '''
					  ssh -o StrictHostKeyChecking=no ubuntu@$AI_PRIVATE_IP << 'EOF'
					     set -e #stops the process if any command fails
					     sudo -i
					     echo "Pulling latest code..."
					     cd oci-llmops-platform/
					     git pull origin
					     
					     echo "Building native ARM image..."
					     cd application
					     sudo docker build -t manifest-doctor:latest .
					     
					     echo "Exporting and injecting into K3s..."
					     sudo docker save -o ~/manifest-doctor.tar manifest-doctor:latest
					     sudo k3s ctr images import ~/manifest-doctor.tar
					     
					     echo "Orchestrating rollout..."
					     cd ..
					     sudo kubectl apply -f kubernetes/
					     sudo kubectl rollout restart deployment manifest-doc-deployment
					     
					     echo "Deployment successful!"
					     EOF
				      '''
			       }
			    }
	        }
        }
    
    }
}
