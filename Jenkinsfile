pipeline {
    agent any    
    
    stages {
        
        stage('Checkout') {
            steps {
                // Clonar el repositorio de tu código aquí         
                cleanWs()     
                git branch: 'main', credentialsId: 'jenkins-github-bst', url: 'https://github.com/BST-Tech/210_ClaroVTR-Backend-ComplianceNoMolestar-dev.git'
            }
        }

        stage('Create ZIP') {
            steps {
                script {
                    sh '''
                        cd backend/210_clarovtr_create_contact_center && zip -r ../../210_clarovtr_create_contact_center.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_create_user && zip -r ../../210_clarovtr_create_user.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_download_historical_leads && zip -r ../../210_clarovtr_download_historical_leads.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_get_historical_leads && zip -r ../../210_clarovtr_get_historical_leads.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_get_info_contact_center && zip -r ../../210_clarovtr_get_info_contact_center.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_get_user && zip -r ../../210_clarovtr_get_user.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_insert_tipificaciones && zip -r ../../210_clarovtr_insert_tipificaciones.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_last_login && zip -r ../../210_clarovtr_last_login.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_list_contact_center && zip -r ../../210_clarovtr_list_contact_center.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_list_contact_center_by_id && zip -r ../../210_clarovtr_list_contact_center_by_id.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_list_tipo_contact_center && zip -r ../../210_clarovtr_list_tipo_contact_center.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_put_contact_center && zip -r ../../210_clarovtr_put_contact_center.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_session_registration && zip -r ../../210_clarovtr_session_registration.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_upload_leads && zip -r ../../210_clarovtr_upload_leads.zip .
                    '''
                    sh '''
                        cd backend/210_clarovtr_validar_gestiones && zip -r ../../210_clarovtr_validar_gestiones.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_password_reset && zip -r ../../210_clavovtr_password_reset.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_delete_tipificacion && zip -r ../../210_clavovtr_delete_tipificacion.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_get_conctact_center && zip -r ../../210_clavovtr_get_conctact_center.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_get_roles && zip -r ../../210_clavovtr_get_roles.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_get_tipificaciones_list && zip -r ../../210_clavovtr_get_tipificaciones_list.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_get_tipificacion_by_id && zip -r ../../210_clavovtr_get_tipificacion_by_id.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_get_users_list && zip -r ../../210_clavovtr_get_users_list.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_put_tipificacion && zip -r ../../210_clavovtr_put_tipificacion.zip .
                    '''
                    sh '''
                        cd backend/210_clavovtr_put_users && zip -r ../../210_clavovtr_put_users.zip .
                    '''

                }
            }
        }

       stage('Deploy Terraform IaC') {
            steps {
                script {
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds-prod-bst', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        echo 'Deploy IaC Backend'
                        // sh '''                           
                        //    terraform init
                        //    terraform plan
                        //    terraform apply -auto-approve
                        // '''   
                    }                        
                }                
            }
        }      

        stage('Import Cognito User Pool') {
            steps {
                script {
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds-prod-bst', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        echo 'Import Cognito User Pool'
                        // sh '''
                        //     aws cognito-idp create-user-pool \
                        //     --pool-name "clarovtrNomolestar-userpool" \
                        //     --region "us-west-2" \
                        //     --username-attributes "email" \
                        //     --cli-input-json file://cognito/user-pool.json
                        // '''   
                    }                        
                }                
            }
        }

        stage('Import Cognito User Pool Client') {
            steps {
                script {
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds-prod-bst', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        echo 'Import Cognito User Pool Client'
                        sh '''
                            aws cognito-idp create-user-pool-client \
                            --region "us-west-2" \
                            --user-pool-id us-west-2_nFCex3Tgc \
                            --client-name create_userpool \
                            --cli-input-json file://cognito/user-pool-client-create.json
                        '''   
                    }                        
                }                
            }
        } 
         
        stage('Import Cognito User Pool Client Custom') {
            steps {
                script {
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds-prod-bst', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        echo 'Import Cognito User Pool Client'
                        // sh '''
                        //     aws cognito-idp set-ui-customization \
                        //     --region "us-west-2" \
                        //     --user-pool-id us-west-2_HVGSoOAbU \
                        //     --client-id 3kbeh0rg6vi49t7u2nqu8n7vvq \
                        //     --cli-input-json file://cognito/user_pool_client_customization.json
                        // '''   
                    }                        
                }                
            }
        }                 
    }

    post {
    success {
      office365ConnectorSend webhookUrl: "${WEBHOOK_TEAMS}",
            color: '#00FF00',
            factDefinitions: [[name: "Proyecto", template: "ClaroVTR: No Molestar Backend"],
            [name: "Pipeline", template: "${env.JOB_NAME}"],
            [name: "Infraestructura", template: "Infraestructura IaC Backend"],
            [name: "Nro. de Ejecución", template: "${env.BUILD_NUMBER}"]],
            status: "Success"  
    }

    failure {
       office365ConnectorSend webhookUrl: "${WEBHOOK_TEAMS}",
            color: '#FF0000',
            factDefinitions: [[name: "Proyecto", template: "ClaroVTR: No Molestar Backend"],
            [name: "Pipeline", template: "${env.JOB_NAME}"],
            [name: "Infraestructura", template: "Infraestructura IaC Backend"],
            [name: "Nro. de Ejecución", template: "${env.BUILD_NUMBER}"]],
            status: "Failure"   
    }
}
}
