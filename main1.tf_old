provider "aws" {
  region = "us-west-2"  # Cambia esto a la región deseada
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-nomolestar-clarovtr-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",  
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_lambda_function" "clarovtr_create_contact_center" {
  function_name = "210_clarovtr_create_contact_center"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_create_contact_center.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_create_user" {
  function_name = "210_clarovtr_create_user"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_create_user.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_delete_contact_center" {
  function_name = "210_clarovtr_delete_contact_center"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_delete_contact_center.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}
resource "aws_lambda_function" "clarovtr_delete_tipificacion" {
  function_name = "210_clarovtr_delete_tipificacion"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_delete_tipificacion.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_download_historical_leads" {
  function_name = "210_clarovtr_download_historical_leads"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_download_historical_leads.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}
resource "aws_lambda_function" "clarovtr_get_conctact_center" {
  function_name = "210_clarovtr_get_conctact_center"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_conctact_center.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_historical_leads" {
  function_name = "210_clarovtr_get_historical_leads"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_historical_leads.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_info_contact_center" {
  function_name = "210_clarovtr_get_info_contact_center"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_info_contact_center.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_perfiles" {
  function_name = "210_clarovtr_get_perfiles"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_perfiles.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_profile_list" {
  function_name = "210_clarovtr_get_profile_list"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_profile_list.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_roles" {
  function_name = "210_clarovtr_get_roles"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_roles.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_tipificacion_by_id" {
  function_name = "210_clarovtr_get_tipificacion_by_id"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_tipificacion_by_id.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_tipificaciones_list" {
  function_name = "210_clarovtr_get_tipificaciones_list"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_tipificaciones_list.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_user" {
  function_name = "210_clarovtr_get_user"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_user.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_get_users_list" {
  function_name = "210_clarovtr_get_users_list"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_users_list.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_insert_tipificaciones" {
  function_name = "210_clarovtr_insert_tipificaciones"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_insert_tipificaciones.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_last_login" {
  function_name = "210_clarovtr_last_login"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_last_login.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_list_contact_center" {
  function_name = "210_clarovtr_list_contact_center"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_list_contact_center.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_list_contact_center_by_id" {
  function_name = "210_clarovtr_list_contact_center_by_id"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_list_contact_center_by_id.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_list_empresas" {
  function_name = "210_clarovtr_list_empresas"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_list_empresas.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_list_reglas_negocio" {
  function_name = "210_clarovtr_list_reglas_negocio"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_list_reglas_negocio.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}
resource "aws_lambda_function" "clarovtr_list_tipo_contact_center" {
  function_name = "210_clarovtr_list_tipo_contact_center"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_list_tipo_contact_center.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_mantenedores" {
  function_name = "210_clarovtr_mantenedores"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_mantenedores.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_migrateusers_to_cognito" {
  function_name = "210_clarovtr_migrateusers_to_cognito"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_migrateusers_to_cognito.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_password_reset" {
  function_name = "210_clarovtr_password_reset"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_password_reset.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_put_contact_center" {
  function_name = "210_clarovtr_put_contact_center"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_put_contact_center.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_put_tipificacion" {
  function_name = "210_clarovtr_put_tipificacion"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_put_tipificacion.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_put_users" {
  function_name = "210_clarovtr_put_users"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_put_users.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_session_registration" {
  function_name = "210_clarovtr_session_registration"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_session_registration.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}
resource "aws_lambda_function" "clarovtr_upload_leads" {
  function_name = "210_clarovtr_upload_leads"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_upload_leads.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}

resource "aws_lambda_function" "clarovtr_validar_gestiones" {
  function_name = "210_clarovtr_validar_gestiones"
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_validar_gestiones.zip"  # Cambia esto al nombre de tu archivo ZIP
  timeout       = 60
  memory_size   = 128    
    tracing_config {
        mode = "PassThrough"
    }
    layers = [
        "arn:aws:lambda:us-west-2:868883634636:layer:layer-psycopg2-py311:1"
    ]
    tags = {
        BU_COST_CENTRE = "5001"
    }
}
