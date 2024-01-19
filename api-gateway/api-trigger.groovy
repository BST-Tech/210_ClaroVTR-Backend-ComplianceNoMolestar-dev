pipeline {
    agent any
    
    environment {
        REGION_NAME="us-west-2"
        ACCOUNT="868883634636"
        APIGW=""
        STATEMENT_ID=""
    }
    
    stages {
        
        stage('Activate Lambda API Gateway Trigger') {
            steps {
               
                echo 'Activación Trigger Api Lambdas......'
                    withCredentials([aws(accessKeyVariable: 'AWS_ACCESS_KEY_ID', credentialsId: 'aws-creds-prod-bst', secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        sh '''
                            APIGW=$(aws apigateway get-rest-apis --region ${REGION_NAME} --query "items[?name=='clarovtrNoMolestar'].id" --output text)
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_create_contact_center \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/POST/create_contact_center"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_create_user \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/POST/create_users"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_delete_tipificacion \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/PUT/delete_tipificacion"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_download_historical_leads \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/download_historical_leads"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_conctact_center \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_conctact_centers_list"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_historical_leads \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_historical_leads"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_roles \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_roles"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_session_registration \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_sessions_data"
                            
                                                     
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_tipificacion_by_id \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_tipificacion_by_id"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_tipificaciones_list \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_tipificaciones"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_user \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_user_by_id"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_users_list \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_users_list"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_insert_tipificaciones \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/POST/insert_tipificaciones"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_list_contact_center \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/list_contact_center"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_list_tipo_contact_center \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/list_tipo_contact_center"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_password_reset \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/POST/password_reset"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_put_tipificacion \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/PUT/put_tipificacion"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_create_user \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/PUT/put_users"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_last_login \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/PUT/update_last_login"
                            
                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_validar_gestiones \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/POST/upload_gestiones"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_migrateusers_to_cognito \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/POST/authenticate"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_count_leads_cooler \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/count_leads_cooler"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_mantenedores \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/*/entity_maintainer"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_reglas_negocio_by_id \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_reglas_negocio_by_id"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_info_contact_center \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/get_sessions_data"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_list_contact_center_by_id \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/list_contact_center_by_id"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_list_empresas \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/list_empresa_login"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_get_list_empresas \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/list_list_empresa_user"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_list_reglas_negocio \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/list_reglas_negocio"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_list_tipo_evento \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/GET/list_tipo_evento"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_put_contact_center \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/PUT/put_contact_center"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_put_regla_negocio \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/PUT/put_regla_negocio"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_put_users \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/PUT/put_users"

                            STATEMENT_ID=$(uuidgen)
                            aws lambda add-permission --function-name 210_clarovtr_upload_leads \
                            --region ${REGION_NAME} \
                            --statement-id ${STATEMENT_ID} \
                            --action lambda:InvokeFunction \
                            --principal apigateway.amazonaws.com \
                            --source-arn "arn:aws:execute-api:${REGION_NAME}:${ACCOUNT}:${APIGW}/*/POST/upload_leads"
                            
                        '''
                    }
            }
        }
    }
}
