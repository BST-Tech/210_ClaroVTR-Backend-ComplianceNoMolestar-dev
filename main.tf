provider "aws" {
  region = "us-west-2"  # Cambia esto a la región deseada
}

resource "aws_lambda_function" "clarovtr_get_list_empresas" {
  function_name = "210_clarovtr_get_list_empresas"
  role          = "arn:aws:iam::868883634636:role/lambda-nomolestar-clarovtr-role"
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_list_empresas.zip"  # Cambia esto al nombre de tu archivo ZIP
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

resource "aws_lambda_function" "clarovtr_get_reglas_negocio_by_id" {
  function_name = "210_clarovtr_get_reglas_negocio_by_id"
  role          = "arn:aws:iam::868883634636:role/lambda-nomolestar-clarovtr-role"
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_get_reglas_negocio_by_id.zip"  # Cambia esto al nombre de tu archivo ZIP
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

resource "aws_lambda_function" "clarovtr_count_leads_cooler" {
  function_name = "210_clarovtr_count_leads_cooler"
  role          = "arn:aws:iam::868883634636:role/lambda-nomolestar-clarovtr-role"
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_count_leads_cooler.zip"  # Cambia esto al nombre de tu archivo ZIP
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

resource "aws_lambda_function" "clarovtr_list_tipo_evento" {
  function_name = "210_clarovtr_list_tipo_evento"
  role          = "arn:aws:iam::868883634636:role/lambda-nomolestar-clarovtr-role"
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_list_tipo_evento.zip"  # Cambia esto al nombre de tu archivo ZIP
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

resource "aws_lambda_function" "clarovtr_put_regla_negocio" {
  function_name = "210_clarovtr_put_regla_negocio"
  role          = "arn:aws:iam::868883634636:role/lambda-nomolestar-clarovtr-role"
  handler       = "main.run"  # Cambia esto al nombre de tu archivo Python y función handler
  runtime       = "python3.11"
  filename      = "210_clarovtr_put_regla_negocio.zip"  # Cambia esto al nombre de tu archivo ZIP
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