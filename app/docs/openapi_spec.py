def build_openapi_spec(base_url="http://127.0.0.1:5000"):
    return {
        "openapi": "3.0.3",
        "info": {
            "title": "Financas Pessoais API",
            "version": "1.0.0",
            "description": "API REST do MVP de finanças pessoais.",
        },
        "servers": [{"url": base_url}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                }
            },
            "schemas": {
                "ErrorResponse": {
                    "type": "object",
                    "properties": {"error": {"type": "string"}},
                    "required": ["error"],
                },
                "AuthRegisterRequest": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string", "minLength": 8},
                    },
                    "required": ["name", "email", "password"],
                },
                "AuthLoginRequest": {
                    "type": "object",
                    "properties": {
                        "email": {"type": "string", "format": "email"},
                        "password": {"type": "string"},
                    },
                    "required": ["email", "password"],
                },
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                },
                "AuthLoginData": {
                    "type": "object",
                    "properties": {
                        "access_token": {"type": "string"},
                        "token_type": {"type": "string", "example": "Bearer"},
                    },
                },
                "CategoryRequest": {
                    "type": "object",
                    "properties": {"name": {"type": "string"}},
                    "required": ["name"],
                },
                "Category": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "name": {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                },
                "IncomeRequest": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "string", "example": "2500.00"},
                        "description": {"type": "string", "nullable": True},
                        "received_at": {"type": "string", "format": "date-time"},
                    },
                    "required": ["amount", "received_at"],
                },
                "IncomeUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "string", "example": "2500.00"},
                        "description": {"type": "string", "nullable": True},
                        "received_at": {"type": "string", "format": "date-time"},
                    },
                },
                "Income": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "amount": {"type": "string"},
                        "description": {"type": "string", "nullable": True},
                        "received_at": {"type": "string", "format": "date-time"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                },
                "ExpenseRequest": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "integer"},
                        "amount": {"type": "string", "example": "450.00"},
                        "description": {"type": "string", "nullable": True},
                        "spent_at": {"type": "string", "format": "date-time"},
                    },
                    "required": ["category_id", "amount", "spent_at"],
                },
                "ExpenseUpdateRequest": {
                    "type": "object",
                    "properties": {
                        "category_id": {"type": "integer"},
                        "amount": {"type": "string", "example": "450.00"},
                        "description": {"type": "string", "nullable": True},
                        "spent_at": {"type": "string", "format": "date-time"},
                    },
                },
                "Expense": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "user_id": {"type": "integer"},
                        "category_id": {"type": "integer"},
                        "amount": {"type": "string"},
                        "description": {"type": "string", "nullable": True},
                        "spent_at": {"type": "string", "format": "date-time"},
                        "created_at": {"type": "string", "format": "date-time"},
                        "updated_at": {"type": "string", "format": "date-time"},
                    },
                },
                "DashboardSummary": {
                    "type": "object",
                    "properties": {
                        "month": {"type": "integer"},
                        "year": {"type": "integer"},
                        "total_incomes": {"type": "string"},
                        "total_expenses": {"type": "string"},
                        "balance": {"type": "string"},
                        "expenses_by_category": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "category": {"type": "string"},
                                    "total": {"type": "string"},
                                },
                            },
                        },
                    },
                },
            },
        },
        "paths": {
            "/api/auth/register": {
                "post": {
                    "tags": ["Auth"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AuthRegisterRequest"}
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Usuário registrado",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "data": {"$ref": "#/components/schemas/User"},
                                        },
                                    }
                                }
                            },
                        },
                        "400": {"description": "Erro de validação"},
                        "409": {"description": "Email já cadastrado"},
                    },
                }
            },
            "/api/auth/login": {
                "post": {
                    "tags": ["Auth"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AuthLoginRequest"}
                            }
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Login realizado",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"data": {"$ref": "#/components/schemas/AuthLoginData"}},
                                    }
                                }
                            },
                        },
                        "401": {"description": "Credenciais inválidas"},
                    },
                }
            },
            "/api/auth/me": {
                "get": {
                    "tags": ["Auth"],
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Usuário autenticado",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {"data": {"$ref": "#/components/schemas/User"}},
                                    }
                                }
                            },
                        },
                        "401": {"description": "Não autorizado"},
                    },
                }
            },
            "/api/categories": {
                "get": {
                    "tags": ["Categories"],
                    "security": [{"bearerAuth": []}],
                    "responses": {
                        "200": {
                            "description": "Lista de categorias",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "data": {
                                                "type": "array",
                                                "items": {"$ref": "#/components/schemas/Category"},
                                            }
                                        },
                                    }
                                }
                            },
                        }
                    },
                },
                "post": {
                    "tags": ["Categories"],
                    "security": [{"bearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CategoryRequest"}
                            }
                        },
                    },
                    "responses": {
                        "201": {
                            "description": "Categoria criada",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "message": {"type": "string"},
                                            "data": {"$ref": "#/components/schemas/Category"},
                                        },
                                    }
                                }
                            },
                        },
                        "409": {"description": "Categoria duplicada"},
                    },
                },
            },
            "/api/categories/{id}": {
                "put": {
                    "tags": ["Categories"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/CategoryRequest"}
                            }
                        },
                    },
                    "responses": {"200": {"description": "Categoria atualizada"}, "404": {"description": "Não encontrada"}},
                },
                "delete": {
                    "tags": ["Categories"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {"200": {"description": "Categoria removida"}, "404": {"description": "Não encontrada"}},
                },
            },
            "/api/incomes": {
                "get": {
                    "tags": ["Incomes"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "month", "in": "query", "required": False, "schema": {"type": "integer"}},
                        {"name": "year", "in": "query", "required": False, "schema": {"type": "integer"}},
                    ],
                    "responses": {"200": {"description": "Lista de receitas"}},
                },
                "post": {
                    "tags": ["Incomes"],
                    "security": [{"bearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/IncomeRequest"}}
                        },
                    },
                    "responses": {"201": {"description": "Receita criada"}},
                },
            },
            "/api/incomes/{id}": {
                "get": {
                    "tags": ["Incomes"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {"200": {"description": "Receita"}, "404": {"description": "Não encontrada"}},
                },
                "put": {
                    "tags": ["Incomes"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/IncomeUpdateRequest"}
                            }
                        },
                    },
                    "responses": {"200": {"description": "Receita atualizada"}, "404": {"description": "Não encontrada"}},
                },
                "delete": {
                    "tags": ["Incomes"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {"200": {"description": "Receita removida"}, "404": {"description": "Não encontrada"}},
                },
            },
            "/api/expenses": {
                "get": {
                    "tags": ["Expenses"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "month", "in": "query", "required": False, "schema": {"type": "integer"}},
                        {"name": "year", "in": "query", "required": False, "schema": {"type": "integer"}},
                    ],
                    "responses": {"200": {"description": "Lista de despesas"}},
                },
                "post": {
                    "tags": ["Expenses"],
                    "security": [{"bearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {"schema": {"$ref": "#/components/schemas/ExpenseRequest"}}
                        },
                    },
                    "responses": {"201": {"description": "Despesa criada"}},
                },
            },
            "/api/expenses/{id}": {
                "get": {
                    "tags": ["Expenses"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {"200": {"description": "Despesa"}, "404": {"description": "Não encontrada"}},
                },
                "put": {
                    "tags": ["Expenses"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ExpenseUpdateRequest"}
                            }
                        },
                    },
                    "responses": {"200": {"description": "Despesa atualizada"}, "404": {"description": "Não encontrada"}},
                },
                "delete": {
                    "tags": ["Expenses"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "id", "in": "path", "required": True, "schema": {"type": "integer"}}
                    ],
                    "responses": {"200": {"description": "Despesa removida"}, "404": {"description": "Não encontrada"}},
                },
            },
            "/api/dashboard/summary": {
                "get": {
                    "tags": ["Dashboard"],
                    "security": [{"bearerAuth": []}],
                    "parameters": [
                        {"name": "month", "in": "query", "required": False, "schema": {"type": "integer"}},
                        {"name": "year", "in": "query", "required": False, "schema": {"type": "integer"}},
                    ],
                    "responses": {
                        "200": {
                            "description": "Resumo mensal",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "data": {"$ref": "#/components/schemas/DashboardSummary"}
                                        },
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
    }
